#!/usr/bin/python

PORT = 50007

import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('', PORT))

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

while userinput != 'n':
    userinput = raw_input('Choose direction: ')
    if userinput != 'n':
        client.send(userinput)
        data = client.recv(1024)
        print 'Answer from server: ', repr(data)

client.send('close')
client.close()
