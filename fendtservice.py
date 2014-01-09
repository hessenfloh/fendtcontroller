#import RPi.GPIO as GPIO
import RPIMockGPIO as GPIO
import socket
import sys

from threading import Timer
from uuid import uuid4
from time import time


class FendtService:
    """Control the Fendt RC tractor using GPIO"""
    
    def __init__(self, forwardPin, leftPin, rightPin, backPin, turnPin, movePin):
        self.__forwardPin = forwardPin
        self.__leftPin = leftPin
        self.__rightPin = rightPin
        self.__backPin = backPin
        self.__turnPin = turnPin
        self.__movePin = movePin
        self.__clientid = None
        self.__lastPing = 0
    
    def stopAll(self):
        GPIO.output(self.__forwardPin, False)
        GPIO.output(self.__leftPin, False)
        GPIO.output(self.__rightPin, False)
        GPIO.output(self.__backPin, False)
        GPIO.output(self.__turnPin, False)
        GPIO.output(self.__movePin, False)

    def enableMotor(self, movePin, directionPin, motorPin, turnPin):
        self.stopAll()
        print 'Pins: Move {} Direction {} Motor {} Turn {}'.format(movePin, directionPin, motorPin, turnPin)
        GPIO.output(motorPin, True)
        GPIO.output(turnPin, True)
        GPIO.output(movePin, True)
        GPIO.output(directionPin, True)

    def evaluateDirection(self, userinput):
        if userinput=='vl':
            self.enableMotor(self.__forwardPin, self.__leftPin, self.__movePin, self.__turnPin)
        if userinput=='vr':
            self.enableMotor(self.__forwardPin, self.__rightPin, self.__movePin, self.__turnPin)
        if userinput=='vv':
            self.enableMotor(self.__forwardPin, self.__forwardPin, self.__movePin, self.__movePin)
        if userinput=='zl':
            self.enableMotor(self.__backPin, self.__leftPin, self.__movePin, self.__turnPin)
        if userinput=='zr':
            self.enableMotor(self.__backPin, self.__rightPin, self.__movePin, self.__turnPin)
        if userinput=='zz':
            self.enableMotor(self.__backPin, self.__backPin, self.__movePin, self.__movePin)
        if userinput=='s':
            self.stopAll()
        

    def consoleMode(self):
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
            self.evaluateDirection(userinput)
            if userinput=='n':
                break

    def checkPing(self):
        if (self.__lastPing + 2) < time():
            print "Need to disconnect!!" 
            self.__disconnect = True
            self.stopAll()

    def serviceMode(self, port):
        theSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        theSocket.bind(('', port))
        theSocket.listen(1)
        while 1:
            try:
                self.__conn, addr = theSocket.accept()
                print "a client tries to connect..."
                if addr[0] != '127.0.0.1':
                    self.__conn.close()
                    raise OnlyLocalConnectAllowed('Only accepting local connects!')
                else:
                    self.__clientid = repr(uuid4())
                    print "generated client id: {}".format(self.__clientid)
                    self.__conn.send(self.__clientid)
                    self.__disconnect = False
                    self.__lastPing = time()
                    print "last ping is: ", repr(self.__lastPing)
                    self.__timer = Timer(1, self.checkPing)
                    self.__timer.start()
                while 1:
                    print 'waiting for client...'
                    data = self.__conn.recv(1024)
                    print 'local echo client: ', repr(data) 
                    if (len(data) == 2) or (data=='s'):
                        self.evaluateDirection(data)
                        self.__conn.send('OK')
                    elif repr(data) == 'close':
                        self.__timer.cancel()
                        self.evaluateDirection('s')
                        self.__conn.close()
                        break
                    else:
                        self.__conn.send('Wrong command! Only 2 characters or <s> allowed!: {}'.format(data))
            except KeyboardInterrupt:
                print 'Ending due to keyboard interrupt!'
                break
            except:
                print 'Socket error or error in operation!', sys.exc_info()[0], sys.exc_info()[1]
