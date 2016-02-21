from pololu_drv8835_rpi import motors, MAX_SPEED

class MotorService():
    def __init__(self):
        motors.setSpeeds(0, 0)
        self.MAX_THROTTLE_POSITION = 100
        
    def Message_Received(self, data):
        pertinentData = data[5:]
        pipePosition = pertinentData.rindex('|')
        leftMotorData = pertinentData[:pipePosition]
        rightMotorData = pertinentData[pipePosition + 1:]
        increment = MAX_SPEED / self.MAX_THROTTLE_POSITION
        leftMotorForward = leftMotorData[:1] == "F"
        leftMotorSpeed = increment * int(leftMotorData[1:])
        if (leftMotorForward == False):
            leftMotorSpeed = leftMotorSpeed * -1
        rightMotorForward = rightMotorData[:1] == "F"
        rightMotorSpeed = increment * int(rightMotorData[1:])
        if (rightMotorForward == False):
            rightMotorSpeed = rightMotorSpeed * -1
        motors.setSpeeds(leftMotorSpeed, rightMotorSpeed)
