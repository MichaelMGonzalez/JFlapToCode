import json
import sys
import jinja2
import os

out_file_name = "index.html"

out_fd = open(out_file_name, 'w+')

config_path = os.path.join( "..", "Config", "settings.json" )
config_fd = open( config_path )
config = json.load( config_fd )
config_fd.close()


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader( '.' ))
JINJA_ENVIRONMENT.line_comment_prefix = "#//"
JINJA_ENVIRONMENT.line_statement_prefix = "%"


template_file = 'index.jinja.html'
template = JINJA_ENVIRONMENT.get_template(template_file)
output = template.render(config)

out_fd.write(output)
out_fd.close()
