#import RPi.GPIO as GPIO
import RPIMockGPIO as GPIO
import asyncore
import socket
import sys

from threading import Thread
from uuid import uuid4
from time import time, sleep

class SocketReader(asyncore.dispatcher_with_send):
    def __init__(self, sock, eval_function, setPing):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.__eval_function = eval_function
        self.__lastPing = setPing
        self.__lastPing(time())

    def handle_read(self):
        data = self.recv(1024)
        if data:
            self.__lastPing(time())
            if self.__eval_function(data):
                self.send('OK')
            else:
                self.close()

class MainSocket(asyncore.dispatcher):
    def __init__(self, host, port, eval_function, setPing):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)
        self.__eval_function = eval_function
        self.__lastPing = setPing
        
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            if addr[0] != '127.0.0.1':
                self.close()
                raise OnlyLocalConnectAllowed('Only accepting local connects!')
            handler = SocketReader(sock, self.__eval_function, self.__lastPing)


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
        self.__lastPing = time()
        self.__stopped = True
    
    def stopAll(self):
        GPIO.output(self.__forwardPin, False)
        GPIO.output(self.__leftPin, False)
        GPIO.output(self.__rightPin, False)
        GPIO.output(self.__backPin, False)
        GPIO.output(self.__turnPin, False)
        GPIO.output(self.__movePin, False)
        self.__stopped = True

    def enableMotor(self, movePin, directionPin, motorPin, turnPin):
        self.stopAll()
        print 'Pins: Move {} Direction {} Motor {} Turn {}'.format(movePin, directionPin, motorPin, turnPin)
        GPIO.output(motorPin, True)
        GPIO.output(turnPin, True)
        GPIO.output(movePin, True)
        GPIO.output(directionPin, True)
        self.__stopped = False

    def evaluateDirection(self, userinput):
        goOn = True
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
        if userinput=='close':
            self.stopAll()
            goOn = False            
        return goOn
        

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

    def setPing(self, pingTime):
        self.__lastPing = pingTime
        print "last ping is: ", repr(self.__lastPing)
        
    def checkPing(self):
        while self.__serviceRunning:
            if (self.__lastPing + 4) < time() and not self.__stopped:
                print "Need to stop!!" 
                self.evaluateDirection('s')
            else:
                sleep(1)
        if not self.__stopped:
            self.evaluateDirection('s')

    def serviceMode(self, port):
        self.__serviceRunning = True
        self.__timer = Thread(target=self.checkPing)
        self.__timer.start()
        while 1:
            server = MainSocket('', port, self.evaluateDirection, self.setPing)
            try:                
                asyncore.loop()                
            except KeyboardInterrupt:
                print 'Ending due to keyboard interrupt!'
                server.close()
                self.__serviceRunning = False
                break
            except:
                print 'Socket error or error in operation!', sys.exc_info()[0], sys.exc_info()[1]
