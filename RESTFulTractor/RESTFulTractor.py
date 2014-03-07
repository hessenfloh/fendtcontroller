#!/usr/bin/python

from flask import Flask, url_for, send_from_directory, request
from TractorClient import TractorClient

PING_ACTION = 'ping'

app = Flask(__name__)

@app.route("/")
def index():
    url_for('static', filename='TractorControl.html')
    url_for('static', filename='TractorControl.css')
    url_for('static', filename='TractorControl.js')
    return send_from_directory('static', 'TractorControl.html')

def connectAndSend(cmd):
    tractor = TractorClient()
    ret=tractor.connectTractor()
    if tractor.isConnected():
        ret = repr(tractor.sendInstruction(cmd))
        tractor.disconnectTractor()
    return ret  

@app.route('/pingTractor')
def pingTractor():
    return connectAndSend(PING_ACTION)

@app.route('/moveForward')
def moveForward():
    return connectAndSend('vv')

@app.route('/moveForwardLeft')
def moveForwardLeft():
    return connectAndSend('vl')

@app.route('/moveForwardRight')
def moveForwardRight():
    return connectAndSend('vr')

@app.route('/moveBackward')
def moveBackward():
    return connectAndSend('zz')

@app.route('/moveBackwardLeft')
def moveBackwardLeft():
    return connectAndSend('zl')

@app.route('/moveBackwardRight')
def moveBackwardRight():
    return connectAndSend('zr')

@app.route('/stop')
def stop():
    return connectAndSend('s')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
