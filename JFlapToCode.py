import xml.etree.ElementTree as ET
import json
import sys
from sets import Set
from Constants import *
from GraphUtils import *
from CodeWriter import *

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
        self.trans_funcs = Set()
        for node in self.fsm:
            if node.tag == "state":
                n = Node(node)
                self.state_map[node.attrib["id"]] = n
                self.states.append( n )
                if node.find("initial") is not None: self.init = n.name
            if node.tag == "transition":
                e = Edge( node, self )
                self.trans_funcs.add(e.func)
                
    def dump_to_file(self):
        f = open(self.class_name + self.config["file_ext"] , 'w')
        f.write( self.make_code() )
        f.close()

    def make_code(self):
        c = self.config
        # End of statement
        eos = c["end_var"]
        eq = c["assign_var"]
        indent_level = 1 # Dynamically changing indentation level
        writer = CodeWriter( c )
        if "before_all" in c: 
            for l in c["before_all"]: writer.write(l,0)
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
        # Create state variables
        state_var = "state"
        prev_state_var = "prevState"
        time_var = c["time_var"]
        state_var_decl = c["state_var_type"] + state_var
        prev_var_decl = c["state_var_type"] + prev_state_var + eq + state_var
        if self.init: state_var_decl +=  eq + self.init.upper() 
        if "time_type" in c: 
            writer.write( c["time_type" ] + time_var + eq + "0" + eos, 1)
        writer.write( state_var_decl + eos, 1)
        writer.write( prev_var_decl  + eos, 1)
        # Begin optional sections
        # If there's a wrapper function, then make it
        if wrapper_function in c:
            writer.write( c[wrapper_function], indent_level )
            indent_level += 1
        # If there's an infinite state loop desired, then make it
        if inf_loop in c:
            writer.write( c[inf_loop], indent_level )
            indent_level += 1

        writer.write( prev_state_var + eq + state_var + eos, indent_level)
        # Handle state action logic
        writer.write_comment("The following switch statement handles the HLSM's state action logic", indent_level)
        writer.write( c["start_switch"], indent_level )
        for s in self.states:
            case =  c["begin_case"] + s.name.upper() + c["after_case"] 
            writer.write( case, indent_level + 1 )
            func = state_action + s.name + c["end_func"] 
            if "before_action" in c: func = c["before_action"] + func
            writer.write(func, indent_level + 2 )
            if "end_case" in c: writer.write( c["end_case"], indent_level + 2 )
        writer.write( c["end_switch"], indent_level )
        # Handle transition logic
        writer.write_comment("The following switch statement handles the HLSM's state transition logic", indent_level)
        writer.write( c["start_switch"], indent_level )
        for s in self.states:
            case =  c["begin_case"] + s.name.upper() + c["after_case"] 
            writer.write( case, indent_level + 1 )
            for func in s.transitions:
                transition = s.transitions[func]
                if transition.is_simple():
                    condition = transition.get_simple_func()
                    assign_state = state_var + eq + transition.get_simple_states() + eos
                    writer.write_cond(indent_level + 2, condition, assign_state)
                else:
                    # First cond
                    condition = func + "()"
                    assign_state = state_var + eq + transition.norm + eos
                    writer.write_cond(indent_level + 2, condition, assign_state )
                    # Second cond
                    writer.write_else( indent_level + 2, state_var + eq + transition.neg + eos)
            if "end_case" in c: writer.write( c["end_case"], indent_level + 2 )
        writer.write( c["end_switch"], indent_level )

        # Write any extra functions at the end of the state loop
        if "run_at_end" in c:
            for l in c["run_at_end"]: writer.write( l, indent_level )

        # Set transition time
        set_time = c["time_var"] + eq + c["time_function"] + c["end_var"]
        writer.write_cond( indent_level, prev_state_var + "!=" + state_var, set_time) 

        # End optional sections
        # End infinite loop 
        if inf_loop in c: writer.write( c["after_func"], indent_level - 1 )
        # End wrapper function
        if wrapper_function in c: writer.write( c["after_func"], 1 )

        # Write state action function stubs
        for s in self.states:
            line = c["state_function"] + state_action + s.name + c["end_func"]
            writer.write( line, 1)
        # Write state transtion function stubs
        for func in self.trans_funcs:
            line = c["transition_function"] + func + c["end_func"]
            writer.write( line, 1)
        # End class 
        writer.write(c["class_end"],0)
        if "after_all" in c:
            for l in c["after_all"]: writer.write(l,0)
        return writer.dump()
        
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
    parser = JFlapParser(config_file=config["default_config"], file_name=file_name)
    print parser.make_code()
    #parser.dump_to_file()