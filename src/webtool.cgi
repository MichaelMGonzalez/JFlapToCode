#!/usr/bin/python
import sys
sys.path.append('/var/www/flask-prod')

from wsgiref.handlers import CGIHandler
from webtool import app


CGIHandler().run(app)
 
