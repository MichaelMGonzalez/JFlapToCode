import xml.etree.ElementTree as ET
import json
from sets import Set


nl = "\n"
tab = "    "
enum = "State"
state_action = "ExecuteAction"
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
        self.to.edges.append(self)
    def __str__(self):
        rv = str(self.orig.name) + " & " + self.func + " -> " + str(self.to)
        return rv
    def __repr__(self):
        return "Edge(" + str(self) + ")"

class JFlapParser:
    def __init__(self, file_name='Chiaby.jff'):
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
        rv = ["public abstract class " + self.class_name + "_FSM {"]
        
        
        body = ["proetected enum " + enum + " { " + ", ".join([ self.states[k].name for k in self.states ]) + " }"]
        body.append( "State state = " + enum + "." + self.init +";")
        # Define the body
        
        start_body   = ["StartCoroutine(FSMThread());"] 
        start_method = ["protected void RunFSM() {"] + indent(start_body) + ["}"]
        
        run_fsm_body   = ["while(true) { "] 
        run_fsm_body.append("// Put your state action logic here")
        run_fsm_body.append("switch(state) {")
        
        for state in [ self.states[k] for k in self.states ]:
            run_fsm_body.append("case " + enum + "." + state.name + ":" )
            run_fsm_body.append(tab + state_action + state.name + "();")
            run_fsm_body.append(tab + "break;")
        run_fsm_body.append("}")
        run_fsm_body.append("// Put your state transition logic here")
        run_fsm_body.append("switch(state) {")
        for state in [ self.states[k] for k in self.states ]:
            run_fsm_body.append("case " + enum + "." + state.name + ":" )
            for transition in state.edges:
                run_fsm_body.append(tab + "if( " + transition.func + "() )")
                run_fsm_body.append(2 * tab + "state = " + enum + "." + transition.to.name + ";" )
            run_fsm_body.append(tab + "break;")
        run_fsm_body.append("}")
        
        
        run_fsm_body = [run_fsm_body[0]] + indent(run_fsm_body[1:]) + ["}"]
        run_fsm_method = ["IEnumerator FSMThread() {"] + indent(run_fsm_body) + ["}"]
        abstract_funcs = [ "abstract bool " + f + "();" for f in self.trans_funcs ]
        abstract_funcs += [ "abstract void " + state_action + s.name + "();" for s in [ self.states[k] for k in self.states ] ]
        body += start_method + run_fsm_method + abstract_funcs
        rv.append( nl.join([ tab + l for l in body] ) )
        rv.append("}" )
        nl.join(rv)
        out_cs = open(self.class_name)
if __name__ == "__main__":
    parser = JFlapParser()
    print parser.make_c_sharp()