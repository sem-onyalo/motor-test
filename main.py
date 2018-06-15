import RPi.GPIO as GPIO
import time

# Agent control variables

MOTOR_A1 = 17
MOTOR_A2 = 23
MOTOR_B1 = 24
MOTOR_B2 = 25
MOTOR_AP = 18
MOTOR_BP = 13
MOTOR_STBY = 22
MOTOR_MAXSPD = 100 # percentage

MOTOR_A = 'A'
MOTOR_B = 'B'

MOTOR_FORWARD = 'F'
MOTOR_BACKWARD = 'B'
MOTOR_STOP = 'S'

AGENT_FORWARD = 'F'
AGENT_BACKWARD = 'B'
AGENT_LEFT = 'L'
AGENT_RIGHT = 'R'
AGENT_STOP = 'S'

def motorDirection(type, dir, spd, pwmMotorA, pwmMotorB):
	if type == MOTOR_A:
		if dir == MOTOR_FORWARD:
			GPIO.output(MOTOR_A1, GPIO.HIGH)
			GPIO.output(MOTOR_A2, GPIO.LOW)
			pwmMotorA.ChangeDutyCycle(spd)
		elif dir == MOTOR_BACKWARD:
			GPIO.output(MOTOR_A1, GPIO.LOW)
			GPIO.output(MOTOR_A2, GPIO.HIGH)
			pwmMotorA.ChangeDutyCycle(spd)
		elif dir == MOTOR_STOP:
			GPIO.output(MOTOR_A1, GPIO.LOW)
			GPIO.output(MOTOR_A2, GPIO.LOW)
			pwmMotorA.ChangeDutyCycle(spd)
	elif type == MOTOR_B:
		if dir == MOTOR_FORWARD:
			GPIO.output(MOTOR_B1, GPIO.HIGH)
			GPIO.output(MOTOR_B2, GPIO.LOW)
			pwmMotorB.ChangeDutyCycle(spd)
		elif dir == MOTOR_BACKWARD:
			GPIO.output(MOTOR_B1, GPIO.LOW)
			GPIO.output(MOTOR_B2, GPIO.HIGH)
			pwmMotorB.ChangeDutyCycle(spd)
		elif dir == MOTOR_STOP:
			GPIO.output(MOTOR_B1, GPIO.LOW)
			GPIO.output(MOTOR_B2, GPIO.LOW)
			pwmMotorB.ChangeDutyCycle(spd)

def agentDirection(dir, spd, pwmMotorA, pwmMotorB):
	if dir == AGENT_FORWARD:
		motorDirection(MOTOR_A, MOTOR_FORWARD, spd, pwmMotorA, pwmMotorB)
		motorDirection(MOTOR_B, MOTOR_FORWARD, spd, pwmMotorA, pwmMotorB)
	elif dir == AGENT_BACKWARD:
		motorDirection(MOTOR_A, MOTOR_BACKWARD, spd, pwmMotorA, pwmMotorB)
		motorDirection(MOTOR_B, MOTOR_BACKWARD, spd, pwmMotorA, pwmMotorB)
	elif dir == AGENT_LEFT:
		motorDirection(MOTOR_A, MOTOR_BACKWARD, spd, pwmMotorA, pwmMotorB)
		motorDirection(MOTOR_B, MOTOR_FORWARD, spd, pwmMotorA, pwmMotorB)
	elif dir == AGENT_RIGHT:
		motorDirection(MOTOR_A, MOTOR_FORWARD, spd, pwmMotorA, pwmMotorB)
		motorDirection(MOTOR_B, MOTOR_BACKWARD, spd, pwmMotorA, pwmMotorB)
	elif dir == AGENT_STOP:
		motorDirection(MOTOR_A, MOTOR_STOP, spd, pwmMotorA, pwmMotorB)
		motorDirection(MOTOR_B, MOTOR_STOP, spd, pwmMotorA, pwmMotorB)

def initAgent(pwmFreq):
	GPIO.setup(MOTOR_A1, GPIO.OUT)
	GPIO.setup(MOTOR_A2, GPIO.OUT)
	GPIO.setup(MOTOR_AP, GPIO.OUT)
	
	GPIO.setup(MOTOR_B1, GPIO.OUT)
	GPIO.setup(MOTOR_B2, GPIO.OUT)
	GPIO.setup(MOTOR_BP, GPIO.OUT)
	
	GPIO.setup(MOTOR_STBY, GPIO.OUT)
	GPIO.output(MOTOR_STBY, GPIO.HIGH)

	pwmMotorA = GPIO.PWM(MOTOR_AP, pwmFreq)
	pwmMotorA.start(0)

	pwmMotorB = GPIO.PWM(MOTOR_BP, pwmFreq)
	pwmMotorB.start(0)

	agentDirection(AGENT_STOP, MOTOR_MAXSPD, pwmMotorA, pwmMotorB)

	return pwmMotorA, pwmMotorB

def runAgent():
	_spd = 20
	_pwmFreq = 1000
	_delaySec = 5
	
	pwmMotorA, pwmMotorB = initAgent(_pwmFreq)
	
	while True:
		agentDirection(AGENT_FORWARD, _spd, pwmMotorA, pwmMotorB)
		time.sleep(_delaySec)
		
		agentDirection(AGENT_BACKWARD, _spd, pwmMotorA, pwmMotorB)
		time.sleep(_delaySec)
		
		agentDirection(AGENT_LEFT, _spd, pwmMotorA, pwmMotorB)
		time.sleep(_delaySec)
		
		agentDirection(AGENT_RIGHT, _spd, pwmMotorA, pwmMotorB)
		time.sleep(_delaySec)

		agentDirection(AGENT_STOP, _spd, pwmMotorA, pwmMotorB)
		time.sleep(_delaySec)

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	
	try:
		runAgent()
		
	except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
		print("Keyboard interrupt")
		
	finally:
		GPIO.cleanup()
