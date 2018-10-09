from time import sleep
import RPi.GPIO as GPIO

DIR = 27   # Direction GPIO Pin
STEP = 17  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1600   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

step_count = 1000
delay = 0.0025

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

sleep(.5)
GPIO.output(DIR, CW)
##for x in range(step_count):
##    GPIO.output(STEP, GPIO.HIGH)
##    sleep(delay)
##    GPIO.output(STEP, GPIO.LOW)
##    sleep(delay)

GPIO.cleanup()