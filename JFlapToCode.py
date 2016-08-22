import xml.etree.ElementTree as ET
import json
import sys
import jinja2
import os
from sets import Set
from Constants import *
from GraphUtils import *
from CodeWriter import *

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader( templates_dir ))

class JFlapParser:
    def __init__(self, config_file=None, file_name='Monster.jff'):
       self.load_config( config_file )
       self.class_name = os.path.split(file_name)[1].split(".")[0]
       if not self.class_name:
           self.class_name = file_name.split(".")[0]
       tree = ET.parse(file_name)
       root = tree.getroot() 
       self.fsm = root.find("automaton")
       self.fsm_type = root.find("type").text
       self.init = None
       self.find_states()
       self.defined_funcs = Set([t.func for t in self.states if t.func ])
       # If the FSM is an MDP, prepare the random logic
       if self.fsm_type == mdp: self.prepare()

    def load_config( self, config_file ):
       json_file = open(config_file)
       config = json.load(json_file)
       mode = config["mode"]
       self.config = config["modes"][mode]
       json_file.close()

    def is_hlsm( self ): return self.fsm_type == hlsm

    def is_mdp( self ): return self.fsm_type == mdp

    def find_states(self):
        self.state_map = {}
        self.states = []
        self.trans_funcs = Set()
        for node in self.fsm:
            if node.tag == "state":
                n = Node(node)
                self.state_map[node.attrib["id"]] = n
                self.states.append( n )
                if node.find("initial") is not None: self.init = n.name
            if node.tag == "transition":
                e = ParseEdge( node, self )
                self.trans_funcs.add(e.func)

    def prepare(self):        
        for s in self.states:
            for t in s.transitions:
                s.transitions[t].prepare()

    def dump_to_file(self):
        if self.is_hlsm():
            f = open(self.class_name + self.config["file_ext"] , 'w')
        elif self.is_mdp():
            f = open(self.class_name + self.config["mdp_file_ext"] , 'w')
        state_names = [ s.name for s in self.states ]
        enum_names = [ s.name + " = " + str(s.id) for s in self.states ]
        jinja_vars = { "class_name" : self.class_name ,
                   "init_state"      : self.init,
                   "states"          : self.states,
                   "user_state_f"    : self.defined_funcs,
                   "transitions"     : self.trans_funcs,
                   "type"            : self.fsm_type
        }
	template_file = self.config["jinja_template"]
        template = JINJA_ENVIRONMENT.get_template(template_file)
        code = template.render(jinja_vars).encode('ascii', 'ignore')
        print code
        f.write(code)
        f.close()


    
        
if __name__ == "__main__":
    # Load the settings file
    config = json.load( open( config_file ) )
    # If no command line argument is passed
    if len(sys.argv) < 2:
        if "file_to_process" in config:
            file_name = slash.join(config["file_to_process"])
        else:
            print "What state machine would you like to process?"
            file_name = raw_input(">> ")
    # Take the file passed on from the command line
    else: file_name = sys.argv[1]
    parser = JFlapParser(config_file=config_file, file_name=file_name)
    parser.dump_to_file()
