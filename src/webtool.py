from flask import Flask
from flask import request
import json
from FSMTranslator.JFlapToCode import * 
from FSMTranslator.Constants import * 
from FSMTranslator.GraphUtils import *

app = Flask(__name__)

def parse( mode ):
    try:
        val = request.form["network"]
        network_json = json.loads( val )
        parser = JFlapParser(config_file=config_file)
        parser.quiet_mode()
        parser.set_mode(mode)
        parser.parse_json( network_json )
        parser.setup_functions()
    	code = parser.render_jinja()
        return str(code)
    except Exception as e:
        return "what : " + str( e ) 
        pass
    return str( network_json )
 

 
@app.route("/<target>", methods=["POST"])
def compile(target):
    return parse(target)
if __name__ == "__main__":
    app.run()
