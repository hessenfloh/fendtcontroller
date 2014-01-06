import socket

PORT = 50007

class TractorClient:
    """The tractor connection"""
    __connected = False
    
    def isConnected(self):
        return self.__connected
    
    def connectTractor(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('', PORT))
            self.__connected = True
        except socket.error:
            self.__connected = False
            return 'Connection error!'
        
    def sendInstruction(self, instruction):
        if self.__connected:
            client.send(instruction)
            data = client.recv(1024)
            print data
        
    def disconnectTractor(self):
        if self.__connected:
            client.send('close')
            client.close()
        
