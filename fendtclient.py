#!/usr/bin/python

PORT = 50007

import socket

from threading import Thread
from time import sleep
from Queue import Queue

class FendtClient:
    def sendToTractor(self):
        while self.__isrunning:
            if not self.__queue.empty():
                cmd = self.__queue.get()
                print "cmd is ", cmd
                self.__client.send(cmd)
                data = self.__client.recv(1024)
                print 'Answer to {} from server: {}'.format(cmd, repr(data))
            sleep(0.5)
            print "send Loop..."

    def addPing(self):
        while self.__isrunning:
            print "queueing a ping..."
            self.__queue.put('ping')
            sleep(2)

    def mainLoop(self):
        self.__queue = Queue()
        self.__queue.put('ping')
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect(('', PORT))
        
        userinput = '-'
        print "Fendt Motor Runner..."
        print "vl = VOR LINKS"
        print "vr = VOR RECHTS"
        print "vv = VOR VOR"
        print "zl = ZURUECK LINKS"
        print "zr = ZURUECK RECHTS"
        print "zz = ZURUECK ZURUECK"
        print "s  = STOP"
        print "n zum Beenden"    
        
        self.__isrunning = True
        t = Thread(target=self.sendToTractor)
        t.start()
        print "send Thread started."
        t2 = Thread(target=self.addPing)
        t2.start()
        print "ping Thread started."        
        while userinput != 'n':
            userinput = raw_input('Choose direction: ')
            if userinput != 'n':
                self.__queue.put(userinput)
        self.__client.send('close')
        while not self.__queue.empty():
            sleep(0.5)
        self.__isrunning = False        
        t.join()
        t2.join()
        self.__client.close()
        
f = FendtClient()
f.mainLoop()
