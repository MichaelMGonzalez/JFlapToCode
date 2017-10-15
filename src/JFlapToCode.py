import xml.etree.ElementTree as ET
import json
import sys
import jinja2
import os
from Constants import *
from GraphUtils import *
from CodeWriter import *

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader( templates_dir ))
JINJA_ENVIRONMENT.line_comment_prefix = "#//"

class JFlapParser:
    def __init__(self, config_file=None ):
       self.config = {}
       self.load_config(config_file)
       self.line_statement_prefix= self.config["line_statement_prefix"]
       self.initial_state = None
       self.quiet = False
       self.setup()
       self.class_name = "Test_Class"
       JINJA_ENVIRONMENT.line_statement_prefix = self.line_statement_prefix

    def setup( self ):
       self.any_state  = None
       self.any_state_id  = None
       self.boolean_variables = []
       self.id_to_state = {}
       self.nodes = []
       self.state_list = []
       self.trans_funcs = set()
       self.edges = []
       self.initial_state = None

    def parse_file(self, filename='Monster.jff'):
       self.class_name = os.path.split(filename)[1].split(".")[0]
       self.setup()
       if not self.class_name:
           self.class_name = filename.split(".")[0]
       try:
           self.parse_xml_file(filename)
       except Exception as e:
           self.parse_json_file( filename )
       if not self.initial_state: 
           self.initial_state = self.state_list[0]
       self.setup_functions()

    def setup_functions( self ):
       self.defined_funcs   = set([t.func  for t in self.state_list if t.func ])
       self.delay_variables = set([t for t in self.state_list if t.delay ])
       # print (self.delay_variables)
       # If the FSM is an MDP, prepare the random logic
       if self.fsm_type == mdp: 
           self.setup_markov_chain()

    def load_config( self, config_file ):
       json_file = open(config_file)
       self._config = json.load(json_file)
       mode = self._config["mode"]
       self.set_mode(mode)
       json_file.close()

    def set_mode( self, mode ):
       self.mode = mode
       self.config = self._config["modes"][mode]

    def is_hlsm( self ): 
        return self.fsm_type == hlsm

    def is_mdp( self ): 
        return self.fsm_type == mdp

    def quiet_mode(self):
        self.quiet = True

    def parse_json_file( self, filename ):
        f = open( filename )
        raw_string = (f.read()[3:]) 
        f.close()
        d = json.loads( raw_string )
        self.parse_json( d )

    def parse_json( self, d ):
        self.fsm_type = hlsm
        for node_dict in d["nodes"]:
            node = JSONNode( node_dict )
            self.add_state( node, node.id )
            if node_dict["initial"]:
                self.initial_state = node
        for edge_dict in d["edges"]:
            #print(node)
            edge = JSONEdgeParser( edge_dict, self )
            self.add_transition(edge)

    def add_transition( self, transition ):
        if transition.should_produce_new_function and transition.func:
           self.trans_funcs.add(transition.func)
        self.edges.append(transition)

    def add_state( self, state, state_id ):
        self.id_to_state[state_id] = state
        if state.name == "any": 
            self.any_state = state
            self.any_state_id = state_id 
        else: 
            self.state_list.append( state )

    def parse_xml_file(self,filename):
        tree = ET.parse(filename)
        root = tree.getroot() 
        self.fsm = root.find("automaton")
        self.fsm_type = root.find("type").text
        self.parse_xml()

    def parse_xml(self):
        for xml_node in self.fsm:
            if xml_node.tag == "state":
                node = XMLNode(xml_node)
                state_id = xml_node.attrib["id"]
                self.add_state( node, state_id )
            if xml_node.find("initial") is not None: 
                self.initial_state = node
            if xml_node.tag == "transition":
                e = XMLEdgeParser( xml_node, self )
                self.add_transition(e)

    def setup_markov_chain(self):        
        states = self.state_list[:]
        if self.any_state: states.append( self.any_state ) 
        for s in states:
            for t in s.transitions:
                s.transitions[t].setup_markov_edge()
        if self.any_state:  
            del self.id_to_state[self.any_state_id]


    def write_to_file(self, filename=None):
        # Create a file stream
        if filename:
            file_stream = open(filename, 'w+') 
        elif self.is_mdp() and mdp_ext_key in self.config:
            file_stream = open(self.class_name + self.config[mdp_ext_key] , 'w')
        else:
            file_stream = open(self.class_name + self.config["file_ext"] , 'w')
        # Determine rendering method
        if self.mode == "Dot":
            output = self.render_dot()
        else:
            output = self.render_jinja()
        file_stream.write( output )
        file_stream.close()

    def render_dot(self):
        from graphviz import Digraph
        dot = Digraph( comment=self.class_name )
        node_fmt = "node_%s"
        for node in self.state_list:
            nid = node_fmt % node.id 
            dot.node( nid, node.name )
        for edge in self.edges:
            fid = node_fmt % edge.orig.id
            tid = node_fmt % edge.to.id
            func = edge.raw_func if edge.raw_func is not None else "-"
            if edge.prob:
                func += ", p = {0:.2f}".format(edge.prob)
            dot.edge( fid, tid, label=func )
        if self.initial_state:
            nid = node_fmt % self.initial_state.id 
            invis = "__invis"
            dot.node( invis, label='', shape='none', width='0', height='0' )
            dot.edge( invis, nid, penwidth='3')
        return dot.source

    def render_jinja(self ):
        if self.initial_state and self.initial_state.name:
            self.initial_state = self.initial_state.name
        self.boolean_variables = [ v for v in set(self.boolean_variables) ]
        state_names = [ s.name for s in self.state_list ]
        enum_names = [ s.name + " = " + str(s.id) for s in self.state_list ]
        jinja_vars = { "class_name"       : self.class_name ,
                   "init_state"           : self.initial_state,
                   "any_state"            : self.any_state,
                   "states"               : self.state_list,
                   "user_state_f"         : self.defined_funcs,
                   "transitions"          : self.trans_funcs,
                   "delays"               : self.delay_variables,
                   "boolean_variables"    : self.boolean_variables, 
                   super_class_key        : self._config[super_class_key],
                   namespace_key          : self._config[namespace_key],
                   class_prefix_key       : self._config[class_prefix_key],
                   function_prefix_key    : self._config[function_prefix_key],
                   "type"                 : self.fsm_type
        }
        template_file = self.config["jinja_template"]
        template = JINJA_ENVIRONMENT.get_template(template_file)
        code = str(template.render(jinja_vars))#.encode('ascii', 'ignore'))
        if not self.quiet:
            print(code)
        return code
        
if __name__ == "__main__":
    from time import time, sleep
    from JFlapToCodeConsole import JFlapToCodeConsole
    if len(sys.argv) > 1: 
        file_name = sys.argv[1]
    else:
        file_name = ""

    # Load the settings file
    parser = JFlapParser(config_file=config_file )
    display = JFlapToCodeConsole( parser, file_to_parse=file_name )
    display.start()
    display.join()
