import json
from Constants import *


file_stream = open( config_file, "r" ) 
config = json.load( file_stream )
file_stream.close()

print config

def print_available():
    print "You can modify keys: "
    for k in config: print "\t",k

print "What key would you like to modify?"
print_available()
while True:
    key = raw_input("> ")
    if key in config:
        print "The current value of", key, "is:", config[key]
        print "What would you like the new value to be?"
        value = raw_input("> ")
        print key, "updated from", config[key], "to", value 
        config[key] = value
        w = json.dumps(config )
        file_stream = open( config_file, "w" ) 
        file_stream.write(w)
        file_stream.close()
    elif key.lower() == "exit":
        print "Goodbye!"
        break
    else:
        print key, "not found!"
        print_available()