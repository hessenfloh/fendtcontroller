#!/usr/bin/python

MOVE_MOTOR_PIN = 11
FORWARD_PIN = 13
BACKWARD_PIN = 15

TURN_MOTOR_PIN = 12
LEFT_PIN = 18
RIGHT_PIN = 16

#STEPPER_SECONDS = 1

PORT = 50007

#from time import sleep
import RPi.GPIO as GPIO
import socket
import sys
from uuid import uuid4

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOVE_MOTOR_PIN, GPIO.OUT)
    GPIO.setup(FORWARD_PIN, GPIO.OUT)
    GPIO.setup(BACKWARD_PIN, GPIO.OUT)
    GPIO.setup(TURN_MOTOR_PIN, GPIO.OUT)
    GPIO.setup(LEFT_PIN, GPIO.OUT)
    GPIO.setup(RIGHT_PIN, GPIO.OUT)

def done():
    GPIO.cleanup()

def stopAll():
    GPIO.output(FORWARD_PIN, False)
    GPIO.output(LEFT_PIN, False)
    GPIO.output(RIGHT_PIN, False)
    GPIO.output(BACKWARD_PIN, False)
    GPIO.output(TURN_MOTOR_PIN, False)
    GPIO.output(MOVE_MOTOR_PIN, False)

def enableMotor(movePin, directionPin, motorPin, turnPin):
    stopAll()
    print 'Pins: Move {} Direction {} Motor {} Turn {}'.format(movePin, directionPin, motorPin, turnPin)
#   print ' and Stepper {}'.format(STEPPER_SECONDS) 
    GPIO.output(motorPin, True)
    GPIO.output(turnPin, True)
    GPIO.output(movePin, True)
    GPIO.output(directionPin, True)
#    sleep(STEPPER_SECONDS)
#    GPIO.output(movePin, False)
#    GPIO.output(motorPin, False)
#    GPIO.output(directionPin, False)
#    GPIO.output(turnPin, False)

def evaluateDirection(userinput):
    if userinput=='vl':
        enableMotor(FORWARD_PIN, LEFT_PIN, MOVE_MOTOR_PIN, TURN_MOTOR_PIN)
    if userinput=='vr':
        enableMotor(FORWARD_PIN, RIGHT_PIN, MOVE_MOTOR_PIN, TURN_MOTOR_PIN)
    if userinput=='vv':
        enableMotor(FORWARD_PIN, FORWARD_PIN, MOVE_MOTOR_PIN, MOVE_MOTOR_PIN)
    if userinput=='zl':
        enableMotor(BACKWARD_PIN, LEFT_PIN, MOVE_MOTOR_PIN, TURN_MOTOR_PIN)
    if userinput=='zr':
        enableMotor(BACKWARD_PIN, RIGHT_PIN, MOVE_MOTOR_PIN, TURN_MOTOR_PIN)
    if userinput=='zz':
        enableMotor(BACKWARD_PIN, BACKWARD_PIN, MOVE_MOTOR_PIN, MOVE_MOTOR_PIN)
    if userinput=='s':
        stopAll()
    

def consoleMode():
    print "Fendt Motor Runner..."
    print "Mit RPI Board {} und Libversion {}".format(GPIO.RPI_REVISION, GPIO.VERSION)
    print "vl = VOR LINKS"
    print "vr = VOR RECHTS"
    print "vv = VOR VOR"
    print "zl = ZURUECK LINKS"
    print "zr = ZURUECK RECHTS"
    print "zz = ZURUECK ZURUECK"
    print "s  = STOP"
    print "n zum Beenden"    

    userinput = "-"

    while userinput <> "n":
        userinput = raw_input('Wohin? ')
        evaluateDirection(userinput)
        if userinput=='n':
            break

def showUsage():
    print 'Use parameter <console> for console mode or <service> for service mode'

__clientid = None

def serviceMode():
    theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    theSocket.bind(('', PORT))
    theSocket.listen(1)
    while 1:
        try:
            conn, addr = theSocket.accept()
            if addr[0] != '127.0.0.1':
                conn.close()
                raise OnlyLocalConnectAllowed('Only accepting local connects!')
            while 1:
                __clientid = uuid4()
                conn.send(__clientid)
                data = conn.recv(1024)
                print 'local echo client: ', repr(data) 
                if (len(data) == 2) or (data=='s'):
                    evaluateDirection(data)
                    conn.send('OK')
                elif repr(data) == 'close':
                    evaluateDirection('s')
                    conn.close()
                    break
                else:
                    conn.send('Wrong command! Only 2 characters or <s> allowed!: {}'.format(data))
        except KeyboardInterrupt:
            print 'Ending due to keyboard interrupt!'
            break
        except:
            print 'Socket error or error in operation!', sys.exc_info()[0]
            

if __name__ == '__main__':
    print 'Arguments: ', repr(len(sys.argv))
    if len(sys.argv) > 1:
        init()
        if sys.argv[1] == 'console':
            consoleMode()
        elif sys.argv[1] == 'service':
            serviceMode()
        else:
            showUsage()
        done()
    else:
        showUsage()
