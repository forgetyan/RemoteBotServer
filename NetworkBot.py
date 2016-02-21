import socket
import time
from threading import *

TCP_IP = '127.0.0.1'
TCP_PORT = 50005
BUFFER_SIZE = 1024

class NetworkBotInstance(Thread):
    def __init__(self, conn, addr, messageCallback, stopCallback):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.daemon = True
        self.messageCallback = messageCallback
        self.stopCallback = stopCallback
        self.running = True
        self.socketData = ""

    def send(self, message):
#        print "Sending: "
#        print message
        try:
            sent = self.conn.send(message + "||")
        except:
            print "Send Error"
            self.running = False
    
    def run(self):
        while self.running:
#            try:
                time.sleep(0.1)
                data = self.conn.recv(BUFFER_SIZE)
                if data:
                    self.socketData = self.socketData + data
                    i = self.socketData.find("||")
                    while i > 0:
                        command = self.socketData[:i]
#                        print "Received command: "
#                        print command
                        self.socketData = self.socketData[i+2:]
                        self.messageCallback(command)
                        i = self.socketData.find("||")
#            except:
 #               self.running = False
  #              self.conn.close()
   #             print "Connection closed on ", self.addr
        self.stopCallback()

                    
class NetworkBot(Thread):
    def __init__(self, callback):
        Thread.__init__(self)
        self.daemon = True
        self.callback = callback
        self.running = True
        self.socketData = ""
        self.connectionList = []

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('', TCP_PORT))
        self.sock.listen(5)
        print("Listening on " + socket.gethostname())
        while self.running:
            time.sleep(0.8)
            conn, addr = self.sock.accept()
            print 'Connection accepted on address:', addr
            newInstance = NetworkBotInstance(conn, addr, self.callback, self.stopCallback)
            self.connectionList.extend([newInstance])
            newInstance.start()
            
    def stop(self, message):
        self.running = False
        self.join(2)    

    def send(self, message):
        for connection in self.connectionList:
            connection.send(message)

    def stopCallback(self):
        for connection in self.connectionList:
            if connection.running == False:
                self.connectionList.remove(connection)
