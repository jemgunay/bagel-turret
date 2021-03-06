from flask import Flask, render_template, Response, request, jsonify
from flask_basicauth import BasicAuth
from pivideostream import PiVideoStream
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import cv2
import time
from servo_manager import ServoManager
from motor_manager import MotorManager
#import urllib.request, urllib.parse

try:
	# video steam
	vs = PiVideoStream().start()
	
	# vertical axis aiming servo
	servo = ServoManager(11)
	servo.setAngleInDegrees(90)
	
	# horizontal axis aiming motor
	motor = MotorManager(16, 18, 22)
	
	# update public ip on main site for easy access
	#data = {}
	#data['new'] = 'remote_password'
	#url_values = urllib.parse.urlencode(data)
	#url = 'remote page for receiving ip update'
	#full_url = url + '?' + url_values
	#data = urllib.request.urlopen(full_url)
	
	# web server init & auth
	app = Flask(__name__)
	app.config['BASIC_AUTH_USERNAME'] = 'username'
	app.config['BASIC_AUTH_PASSWORD'] = 'password'
	app.config['BASIC_AUTH_FORCE'] = True
	basic_auth = BasicAuth(app)
	
	def __del__(self):
		vs.stop()
		
	@app.route('/')
	def index():
		# serve home page
		return render_template('index.html')

	def gen():
		# yield next camera stream frame
		while True:
			frame = vs.read()
			
			ret, jpeg = cv2.imencode('.jpg', frame)
			# encode image
			yield (b'--frame\r\n'
				   b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')

	@app.route('/stream')
	def stream():
		# serve stream page
		return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

	@app.route("/command")
	def command():
		# handle requests to control turret
		action = request.args.get('action', 0, type=int)
		if action == 0:
			return jsonify(result="no command supplied")
		elif action == 1:
			# rotate left/counterclockwise
			print("left")
			motor.setDirection(0)
			motor.start()			
			time.sleep(0.2);
			motor.stop();
		elif action == 2:
			# rotate right/clockwise
			print("right")
			motor.setDirection(1)
			motor.start()			
			time.sleep(0.2);
			motor.stop();
		elif action == 3:
			# shoot
			print("fire")
		elif action == 4:
			# aim upwards
			print("up")
			servo.setAngleInDegrees(servo.currentAngle - 15)
		elif action == 5:
			# aim downwards
			print("down")
			servo.setAngleInDegrees(servo.currentAngle + 15)
		
		return jsonify(result=action)

	if __name__ == '__main__':
		# debug=True
		app.run(host='0.0.0.0', port=80, debug=False, threaded=True)

# clean up
except KeyboardInterrupt:
	vs.stop()
	servo.cleanup()
	motor.cleanup()
