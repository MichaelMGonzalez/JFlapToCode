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
       self.init = None
       self.quiet = False
       self.setup()
       self.class_name = "Test_Class"
       JINJA_ENVIRONMENT.line_statement_prefix = self.line_statement_prefix
    def setup( self ):
       self.any_state  = None
       self.any_state_id  = None
       self.boolean_variables = []
       self.state_map = {}
       self.nodes = []
       self.states = []
       self.trans_funcs = set()
       self.edges = []
       self.init = None
    def parse(self, filename='Monster.jff'):
       self.class_name = os.path.split(filename)[1].split(".")[0]
       self.setup()
       if not self.class_name:
           self.class_name = filename.split(".")[0]
       try:
           tree = ET.parse(filename)
           root = tree.getroot() 
           self.fsm = root.find("automaton")
           self.fsm_type = root.find("type").text
           self.parse_xml()
       except Exception as e:
           self.parse_json_file( filename )
       if not self.init: 
           self.init = self.states[0]
       self.setup_functions()
    def setup_functions( self ):
       self.defined_funcs   = set([t.func  for t in self.states if t.func ])
       self.delay_variables = set([t for t in self.states if t.delay ])
       # print (self.delay_variables)
       # If the FSM is an MDP, prepare the random logic
       if self.fsm_type == mdp: 
           self.prepare()

    def load_config( self, config_file ):
       json_file = open(config_file)
       self._config = json.load(json_file)
       mode = self._config["mode"]
       self.set_mode(mode)
       json_file.close()
    def set_mode( self, mode ):
       self.mode = mode
       self.config = self._config["modes"][mode]

    def is_hlsm( self ): return self.fsm_type == hlsm

    def is_mdp( self ): return self.fsm_type == mdp
    def parse_json_file( self, filename ):
        f = open( filename )
        raw_string = (f.read()[3:] ) 
        f.close()
        d = json.loads( raw_string )
        self.parse_json( d )
    def parse_json( self, d ):
        self.fsm_type = hlsm
        for node_dict in d["nodes"]:
            node = JSONNode( node_dict )
            self.state_map[node.id] = node
            self.states.append( node )
            if node_dict["initial"]:
                self.init = node
        for edge_dict in d["edges"]:
            #print(node)
            edge = JSONEdgeParser( edge_dict, self )
            self.add_edge(edge)

    def add_edge( self, edge ):
        if edge.should_produce_new_function and edge.func:
           self.trans_funcs.add(edge.func)
        self.edges.append(edge)
    def parse_xml(self):
        for node in self.fsm:
            if node.tag == "state":
                n = XMLNode(node)
                sid = node.attrib["id"]
                self.state_map[sid] = n
                if n.name == "any": 
                    self.any_state = n
                    self.any_state_id = sid 
                else: 
                    self.states.append( n )
                if node.find("initial") is not None: self.init = n
            if node.tag == "transition":
                e = XMLEdgeParser( node, self )
                self.add_edge(e)

    def prepare(self):        
        states = self.states[:]
        if self.any_state: states.append( self.any_state ) 
        for s in states:
            for t in s.transitions:
                s.transitions[t].prepare()
        if self.any_state:  
            del self.state_map[self.any_state_id]
    def quiet_mode(self):
        self.quiet = True
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
        for node in self.states:
            nid = node_fmt % node.id 
            dot.node( nid, node.name )
        for edge in self.edges:
            fid = node_fmt % edge.orig.id
            tid = node_fmt % edge.to.id
            func = edge.raw_func if edge.raw_func is not None else "-"
            if edge.prob:
                func += ", p = {0:.2f}".format(edge.prob)
            dot.edge( fid, tid, label=func )
        if self.init:
            nid = node_fmt % self.init.id 
            invis = "__invis"
            dot.node( invis, label='', shape='none', width='0', height='0' )
            dot.edge( invis, nid, penwidth='3')
        return dot.source
    def render_jinja(self ):
        if self.init and self.init.name:
            self.init = self.init.name
        self.boolean_variables = [ v for v in set(self.boolean_variables) ]
        state_names = [ s.name for s in self.states ]
        enum_names = [ s.name + " = " + str(s.id) for s in self.states ]
        jinja_vars = { "class_name"       : self.class_name ,
                   "init_state"           : self.init,
                   "any_state"            : self.any_state,
                   "states"               : self.states,
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
