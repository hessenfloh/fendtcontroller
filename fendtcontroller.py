#!/usr/bin/python

MOVE_MOTOR_PIN = 12
FORWARD_PIN = 18
BACKWARD_PIN = 16

TURN_MOTOR_PIN = 11
LEFT_PIN = 15
RIGHT_PIN = 13

#STEPPER_SECONDS = 1

PORT = 50007

import RPi.GPIO as GPIO
#import RPIMockGPIO as GPIO
import sys
from fendtservice import FendtService

def showUsage():
    print 'Use parameter <console> for console mode or <service> for service mode'

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

if __name__ == '__main__':
    print 'Arguments: ', repr(len(sys.argv))
    if len(sys.argv) > 1:
        init()
        f = FendtService(FORWARD_PIN, LEFT_PIN, RIGHT_PIN, BACKWARD_PIN, TURN_MOTOR_PIN, MOVE_MOTOR_PIN)
        if sys.argv[1] == 'console':
            f.consoleMode()
        elif sys.argv[1] == 'service':
            f.serviceMode(PORT)
        else:
            showUsage()
        done()
    else:
        showUsage()
                    
