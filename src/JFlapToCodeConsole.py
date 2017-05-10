from JFlapToCodeConsoleAbstractHLSM import JFlapToCodeConsoleAbstractFSM
import sys
import os
import json
from Constants import *
from time import sleep
from threading import Thread

if sys.version == '3':
    raw_input = input
if sys.version[0] =='2':
    input = raw_input
input_carrot = "> "
run_key = "r"
line_size = 80
def print_header( w ):
    n = line_size - len(w)
    if n > 0:
        padding = int((n-1)/2) * " "
    body = "|%s%s%s|" % (padding, w, padding)
    edge = "-" * len(body)
    print (edge)
    print (body)
    print (edge)
    print('\n')
class ParallelReader( Thread ):
    def __init__(self):
        Thread.__init__(self)
        self.buf = []
    def run( self ):
        self.buf = sys.stdin.readline()
class Option():
    def __init__(self, text, func=lambda x: None ):
        self.text = text
        self.func = func
    def display(self, button):
        txt = " [%s]  -   %s" % (button, self.text)
        print(txt)
    def __call__( self, *args, **kwargs ):
        self.func( *args, **kwargs )
class JFlapToCodeConsole( JFlapToCodeConsoleAbstractFSM ):
    def __init__( self, parser, file_to_parse = "" ):
        self.parser = parser
        self.reader = ParallelReader()
        self.anim_chars = [ '>', '^', '<', '^' ]
        self.file_to_parse = file_to_parse
        self.anim_idx = 0
        self.ready_to_parse = False
        self.mode_options = { "m" : Option( "Change mode", func=self.set_mode  ),
                              "p" : Option( "Set file to parse", func=self.set_file_to_parse ),
                              "s" : Option( "Set the parent class for generated FSM", func=self.set_super_class),
                              "k" : Option( "Set keywords prefixing class declaration", func=self.set_class_prefix),
                              "f" : Option( "Set keyword prededing functions", func=self.set_func_prefix),
                              "n" : Option( "Set the namespace for generated FSM", func=self.set_namespace),
                              "r" : Option( "Parse Input file", func=self.try_parse_file),
                              "x" : Option( "Exit", func=self.quit)
                            }
        JFlapToCodeConsoleAbstractFSM.__init__(self)
    def try_parse_file( self ):
        if self.file_to_parse:
            self.ready_to_parse = True
        else:
            self.set_file_to_parse()
    def set_mode( self ):
        self.clear_all()
        print_header( "Enter the new translation mode")
        config = self.parser._config
        modes = [ k for k in config['modes'].keys() ]
        modes = [ (i, mode) for i,mode in enumerate(modes) ]
        options = list( [ (str(i), Option( mode, func=None)) for (i,mode) in modes] )
        for i,op in options:
            op.display(i)
        new_mode = input( input_carrot )
        try:
            n = int(new_mode)
            if n < len(modes) and n >= 0:
                new_mode = modes[n][1]
                config['mode'] = new_mode 
                self.parser.set_mode( new_mode )
                self.write_to_config_file( config ) 
        except Exception:
            pass
    def set_class_prefix( self):
        self.set_key(class_prefix_key)
    def set_func_prefix( self):
        self.set_key(function_prefix_key)
    def set_super_class( self ):
        self.set_key( super_class_key )
    def set_namespace( self ):
        self.set_key( namespace_key )
    def set_key( self, key):
        self.clear_all()
        print_header( "Enter the name value for %s" % key )
        userinput = input( input_carrot )
        config = self.parser._config
        config[key] = userinput 
        self.write_to_config_file( config ) 
    def set_file_to_parse( self ):
        self.clear_all()
        print_header( "Enter the file name to translate")
        self.file_to_parse = input( input_carrot )
    def write_prompt( self ):
        sys.stdout.write(">: ")
        sys.stdout.flush()
    def execute_action_init(self):
        print_header ("Welcome to JFlap to code!")
        print ("Press %s & enter to parse immediately or any other key to enter config!" % run_key)
        if self.file_to_parse:
            self.reader.start()
        #self.write_prompt()
    def execute_action_prompt_auto(self):
        pass
    def execute_action_automate(self):
        print_header( "Translating..." )
        self.parser.parse(self.file_to_parse)
        self.parser.write_to_file()
    def get_config_value(self, config, key):
        rv = config[key]
        rv = rv if rv else "N/A"
        return rv

    def execute_action_display_config(self):
        self.clear_all()
        config = self.parser._config
        super_class = self.get_config_value( config, super_class_key ) 
        function_prefix = self.get_config_value( config, function_prefix_key) 
        namespace = self.get_config_value(config, namespace_key) 
        class_keyword_prefix = self.get_config_value(config, class_prefix_key)
        in_file = self.file_to_parse if self.file_to_parse else "N/A"
        print_header( "Current Configuration")
        print( "Translation Mode: %s" % config['mode' ] ) 
        print( "Parent Class: %s" % super_class) 
        print( "Class Keyword Prefix: %s" % class_keyword_prefix ) 
        print( "Function Prefix: %s" % function_prefix ) 
        print( "Namespace: %s" % namespace) 
        print( "File to Translate: %s" % in_file ) 
        print('\n')
        print( "What would you like to do?" )
        selection = ""
        while selection not in self.mode_options:
            for button, option in self.mode_options.items():
                option.display( button )
            try:
                selection = input(input_carrot) 
                selection = selection.lower()
                if selection in self.mode_options:
                    self.mode_options[selection]()
                else:
                    print ("Unknown option: " +  selection)
            except EOFError as e:
                print (e)

    def execute_action_console_animation(self):
        sys.stdout.write( 2 * '\b' )
        sys.stdout.write( self.anim_chars[ self.anim_idx ] + ":" )
        sys.stdout.flush()
        self.anim_idx += 1
        self.anim_idx %= len( self.anim_chars )
    # Transitional Logic Functions
    def should_auto_continue(self):
        timeout = self.get_time_since_start() > 2
        just_parse = self.reader.buf and self.reader.buf[0] == run_key
        return timeout or just_parse
    def should_refresh_anim(self):
        return self.get_time_in_state() > .1
    def enter_config(self):
        return self.reader.buf and self.reader.buf[0] != run_key
    def execute_action_exit(self):
        exit_time = 1
        print( "Translation complete!" )
        print( "JFlapToCode will close in %d seconds" % exit_time )
        sleep( exit_time )
        self.is_running = False
        self.quit()
    def has_file_to_parse(self):
        return  self.file_to_parse
    def clear_all( self ):
        os.system('cls' if os.name == 'nt' else 'clear')
    def should_parse(self):
        return self.ready_to_parse
    def write_to_config_file( self, config ):
        file_descriptor = open( config_file, 'w+' )
        json.dump( config, file_descriptor, indent=4 )
        file_descriptor.close()
    def quit(self):
        sys.exit()


if __name__ == '__main__':
    prog = JFlapToCodeConsole()
    prog.start()
    prog.join()
