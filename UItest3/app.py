"""
This file is part of the flask+d3 Hello World project.
"""

import json
import flask
import numpy as np


app = flask.Flask(__name__)


@app.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.

    """
    return flask.render_template("index1.html")

@app.route("/jsonData")
def jsonData():
    
    with open('flare.json') as data_file:    
        flareData = json.load(data_file)

    return json.dumps(flareData)
    

@app.route("/data")
def data():
    #return json.loads(open('flare.json'))
    with open('/flare.json') as data_file:    
        data = json.load(data_file)
        print(data)
        return data




if __name__ == "__main__":
    import os

    port = 8000

    # Open a web browser pointing at the app.
    os.system("open http://localhost:{0}".format(port))

    # Set up the development server on port 8000.
    app.debug = True
    app.run(port=port)
