from JFlapToCode import *
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
template = JINJA_ENVIRONMENT.get_template("Python.jinja.py")

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


    state_names = [ s.name for s in parser.states ]
    enum_names = [ s.name + " = " + str(s.id) for s in parser.states ]
    jinja_vars = { "class_name" : parser.class_name ,
                   "init_state" : parser.init,
                   "states"   : parser.states,
                   "transitions" : parser.trans_funcs,
                   "type"        : parser.fsm_type
    }

    f = template.render(jinja_vars).encode('ascii', 'ignore')
    print f
