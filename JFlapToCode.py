import xml.etree.ElementTree as ET
import json
import sys
from sets import Set


nl = "\n"
tab = "    "
enum = "State"
state_action = "ExecuteAction"
config_file = "settings.json"
def indent( body ):
    return [ tab + l for l in body ]
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
       self.setup_states()
    def setup_states(self):
        self.states      = {}
        self.transitions = []
        self.trans_funcs = Set()
        for node in self.fsm:
            if node.tag == "state":
                n = Node(node)
                self.states[node.attrib["id"]] = n
                if node.find("initial") is not None:
                    self.init = n.name
                    #print self.init
            if node.tag == "transition":
                e = Edge( node, self.states)
                self.transitions.append(e)
                self.trans_funcs.add(e.func)
                
                
                
    def make_c_sharp(self):
        c = self.config
        rv = [ c["before_include"] + l + c["after_include"] for l in c["libs"] ]
        rv += [c["class_header_bef"] + self.class_name +  c["class_header_aft"]]
        b_f = c["before_func"]
        a_f = c["after_func"]
        
        body = ["protected enum " + enum + " { " + ", ".join([ self.states[k].name for k in self.states ]) + " }"]
        body.append( "protected State state = " + enum + "." + self.init +";")
        # Define the body
        
        start_body   = ["StartCoroutine(FSMThread());"] 
        #start_method = ["protected override void RunFSM() {"] + indent(start_body) + ["}"]
        start_method = []
        run_fsm_body   = ["while(true) { "] 
        run_fsm_body.append("State prevState = state;")
        run_fsm_body.append("// This is the state action logic")
        run_fsm_body.append("switch(state) {")
        
        for state in [ self.states[k] for k in self.states ]:
            run_fsm_body.append("case " + enum + "." + state.name + ":")
            run_fsm_body.append(tab + "yield return " + state_action + state.name + "();")
            run_fsm_body.append(tab + "break;")
        run_fsm_body.append("}")
        run_fsm_body.append("// This is the state transition logic")
        run_fsm_body.append("switch(state) {")
        for state in [ self.states[k] for k in self.states ]:
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
        eos  = c["end_stub_var"]
        eosf = c["end_stub_func"]
        abstract_funcs = [ c["before_stub"] + "bool " + f + eosf for f in self.trans_funcs ]
        abstract_funcs += [ c["before_stub"] + "IEnumerator " + state_action + s.name + eosf  for s in [ self.states[k] for k in self.states ] ]

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
    print parser.make_c_sharp()