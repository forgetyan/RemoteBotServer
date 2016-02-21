import math
import time
import RPi.GPIO as GPIO
from NetworkBot import *
from CompassService import *
from MotorService import *
from CameraServoService import *

class Program():
    def Init(self):
        #self.led1 = 37
        GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(self.led1, GPIO.OUT)
        self.networkBot = NetworkBot(self.on_network_message_received)
        self.networkBot.start()
        self.compassService = CompassService(self.on_compass_event)
        self.motorService = MotorService()
        self.compassService.start()
        self.cameraServoService = CameraServoService()
        self.cameraServoService.start()

    def cleanup():
        self.cameraServoService.stop()
        self.compassService.stop()
        
    def Run(self):
        self.running = True
        print("Running!")
        while self.running:
            time.sleep(0.8)

    def on_compass_event(self, data):
        self.networkBot.send(data)

    def on_network_message_received(self, data):
        #print("Data received: " + data);
        if data == "ON":
            print "Setting LED state to ON"
            #GPIO.output(self.led1, 1)
        if data == "OFF":
            print "Setting LED state to OFF"
            #GPIO.output(self.led1, 0)
        if data == "ASK_COMPASS":
            self.compassService.SendInfo()
        if data.startswith("MOTOR"):
            self.motorService.Message_Received(data)
        if data.startswith("CAMERA_POS"):
            self.cameraServoService.Message_Received(data)

p = Program()
p.Init()
p.Run()
p.cleanup()
GPIO.cleanup()
