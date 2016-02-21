import time
import json
from threading import Thread
from Adafruit_LSM303 import Adafruit_LSM303 


class CompassService(Thread):

    def __init__(self, callback):
        Thread.__init__(self)
        self.daemon = True
        self.callback = callback
        self.running = True
        self.lsm = Adafruit_LSM303()

    def start(self):
        time.sleep(5)
#        while self.running:
#            time.sleep(0.5)
#            data = self.lsm.read()
#            self.callback("COMPASS:" + str(data[1][3]))# json.dumps(data))

    def SendInfo(self):
        nbTry = 0
        callDone = False
        while nbTry < 3 and callDone == False:
            try:
                data = self.lsm.read()
                self.callback("COMPASS:" + json.dumps(data)) #str(data[1][3]))
                callDone = True
            except:
                print "Error in CompassService.SendInfo"
                nbTry = nbTry + 1
                time.sleep(1)

    def stop(self):
        self.running = False
        self.join(2)
