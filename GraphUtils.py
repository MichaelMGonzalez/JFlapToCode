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
        self.func_map = {}
        self.transitions = {}
    def __str__(self):
        rv = self.name + " " + self.id
        return rv
    def __repr__(self):
        return "Node (" + str(self) + ")"
    def add_edge(self, edge ):
        f = edge.func
        if f not in self.func_map: self.func_map[f] = []
        self.func_map[f].append(edge)
    def get_transition( self, f ):
        #print self.name, f in self.transitions, f
        if f not in self.transitions: self.transitions[f] = Transition( f )
        return self.transitions[f]

class Transition:
    def __init__( self, func):
        self.func = func
        self.norm = []
        self.neg  = []
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
class Edge:
    def __init__(self, xml_node, parser):
        states = parser.state_map
        self.orig  = states[xml_node.find("from").text]
        self.to    = states[xml_node.find("to").text]
        self.func  = xml_node.find("read").text[:]
        self.neg   = ""
        isNegated = False
        if self.func[0] == "!": 
            self.func = self.func[1:]
            self.neg  = "!"
            isNegated = True
        self.transition = self.orig.get_transition( self.func )
        if parser.fsm_type == "fa":
            self.orig.add_edge( self )
            if isNegated: self.transition.neg = self.to.name.upper()
            else: self.transition.norm = self.to.name.upper()
    def __str__(self):
        rv = str(self.orig.name) + " & " + self.func + " -> " + str(self.to)
        return rv
    def __repr__(self):
        return "Edge(" + str(self) + ")"

