import xml.etree.ElementTree as ET
import json
import sys
from sets import Set
from Constants import *

class Node:
    def __init__(self, xml_node):
        self.name  = xml_node.attrib["name"]
        self.id    = xml_node.attrib["id"]
        self.edges = []
    def __str__(self):
        rv = self.name + " " + self.id
        return rv
    def __repr__(self):
        return "Node (" + str(self) + ")"
    def add_edge(self, edge):
        pass

class Edge:
    def __init__(self, xml_node, states):
        self.orig  = states[xml_node.find("from").text]
        self.to    = states[xml_node.find("to").text]
        self.func  = xml_node.find("read").text
        self.neg   = False
        if self.func[0] == "!": 
            self.func = self.func[1:]
            self.neg  = True
        self.orig.edges.append(self)
    def __str__(self):
        rv = str(self.orig.name) + " & " + self.func + " -> " + str(self.to)
        return rv
    def __repr__(self):
        return "Edge(" + str(self) + ")"

class CodeWriter:
    def __init__(self, indent, comment):
        self.indent =  indent 
        self.code = []
        self.comment = comment
    def write(self, line, indent_level):
        indent = indent_level * self.indent
        self.code.append( indent + line )
    def write_comment( self, line, indent_level ):
        self.write( self.comment + line, indent_level )
    def dump( self ):
        return nl.join( self.code )

class JFlapParser:
    def __init__(self, config_file="Unity.json", file_name='Monster.jff'):
       json_file = open(config_file)
       self.config = json.load(json_file)
       json_file.close()
       self.class_name = file_name.split(".")[0]
       tree = ET.parse(file_name)
       root = tree.getroot() 
       self.fsm = root.find("automaton")
       self.fsm_type = root.find("type").text
       self.init = None
       self.setup_states()
    def setup_states(self):
        self.state_map = {}
        self.states = []
        self.transitions = []
        self.trans_funcs = Set()
        for node in self.fsm:
            if node.tag == "state":
                n = Node(node)
                self.state_map[node.attrib["id"]] = n
                self.states.append( n )
                if node.find("initial") is not None:
                    self.init = n.name
                    #print self.init
            if node.tag == "transition":
                e = Edge( node, self.state_map)
                self.transitions.append(e)
                self.trans_funcs.add(e.func)
                
                
                
    def make_code(self):
        c = self.config
        indent_level = 1 # Dynamically changing indentation level
        writer = CodeWriter( c["indent"], c["comment"] )
        # Include required libraries if any
        for line in c["libs"]:
            writer.write( c["before_include"] + line +  c["after_include"], 0 ) 
        # Start class definition
        writer.write(c["class_header_bef"] + self.class_name + c["class_header_aft"], 0)
        # Declare state constants
        for state in self.states:
            line = c["before_const"] + str(state.name).upper() + c["const_assignment"] 
            line += str(state.id) + c["after_const"]
            writer.write(line,1)
        # Create state variable
        state_var = c["state_var_type"] + "state" 
        if self.init: state_var +=  c["assign_var"] + self.init.upper() 
        writer.write( state_var + c["end_var"], 1)
        # Begin optional sections
        # If there's a wrapper function, then make it
        if wrapper_function in c:
            writer.write( c[wrapper_function], indent_level )
            indent_level += 1
        # If there's an infinite state loop desired, then make it
        if inf_loop in c:
            writer.write( c[inf_loop], indent_level )
            indent_level += 1

        # Handle action logic
        writer.write( c["start_switch"], indent_level )
        for s in self.states:
            case =  c["begin_case"] + s.name.upper() + c["after_case"] 
            writer.write( case, indent_level + 1 )
            f = state_action + s.name + c["end_func"] 
            if "before_action" in c: f = c["before_action"] + f
            writer.write(f, indent_level + 2 )
            if "end_case" in c: writer.write( c["end_case"], indent_level + 2 )
        writer.write( c["end_switch"], indent_level )


        # End optional sections
        # End infinite loop 
        if inf_loop in c:
            writer.write( c["after_func"], indent_level - 1 )
        # End wrapper function
        if wrapper_function in c:
            writer.write( c["after_func"], 1 )


        # End class 
        writer.write(c["class_end"],0)
        return writer.dump()
    def make_c_sharp(self):
        c = self.config
        rv = [ c["before_include"] + l + c["after_include"] for l in c["libs"] ]
        rv += [c["class_header_bef"] + self.class_name +  c["class_header_aft"]]
        b_f = c["before_func"]
        a_f = c["after_func"]
        
        body = ["protected enum " + enum + " { " + ", ".join([ self.state_map[k].name for k in self.state_map ]) + " }"]
        body.append( "protected State state = " + enum + "." + self.init +";")
        # Define the body
        
        start_body   = ["StartCoroutine(FSMThread());"] 
        #start_method = ["protected override void RunFSM() {"] + indent(start_body) + ["}"]
        start_method = []
        run_fsm_body   = ["while(true) { "] 
        run_fsm_body.append("State prevState = state;")
        run_fsm_body.append("// This is the state action logic")
        run_fsm_body.append("switch(state) {")
        
        for state in [ self.state_map[k] for k in self.state_map ]:
            run_fsm_body.append("case " + enum + "." + state.name + ":")
            run_fsm_body.append(tab + "yield return " + state_action + state.name + "();")
            run_fsm_body.append(tab + "break;")
        run_fsm_body.append("}")
        run_fsm_body.append("// This is the state transition logic")
        run_fsm_body.append("switch(state) {")
        for state in [ self.state_map[k] for k in self.state_map ]:
            run_fsm_body.append("case " + enum + "." + state.name + ":" )
            for transition in state.edges:
                t_func = transition.func + "()"
                if transition.neg: t_func = "!" + t_func
                run_fsm_body.append(tab + "if( " + t_func + " )")
                run_fsm_body.append(2 * tab + "state = " + enum + "." + transition.to.name + ";" )
            run_fsm_body.append(tab + "break;")
        run_fsm_body.append("}")
        
        run_fsm_body.append("yield return new WaitForSeconds( delayRate );")
        run_fsm_body.append("if( prevState != state ) transitionedAt = Time.time;")
        run_fsm_body = [run_fsm_body[0]] + indent(run_fsm_body[1:]) + ["}"]
        run_fsm_method = ["protected override IEnumerator FSMThread( float delayRate ) {"] + indent(run_fsm_body) + ["}"]
        
        # End of stub
        eos  = c["end_var"]
        eosf = c["end_func"]
        abstract_funcs = [ c["before_stub"] + "bool " + f + eosf for f in self.trans_funcs ]
        abstract_funcs += [ c["before_stub"] + "IEnumerator " + state_action + s.name + eosf  for s in [ self.state_map[k] for k in self.state_map ] ]

        body += start_method + run_fsm_method + abstract_funcs
        rv.append( nl.join([ tab + l for l in body] ) )
        rv.append("}" )
        rv = nl.join(rv)
        out_cs = open(self.class_name + c["file_ext"], "w")
        out_cs.write( rv )
        out_cs.close()
        return rv
if __name__ == "__main__":
    # Load the settings file
    config = json.load( open( config_file ) )
    # If no command line argument is passed
    if len(sys.argv) < 2:
        if "file_to_process" in config:
            file_name = config["file_to_process"]
        else:
            print "What state machine would you like to process?"
            file_name = raw_input(">> ")
    # Take the file passed on from the command line
    else: file_name = sys.argv[1]
    parser = JFlapParser(file_name=file_name)
    print parser.make_code()