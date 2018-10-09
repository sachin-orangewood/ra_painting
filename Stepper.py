import time
from time import sleep
import RPi.GPIO as gpio #https://pypi.python.org/pypi/RPi.GPIO
#import exitHandler #uncomment this and line 58 if using exitHandler


class stepper:
	#instantiate stepper 
	#pins = [stepPin, directionPin, enablePin]
	def __init__(self, pins):
		#setup pins
		self.pins = pins
		self.stepPin = self.pins[0]
		self.directionPin = self.pins[1]
		self.enablePin = self.pins[2]
		
		#use the broadcom layout for the gpio
		gpio.setmode(gpio.BCM)
		
		#set gpio pins
		gpio.setup(self.stepPin, gpio.OUT)
		gpio.setup(self.directionPin, gpio.OUT)
		gpio.setup(self.enablePin, gpio.OUT)
		
		#set enable to high (i.e. power is NOT going to the motor)
		gpio.output(self.enablePin, True)
		
		#print("Stepper initialized (step=" + str(self.stepPin) + ", direction=" + str(self.directionPin) + ", enable=" + str(self.enablePin) + ")")
	
	#clears GPIO settings
	def cleanGPIO(self):
		gpio.cleanup()
	
	#step the motor
	# steps = number of steps to take
	# dir = direction stepper will move
	# speed = defines the denominator in the waitTime equation: waitTime = 0.000001/speed. As "speed" is increased, the waitTime between steps is lowered
	# stayOn = defines whether or not stepper should stay "on" or not. If stepper will need to receive a new step command immediately, this should be set to "True." Otherwise, it should remain at "False."
	def step(self, steps, dir, speed, stayOn=False):
		#set enable to low (i.e. power IS going to the motor)
                gpio.output(self.enablePin, False)
                
		#set the output to true for left and false for right
                turnLeft = True
                if (dir == 'r'):
                    turnLeft = False;
                elif (dir != 'l'):
                    print("STEPPER ERROR: no direction supplied")
                    return False
                gpio.output(self.directionPin, turnLeft)

                stepCounter = 0
                #print("start")
##                execTime=60
                
##                waitTime = speed/0.0001 #waitTime controls speed
                                                
                while stepCounter < steps:
			#gracefully exit if ctr-c is pressed
			#exitHandler.exitPoint(True) #exitHandler.exitPoint(True, cleanGPIO)

			#turning the gpio on and off tells the easy driver to take one step
                        gpio.output(self.stepPin, True)
                        sleep(abs(speed))
                        gpio.output(self.stepPin, False)
                        #sleep(abs(speed))
                        stepCounter += 1
                        
			#wait before taking the next step thus controlling rotation speed
##                        sleep(speed)
		
##                        if (stayOn == False):
##                        #set enable to high (i.e. power is NOT going to the motor)
##                             gpio.output(self.enablePin, True)
                if (stayOn == False):
                        #set enable to high (i.e. power is NOT going to the motor)
                             gpio.output(self.enablePin, True)
                             print ("%s" % (time.ctime(time.time())))


                #print("stepperDriver complete (turned " + dir + " " + str(steps) + " degrees at "+ str(speed)+" speed)" )
		

