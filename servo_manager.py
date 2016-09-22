import RPi.GPIO as GPIO
import time
import os
from numpy import interp

class ServoManager(object):
	# self.current stores degrees
	
	def __init__(self, pin):
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(pin, GPIO.OUT)

		# default to center
		self.pin = pin
		self.currentAngle = 90
		self.setAngleInDegrees(self.currentAngle)
		#time.sleep(1)

	# set angle using degrees
	def setAngleInDegrees(self, degrees):
		if (degrees < 0 or degrees > 180):
			print("Angle must be between 0 and 180 degrees")
		else:
			self.currentAngle = degrees
			self.servo = GPIO.PWM(self.pin, 50)
			self.servo.start(self.degreesToCycle(self.currentAngle))
			time.sleep(1)
		
		self.servo.stop()
		
	# takes degrees, returns duty cycle
	def degreesToCycle(self, degrees):
		return float(interp(degrees,[0,180],[2.5,12.5]))
		
	def cleanup(self):
		self.servo.stop()
		GPIO.cleanup()
