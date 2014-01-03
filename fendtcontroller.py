#!/usr/bin/python

MOVE_MOTOR_PIN = 11
FORWARD_PIN = 13
BACKWARD_PIN = 15

TURN_MOTOR_PIN = 12
LEFT_PIN = 18
RIGHT_PIN = 16

STEPPER_SECONDS = 1

from time import sleep
import RPi.GPIO as GPIO

def enableMotor(movePin, directionPin, motorPin, turnPin):
    print 'Move Pin {} and MotorPin {} and Stepper {}'.format(movePin, motorPin, STEPPER_SECONDS)
    GPIO.output(motorPin, True)
    GPIO.output(turnPin, True)
    GPIO.output(movePin, True)
    GPIO.output(directionPin, True)
    sleep(STEPPER_SECONDS)
    GPIO.output(movePin, False)
    GPIO.output(motorPin, False)
    GPIO.output(directionPin, False)
    GPIO.output(turnPin, False)

print "Fendt Motor Runner..."
print "Mit RPI Board {} und Libversion {}".format(GPIO.RPI_REVISION, GPIO.VERSION)
print "vl = VOR LINKS"
print "vr = VOR RECHTS"
print "vv = VOR VOR"
print "zl = ZURUECK LINKS"
print "zr = ZURUECK RECHTS"
print "zz = ZURUECK ZURUECK"
print "n zum Beenden"    

userinput = "-"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOVE_MOTOR_PIN, GPIO.OUT)
GPIO.setup(FORWARD_PIN, GPIO.OUT)
GPIO.setup(BACKWARD_PIN, GPIO.OUT)
GPIO.setup(TURN_MOTOR_PIN, GPIO.OUT)
GPIO.setup(LEFT_PIN, GPIO.OUT)
GPIO.setup(RIGHT_PIN, GPIO.OUT)

while userinput <> "n":
    userinput = raw_input('Wohin? ')
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
    if userinput=='n':
        break

GPIO.cleanup()
