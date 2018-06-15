#include <stdio.h>
#include <fcntl.h>
#include <wiringPi.h>

// Agent control variables

#define MOTOR_A1 17
#define MOTOR_A2 23
#define MOTOR_B1 24
#define MOTOR_B2 25
#define MOTOR_AP 18
#define MOTOR_BP 13
#define MOTOR_STBY 22
#define MOTOR_MAXSPD 1023

#define MOTOR_A 'A'
#define MOTOR_B 'B'

#define MOTOR_FORWARD 'F'
#define MOTOR_BACKWARD 'B'
#define MOTOR_STOP 'S'

#define AGENT_FORWARD 'F'
#define AGENT_BACKWARD 'B'
#define AGENT_LEFT 'L'
#define AGENT_RIGHT 'R'
#define AGENT_STOP 'S'

void motorDirection(char type, char dir, int spd);
void agentDirection(char dir, int spd);
void runAgent(void);
void initAgent(void);

int main(void)
{	
	printf("init wiringPi...\n");
	wiringPiSetupGpio();
	
	printf("init agent...\n");
	initAgent();
	
	printf("start\n");
	
	runAgent();
	
	return 0;
}

void motorDirection(char type, char dir, int spd)
{
	if (spd > MOTOR_MAXSPD) spd = MOTOR_MAXSPD;
	else if (spd < 0) spd = 0;
	
	if (type == MOTOR_A)
	{
		if (dir == MOTOR_FORWARD)
		{
			digitalWrite(MOTOR_A1, HIGH);
			digitalWrite(MOTOR_A2, LOW);
			pwmWrite(MOTOR_AP, spd);
		}
		else if (dir == MOTOR_BACKWARD)
		{
			digitalWrite(MOTOR_A1, LOW);
			digitalWrite(MOTOR_A2, HIGH);
			pwmWrite(MOTOR_AP, spd);
		}
		else if (dir == MOTOR_STOP)
		{
			digitalWrite(MOTOR_A1, LOW);
			digitalWrite(MOTOR_A2, LOW);
			pwmWrite(MOTOR_AP, spd);
		}
	}
	else if (type == MOTOR_B)
	{
		if (dir == MOTOR_FORWARD)
		{
			digitalWrite(MOTOR_B1, HIGH);
			digitalWrite(MOTOR_B2, LOW);
			pwmWrite(MOTOR_BP, spd);
		}
		else if (dir == MOTOR_BACKWARD)
		{
			digitalWrite(MOTOR_B1, LOW);
			digitalWrite(MOTOR_B2, HIGH);
			pwmWrite(MOTOR_BP, spd);
		}
		else if (dir == MOTOR_STOP)
		{
			digitalWrite(MOTOR_B1, LOW);
			digitalWrite(MOTOR_B2, LOW);
			pwmWrite(MOTOR_BP, spd);
		}
	}
}

void agentDirection(char dir, int spd)
{
	switch (dir)
	{
		case AGENT_FORWARD:
			motorDirection(MOTOR_A, MOTOR_FORWARD, spd);
			motorDirection(MOTOR_B, MOTOR_FORWARD, spd);
			break;
		 
		case AGENT_BACKWARD:
			motorDirection(MOTOR_A, MOTOR_BACKWARD, spd);
			motorDirection(MOTOR_B, MOTOR_BACKWARD, spd);
			break;
		 
		case AGENT_LEFT:
			motorDirection(MOTOR_A, MOTOR_BACKWARD, spd);
			motorDirection(MOTOR_B, MOTOR_FORWARD, spd);
			break;
		 
		case AGENT_RIGHT:
			motorDirection(MOTOR_A, MOTOR_FORWARD, spd);
			motorDirection(MOTOR_B, MOTOR_BACKWARD, spd);
			break;
		 
		case AGENT_STOP:
			motorDirection(MOTOR_A, MOTOR_STOP, spd);
			motorDirection(MOTOR_B, MOTOR_STOP, spd);
			break;
	}
}

void runAgent(void)
{
	int _delayMs = 5000;	
	while(1)
	{
		agentDirection(AGENT_FORWARD, MOTOR_MAXSPD);
		delay(_delayMs);
		
		agentDirection(AGENT_BACKWARD, MOTOR_MAXSPD);
		delay(_delayMs);
		
		agentDirection(AGENT_LEFT, MOTOR_MAXSPD);
		delay(_delayMs);
		
		agentDirection(AGENT_RIGHT, MOTOR_MAXSPD);
		delay(_delayMs);
		
		agentDirection(AGENT_STOP, MOTOR_MAXSPD);
		delay(_delayMs);
	}
}

void initAgent(void)
{
	pinMode(MOTOR_A1, OUTPUT);
	pinMode(MOTOR_A2, OUTPUT);
	pinMode(MOTOR_AP, PWM_OUTPUT);
	
	pinMode(MOTOR_B1, OUTPUT);
	pinMode(MOTOR_B2, OUTPUT);
	pinMode(MOTOR_BP, PWM_OUTPUT);
	
	pinMode(MOTOR_STBY, OUTPUT);

	digitalWrite(MOTOR_STBY, HIGH);

	agentDirection(AGENT_STOP, MOTOR_MAXSPD);
}
