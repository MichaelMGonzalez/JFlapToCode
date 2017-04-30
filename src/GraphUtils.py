import xml.etree.ElementTree as ET
import json
import sys
from Constants import *

DELIMITTER = "#"
NO_FUNC = "NF"
LITERAL_EXPRESSION = "LE"
FUNC = "F:"
DELAY = "D:"

class Node:
    def __init__(self, xml_node):
        self.get_name(xml_node)
        self.id    = xml_node.attrib["id"]
        self.edges = []
        self.func_map = {}
        self.transitions = {}
    def get_name(self, xml_node):
        name  = xml_node.attrib["name"]
        s = len(name)
        nf_s = len(NO_FUNC)
        self.has_func = True
        self.func = None
        self.delay = None
        if DELIMITTER in name:
            state_args = name.split(DELIMITTER)
            name = state_args[0]
            for arg in state_args[1:]:
                if arg == NO_FUNC: self.has_func = False
                elif FUNC  in arg:  self.func  = arg[len(FUNC):]
                elif DELAY in arg:  self.delay = arg[len(DELAY):]
        self.name = name
    def __str__(self):
        rv = self.name + " " + self.id
        return rv
    def __repr__(self):
        return "Node (" + str(self) + ")"
    def get_transition( self, f ):
        #print self.name, f in self.transitions, f
        if f not in self.transitions: self.transitions[f] = Transition( f )
        return self.transitions[f]

class Transition:
    def __init__( self, func):
        self.func = func
        self.norm = []
        self.neg  = []
        self.processed_norm = False
        self.processed_neg  = False
    def is_simple( self ):
        rv = len(self.norm) > 0 and len(self.neg) > 0
        #print self.norm, self.neg, rv 
        return not rv
    def get_simple_func( self ):
        f = self.func + "()"
        if not self.norm: return "!" + f
        else: return f
    def get_simple_states( self ):
        if self.norm: return self.norm
        else: return self.neg
    def __str__( self ):
        rv  = "Transition Function: " + self.func + nl
        rv += "Normal Transition leads to: " + str( self.norm ) + nl
        rv += "Negated Transition leads to: " + str( self.neg) + nl
        return rv
    def __repr__( self): return str(self)
    def process_list( self, l ):
            tot_p = 0.0
            prev_p = 0
            l.sort( ) 
            # Calculate total probablity
            for p,n in l: 
                tot_p += p
            for elem in l:
                # Save probablity
                elem.append( elem[0] / tot_p ) 
                # Set cumlative probability
                elem[0] = elem[2] + prev_p
                # Save previous
                prev_p = elem[0]
    def prepare( self ):
        if self.norm and not self.processed_norm: 
            self.process_list( self.norm )
            self.processed_norm = True
        if self.neg and not self.processed_neg:
            self.process_list( self.neg  ) 
            self.processed_neg = True

class ParseEdge:
    def __init__(self, xml_node, parser):
        states = parser.state_map
        self.orig  = states[xml_node.find("from").text]
        self.to    = states[xml_node.find("to").text]
        self.func  = xml_node.find("read")
        self.should_produce_new_function = True
        self.neg   = ""
        #print(self.func.text)
        if self.func.text is not None: 
            self.func = self.func.text[:]
        else: 
            self.func = ""
        
        is_transition_func_negated = self.parse_function_flags()
        if self.should_produce_new_function and self.func:
            self.func += "()"
        self.transition = self.orig.get_transition( self.func )
        # Regular HLSM
        if parser.is_hlsm():
            if is_transition_func_negated: 
                self.transition.neg = self.to.name
            else: 
                self.transition.norm = self.to.name
        # Treat mealy machines as MDP
        elif parser.is_mdp(): 
            transition_probability = float(xml_node.find("transout").text)
            transition_pair =  [ transition_probability, self.to.name ]
            if is_transition_func_negated:
                 self.transition.neg.append( transition_pair)
            else: 
                 self.transition.norm.append( transition_pair )
    def parse_function_flags( self ):
        is_transition_func_negated = False
        # Check to see if the function name is negated
        if self.func and self.func[0] == "!": 
            self.func = self.func[1:]
            self.neg  = "!"
            is_transition_func_negated = True
        # See if any additional flags are on the function name
        if DELIMITTER in self.func:
            transition_args = self.func.split(DELIMITTER)
            self.func = transition_args[0]
            for arg in transition_args[1:]:
                if arg == LITERAL_EXPRESSION:
                    self.should_produce_new_function = False
        return is_transition_func_negated

    def __str__(self):
        rv = str(self.orig.name) + " & " + self.func + " -> " + str(self.to)
        return rv
    def __repr__(self):
        return "Edge(" + str(self) + ")"

