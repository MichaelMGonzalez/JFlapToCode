from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    f = open( 'index.html' )
    return f.read()