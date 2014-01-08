#!/usr/bin/python

from flask import Flask
from TractorClient import TractorClient

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('static', 'TractorControl.html')

@app.route('/moveForward')
def moveForward():
    tractor = TractorClient()
    ret=tractor.connectTractor()
    if tractor.isConnected():
        ret = 'Moving Forward!'
	ret += repr(tractor.sendInstruction("vv"))
        tractor.disconnectTractor()
    return ret

@app.route('/moveBackward')
def moveBackward():
    return 'Moving Backward!'

@app.route('/moveForwardLeft')
def moveForwardLeft():
    return 'Moving Forward Left!'


if __name__ == '__main__':
    app.run(debug=True)
