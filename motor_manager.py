import RPi.GPIO as GPIO
from time import sleep

class MotorManager(object):
    # init GPIO
    def __init__(self,A,B,E):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self.motorA = A
        self.motorB = B
        self.motorE = E
        GPIO.setup(self.motorA, GPIO.OUT)
        GPIO.setup(self.motorB, GPIO.OUT)
        GPIO.setup(self.motorE, GPIO.OUT)
        self.setDirection(0)
    
	# start motor rotation
    def start(self):
        GPIO.output(self.motorE, GPIO.HIGH)
    
	# stop motor rotation    
    def stop(self):
        GPIO.output(self.motorE, GPIO.LOW)
    
	# flip rotational direction
    def switchDirection(self):
        if self.direction == True:
            self.setDirection(1)
        else:
            self.setDirection(0)
    
	# 
    def setDirection(self, d):
        if d == 1:
            # clockwise
            GPIO.output(self.motorA, GPIO.LOW)
            GPIO.output(self.motorB, GPIO.HIGH)
            self.direction = False
        elif d == 0:
            # counter clockwise
            GPIO.output(self.motorA, GPIO.HIGH)
            GPIO.output(self.motorB, GPIO.LOW)
            self.direction = True
            
    def cleanup(self):
        self.stop()
        GPIO.cleanup()
        