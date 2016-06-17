import xml.etree.ElementTree as ET
import json
import sys
from sets import Set
from Constants import *
from GraphUtils import *

class CodeWriter:
    def __init__(self, config):
        self.config = config
        self.indent = config["indent"] 
        self.comment = config["comment"]
        self.code = []
    def write(self, line, indent_level):
        indent = indent_level * self.indent
        self.code.append( indent + line )
    def write_comment( self, line, indent_level ):
        l_max = 80 - len( self.comment )
        acc = []
        for l in range(0, (len(line) / l_max) + 1 ):
            acc.append( self.comment + line[l * l_max:(l+1) * l_max ] )
        self.write( nl.join(acc), indent_level )
    def write_cond(self, indent, condition, body):
        self.write_cond_body(self.config["begin_cond"] + condition + self.config["after_cond"], indent, body)
    def write_else( self, indent, body):
        self.write_cond_body(self.config["else"], indent, body)
    def write_cond_body( self, cond, indent, body ):  
        c = self.config
        self.write( cond, indent )
        if type(body) is unicode or type(body) is str: body = [body]
        for l in body: self.write(l, indent + 1 )
        if "end_cond" in c: self.write( c["end_cond"], indent)
    def dump( self ):
        return nl.join( self.code )
    def start_switch( self, indent_level ):
        self.write( self.config["start_switch"], indent_level )
    def end_switch( self, indent_level):
        self.write( self.config["end_switch"], indent_level )
    def begin_case( self, indent_level, case ):
        self.write( self.config["begin_case"] + case + self.config["after_case"], indent_level ) 
    def end_case( self, indent_level):
        if "end_case" in self.config: self.write( self.config["end_case"], indent_level  )

