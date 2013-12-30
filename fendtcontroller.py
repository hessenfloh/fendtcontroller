#!/usr/bin/python

MOVE_MOTOR_PIN = 3
FORWARD_PIN = 5
BACKWARD_PIN = 11

TURN_MOTOR_PIN = 12
LEFT_PIN = 16
RIGHT_PIN = 18

STEPPER_SECONDS = 0.25

from time import sleep
import RPi.GPIO as GPIO

def enableMotor(movePin, motorPin):
    print 'Move Pin {} and MotorPin {} and Stepper {}'.format(movePin, motorPin, STEPPER_SECONDS)
    GPIO.output(motorPin, True)
    GPIO.output(movePin, True)
    sleep(STEPPER_SECONDS)
    GPIO.output(movePin, False)
    GPIO.output(motorPin, False)

print "Fendt Motor Runner..."
print "Mit RPI Board {} und Libversion {}".format(GPIO.RPI_REVISION, GPIO.VERSION)
print "l = LINKS"
print "r = RECHTS"
print "v = VOR"
print "z = ZURUECK"
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
    if userinput=='l':
        enableMotor(LEFT_PIN, TURN_MOTOR_PIN)
    if userinput=='r':
        enableMotor(RIGHT_PIN, TURN_MOTOR_PIN)
    if userinput=='v':
        enableMotor(FORWARD_PIN, MOVE_MOTOR_PIN)
    if userinput=='z':
        enableMotor(BACKWARD_PIN, MOVE_MOTOR_PIN)
    if userinput=='n':
        break

GPIO.cleanup()
