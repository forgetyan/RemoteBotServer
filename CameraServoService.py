from Adafruit_PWM_Servo_Driver import PWM
from datetime import datetime
import time
from threading import Thread

class CameraServoService(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.lastTime = datetime.now()
        self.daemon = True
        self.running = True
        self.MAX_CAMERA_POSITION = 100
        self.MIN_CAMERA_POSITION = -100
        self.CAMERA_RANGE = self.MAX_CAMERA_POSITION - self.MIN_CAMERA_POSITION # 200
        # Initialise the PWM device using the default address
        self.pwm = PWM(0x40)
        self.pwm.setPWMFreq(60)
        self.SERVO_XMIN = 150  # Min pulse length out of 4096
        self.SERVO_XMAX = 600  # Max pulse length out of 4096
        self.SERVO_YMIN = 150  # Min pulse length out of 4096
        self.SERVO_YMAX = 475  # Max pulse length out of 4096
        self.SERVO_XRANGE = self.SERVO_XMAX - self.SERVO_XMIN
        self.SERVO_YRANGE = self.SERVO_YMAX - self.SERVO_YMIN
        self.xCameraPulseCurrent = (self.SERVO_XRANGE / 2) + self.SERVO_XMIN
        self.yCameraPulseCurrent = (self.SERVO_YRANGE / 2) + self.SERVO_YMIN
        #self.xCameraPulse = (self.SERVO_XRANGE / 2) + self.SERVO_MIN
        #self.yCameraPulse = (self.SERVO_RANGE / 2) + self.SERVO_MIN
        self.xCameraData = 0
        self.yCameraData = 0

    def start(self):
        time.sleep(5)
        while self.running:
            time.sleep(0.01)
            elapsed = float((datetime.now() - self.lastTime).microseconds)
            self.lastTime = datetime.now()
            #xDiff = self.xCameraPulseCurrent - self.xCameraPulse
            #yDiff = self.yCameraPulseCurrent - self.yCameraPulse
            maxAdjust = elapsed / 200000

            if self.xCameraData <> 0:
                self.xCameraPulseCurrent = self.xCameraPulseCurrent + maxAdjust * self.xCameraData
                if self.xCameraPulseCurrent > self.SERVO_XMAX:
                    self.xCameraPulseCurrent = self.SERVO_XMAX
                if self.xCameraPulseCurrent < self.SERVO_XMIN:
                    self.xCameraPulseCurrent = self.SERVO_XMIN
                self.pwm.setPWM(0, 0, int(self.xCameraPulseCurrent))
            if self.yCameraData <> 0:
                self.yCameraPulseCurrent = self.yCameraPulseCurrent + (maxAdjust * -self.yCameraData)
                if self.yCameraPulseCurrent > self.SERVO_YMAX:
                    self.yCameraPulseCurrent = self.SERVO_YMAX
                if self.yCameraPulseCurrent < self.SERVO_YMIN:
                    self.yCameraPulseCurrent = self.SERVO_YMIN
                self.pwm.setPWM(1, 0, int(self.yCameraPulseCurrent))
                #print(str(self.yCameraPulseCurrent))
                
#            if self.xCameraPulseCurrent <> self.xCameraPulse:
#                if self.xCameraPulseCurrent < self.xCameraPulse:
#                    if self.xCameraPulseCurrent + maxAdjust > self.xCameraPulse:
#                        self.xCameraPulseCurrent = self.xCameraPulse
#                    else:
#                        self.xCameraPulseCurrent = self.xCameraPulseCurrent + maxAdjust
#                else:
#                    if self.xCameraPulseCurrent - maxAdjust < self.xCameraPulse:
#                        self.xCameraPulseCurrent = self.xCameraPulse
#                    else:
#                        self.xCameraPulseCurrent = self.xCameraPulseCurrent - maxAdjust
#                if self.xCameraPulseCurrent > self.SERVO_MAX:
#                    self.xCameraPulseCurrent = self.SERVO_MAX
#                if self.xCameraPulseCurrent < self.SERVO_MIN:
#                    self.xCameraPulseCurrent = self.SERVO_MIN
#                self.pwm.setPWM(0, 0, int(self.xCameraPulseCurrent))

#            if self.yCameraPulseCurrent <> self.yCameraPulse:
#                if self.yCameraPulseCurrent < self.yCameraPulse:
#                    if self.yCameraPulseCurrent + maxAdjust > self.yCameraPulse:
#                        self.yCameraPulseCurrent = self.yCameraPulse
#                    else:
#                        self.yCameraPulseCurrent = self.yCameraPulseCurrent + maxAdjust
#                else:
#                    if self.yCameraPulseCurrent - maxAdjust < self.yCameraPulse:
#                        self.yCameraPulseCurrent = self.yCameraPulse
#                    else:
#                        self.yCameraPulseCurrent = self.yCameraPulseCurrent - maxAdjust
#                if self.yCameraPulseCurrent > self.SERVO_MAX:
#                    self.yCameraPulseCurrent = self.SERVO_MAX
#                if self.yCameraPulseCurrent < self.SERVO_MIN:
#                    self.yCameraPulseCurrent = self.SERVO_MIN
#                self.pwm.setPWM(1, 0, int(self.yCameraPulseCurrent))
            
        
    def setServoPulse(channel, pulse):
      self.pulseLength = 1000000                   # 1,000,000 us per second
      self.pulseLength /= 60                       # 60 Hz
      print "%d us per period" % pulseLength
      self.pulseLength /= 4096                     # 12 bits of resolution
      print "%d us per bit" % pulseLength
      self.pulse *= 1000
      self.pulse /= pulseLength
      self.pwm.setPWM(channel, 0, pulse)
        
    def Message_Received(self, data):
        pertinentData = data[11:]
        pipePosition = pertinentData.rindex('|')
        self.xCameraData = float(pertinentData[:pipePosition])
        self.yCameraData = float(pertinentData[pipePosition + 1:])

        #self.xCameraPulse = int((((self.xCameraData - self.MIN_CAMERA_POSITION) / self.CAMERA_RANGE) * self.SERVO_RANGE) + self.SERVO_MIN)
        #self.yCameraPulse = int((((self.yCameraData - self.MIN_CAMERA_POSITION) / self.CAMERA_RANGE) * self.SERVO_RANGE) + self.SERVO_MIN)

        #print "Camera Pulse x: " + str(self.xCameraPulse)
        #print "Camera Pulse y: " + str(self.yCameraPulse)
        #self.pwm.setPWM(0, 0, self.xCameraPulse)
        #self.pwm.setPWM(1, 0, self.yCameraPulse)
        
