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
       self.class_name = file_name.split(".")[0].split("\\")[-1]
       tree = ET.parse(file_name)
       root = tree.getroot() 
       self.fsm = root.find("automaton")
       self.fsm_type = root.find("type").text
       self.init = None
       self.find_states()
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
                
    def dump_to_file(self):
        if self.is_hlsm():
            f = open(self.class_name + self.config["file_ext"] , 'w')
        elif self.is_mdp():
            f = open(self.class_name + self.config["mdp_file_ext"] , 'w')
        f.write( self.make_code() )
        f.close()

    def get_common_vars(self):
        c = self.config
        return c, c["end_var"], c["assign_var"]

    def write_headers( self, writer ):
        c, eos, eq = self.get_common_vars()
        if "before_all" in c: 
            for l in c["before_all"]: writer.write(l,0)
        # Include required libraries if any
        for line in c["libs"]:
            writer.write( c["before_include"] + line +  c["after_include"], 0 ) 
        # Start class definition
        if self.is_hlsm():
            class_aft = c["class_header_aft"]
        elif self.is_mdp():
            class_aft = c["mdp_class_header_aft"]
        writer.write(c["class_header_bef"] + self.class_name + class_aft, 0)
    def write_state_vars( self, writer ):
        c, eos, eq = self.get_common_vars()
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
        if self.init: state_var_decl +=  eq + self.init.upper() 
        if "time_type" in c: 
            writer.write( c["time_type" ] + time_var + eq + "0" + eos, 1)
        writer.write( state_var_decl + eos, 1)
        return state_var, prev_state_var, time_var

    def create_optional_sections( self, writer ):
        c, eos, eq = self.get_common_vars()
        # Dynamically changing indentation level
        indent_level = 1 
        # If there's a wrapper function, then make it
        if wrapper_function in c:
            writer.write( c[wrapper_function], indent_level )
            indent_level += 1
        # If there's an infinite state loop desired, then make it
        if inf_loop in c:
            writer.write( c[inf_loop], indent_level )
            indent_level += 1
        return indent_level
    def create_function_stubs( self, writer ):
        c, eos, eq = self.get_common_vars()
        # Write state action function stubs
        for s in self.states:
            line = c["state_function"] + state_action + s.name + c["end_func"]
            writer.write( line, 1)
        # Write state transtion function stubs
        for func in [ f for f in self.trans_funcs if f != "" ] :
            line = c["transition_function"] + func + c["end_func"]
            writer.write( line, 1)
        # Write on transition function
        if on_trans in c: writer.write( c[on_trans_type]  + c[on_trans ], 1 )

    def create_actions( self, writer, indent_level, state_var ):
        c, eos, eq = self.get_common_vars()
        writer.write_comment("The following switch statement handles the state machine's action logic", indent_level)
        writer.start_switch( indent_level )
        for s in self.states:
            #print "State:", s, s.transitions
            writer.begin_case( indent_level + 1, s.name.upper())
            func = state_action + s.name + c["end_func"] 
            if "before_action" in c: func = c["before_action"] + func
            writer.write(func, indent_level + 2 )
            writer.end_case( indent_level + 2 )
        writer.end_switch( indent_level )

    def get_mdp_body( self, transitions, state_var, rand_var):
        c, eos, eq = self.get_common_vars()
        condition_writer = CodeWriter( self.config )
        i = 0
        for cdf, state, prob in transitions:
            cond = rand_var + " < " + str(cdf) 
            assign_state = state_var + eq + state + eos
            condition_writer.write_comment("Probability of transition: " + str(prob * 100) + "%", 0 )
            if i == 0: condition_writer.write_cond( 0, cond, assign_state )
            else: condition_writer.write_else_if( 0, cond, assign_state )
            i += 1
        return condition_writer.code

    def create_mdp_transitions( self, writer, indent_level, state_var ):
        c, eos, eq = self.get_common_vars()
        rand_var  = c["random_var"]
        rand_f    = c["random_f"]
        rand_type = c["random_type"]

        writer.write_comment( "Get a uniform random number for MDP transitions", indent_level) 
        writer.write( rand_type + rand_var + eq + rand_f + eos, indent_level )
        writer.write_comment("The following switch statement handles the MDP's state transition logic", indent_level)
        writer.start_switch( indent_level )
        for s in self.states:
            writer.begin_case( indent_level + 1, s.name.upper())
            for func in s.transitions:
                transition = s.transitions[func]
                transition.prepare()
                if transition.is_simple():
                    condition = transition.get_simple_func()
                    code = self.get_mdp_body( transition.get_simple_states(), state_var, rand_var )
                    writer.write_cond(indent_level + 2, condition, code )
                else:
                    # First cond
                    condition = func + "()"
                    code = self.get_mdp_body( transition.norm, state_var, rand_var )
                    writer.write_cond(indent_level + 2, condition, code)
                    # Second cond
                    code = self.get_mdp_body( transition.neg, state_var, rand_var )
                    writer.write_else( indent_level + 2, code) 
            writer.end_case( indent_level + 2 )
        writer.end_switch( indent_level )
    def create_hlsm_transitions( self, writer, indent_level, state_var ):
        c, eos, eq = self.get_common_vars()
        # Handle transition logic
        writer.write_comment("The following switch statement handles the HLSM's state transition logic", indent_level)
        writer.start_switch( indent_level )
        for s in self.states:
            writer.begin_case( indent_level + 1, s.name.upper())
            for func in s.transitions:
                transition = s.transitions[func]
                if transition.is_simple():
                    condition = transition.get_simple_func()
                    assign_state = state_var + eq + transition.get_simple_states() + eos
                    if transition.get_simple_func() == "()": writer.write(assign_state, indent_level + 2) 
                    else: writer.write_cond(indent_level + 2, condition, assign_state)
                else:
                    # First cond
                    condition = func + "()"
                    assign_state = state_var + eq + transition.norm + eos
                    writer.write_cond(indent_level + 2, condition, assign_state )
                    # Second cond
                    writer.write_else( indent_level + 2, state_var + eq + transition.neg + eos)
            writer.end_case( indent_level + 2 )
        writer.end_switch( indent_level )


    def create_footer( self, writer ):
        # End class 
        c, eos, eq = self.get_common_vars()
        writer.write(c["class_end"],0)
        if "after_all" in c:
            for l in c["after_all"]: writer.write(l,0)

    def make_code(self):
        c, eos, eq = self.get_common_vars()
        writer = CodeWriter( c )
        # Write out the headers
        self.write_headers( writer )
        # Create the state variables
        state_var, prev_state_var, time_var = self.write_state_vars( writer )
        # Begin optional sections
        indent_level = self.create_optional_sections( writer )

        prev_var_decl = c["prev_var_type"] + prev_state_var + eq + state_var
        writer.write( prev_var_decl  + eos, indent_level)

        # Handle state action logic
        self.create_actions( writer, indent_level, state_var )

        # Create the transtion logic
        if self.is_hlsm():
            self.create_hlsm_transitions( writer, indent_level, state_var )
        elif self.is_mdp():
            self.create_mdp_transitions( writer, indent_level, state_var )


        # Write any extra functions at the end of the state loop
        if "run_at_end" in c:
            for l in c["run_at_end"]: writer.write( l, indent_level )

        # Set transition time
        transition_body = c["time_var"] + eq + c["time_function"] + c["end_var"]
        if on_trans in c: transition_body = [ transition_body, c[on_trans ] ] 
        writer.write_cond( indent_level, prev_state_var + "!=" + state_var, transition_body) 

        # End optional sections
        # End infinite loop 
        if inf_loop in c: writer.write( c["after_func"], indent_level - 1 )
        # End wrapper function
        if wrapper_function in c: writer.write( c["after_func"], 1 )

        self.create_function_stubs( writer )
        self.create_footer( writer )
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
    parser.dump_to_file()