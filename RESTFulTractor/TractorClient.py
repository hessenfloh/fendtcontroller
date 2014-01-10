import socket

PORT = 50007

class TractorClient:
    """The tractor connection"""
    __connected = False
  
    def isConnected(self):
        return self.__connected
    
    def connectTractor(self):
        try:
            self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client.connect(('', PORT))
            self.__connected = True
        except socket.error:
            self.__connected = False
            return 'Connection error!'
        
    def sendInstruction(self, instruction):
        if self.__connected:
            self.__client.send(instruction)
            data = self.__client.recv(1024)
            return data
        
    def disconnectTractor(self):
        if self.__connected:
            self.__client.send('close')
            self.__client.close()
        
