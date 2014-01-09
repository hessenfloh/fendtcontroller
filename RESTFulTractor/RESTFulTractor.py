#!/usr/bin/python

from flask import Flask, url_for, send_from_directory, request
from TractorClient import TractorClient

PING_ACTION = 'action'
PING_ACTION_CONNECT = 'connect'
PING_ACTION_PING = 'ping'
PING_ACTION_DISCONNECT = 'disconnect'
TRACTOR_CLIENT_ID = 'id'

app = Flask(__name__)

@app.route("/")
def index():
    url_for('static', filename='TractorControl.html')
    url_for('static', filename='TractorControl.css')
    url_for('static', filename='TractorControl.js')
    return send_from_directory('static', 'TractorControl.html')

@app.route('/pingTractor')
def pingTractor():
    if PING_ACTION in request.args:
        tractor = TractorClient()
        if request.args[PING_ACTION] == PING_ACTION_CONNECT:
            ret=tractor.connectTractor()
            if tractor.isConnected():
                ret = 'Is connected!'
        if TRACTOR_CLIENT_ID in request.args:
            clientID = request.args[TRACTOR_CLIENT_ID] 
            if request.args[PING_ACTION] == PING_ACTION_PING:
                tractor.ping(clientID)
            if request.args[PING_ACTION] == PING_ACTION_DISCONNECT:
                tractor.disconnectTractor(clientID)
    return ret

@app.route('/moveForward')
def moveForward():
    tractor = TractorClient()
    ret=tractor.connectTractor()
    if tractor.isConnected():
        ret = 'Moving Forward!'
	ret += repr(tractor.sendInstruction("vv"))
        tractor.disconnectTractor()
    return ret

@app.route('/moveForwardLeft')
def moveForwardLeft():
    return 'Moving Forward Left!'

@app.route('/moveForwardRight')
def moveForwardRight():
    return 'Moving Forward Right!'

@app.route('/moveBackward')
def moveBackward():
    return 'Moving Backward!'

@app.route('/moveBackwardLeft')
def moveBackwardLeft():
    return 'Moving Backward Left!'

@app.route('/moveBackwardRight')
def moveBackwardRight():
    return 'Moving Backward Right!'


if __name__ == '__main__':
    app.run(debug=True)
