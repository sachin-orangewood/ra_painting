import math
import evdev
import _thread
import time
import RPi.GPIO as GPIO
from time import sleep

from Stepper import stepper

######
DIR = 19   # Direction GPIO Pin
STEP = 26  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 1600   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CW)

height = 1.5


######
def print_time(threadName, delay, s, steps, dir, speed):
   count = 1
   while count >=1:
      time.sleep(delay)
      count -= 1
      print ("%s: %s" % ( threadName, time.ctime(time.time())))
      testStepper = stepper(s)
      testStepper.step(steps, dir,speed);
      
#[stepPin, directionPin, enablePin]
##s1=[2,3,4]     #3,5,7--Rpi pins
s1=[6,13,4]    #31,33,7--Rpi pins
s2=[17,27,22]  #11,13,15
s3=[20,21,11]   #38,40,23
##s3=[10,9,11]   #19,21,23

######### Link Lenghts in cm.
l1=42
l2=35.6
######## Coordinates in xy frame in cm
hx = 17.8
hy = 18.4
hz = 0

htheta2=-math.degrees(math.acos((hx*hx+hy*hy-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
htheta1=math.degrees(math.atan(hy/hx) - math.atan((l2*math.sin(htheta2*math.pi/180))/(l1 + l2*math.cos(htheta2*math.pi/180))))
htheta3=math.degrees(math.acos(hz/(l1*math.cos(htheta1*math.pi/180) + l2*math.cos((htheta2 + htheta1)*math.pi/180))))

ox = 17.8
oy = 18.4
oz = 0
#######Inverse Kinematics Equation for obtaining th joint angles -
oldtheta2=-math.degrees(math.acos((ox*ox+oy*oy-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
oldtheta1=math.degrees(math.atan(oy/ox) - math.atan((l2*math.sin(oldtheta2*math.pi/180))/(l1 + l2*math.cos(oldtheta2*math.pi/180))))
oldtheta3=math.degrees(math.acos(oz/(l1*math.cos(oldtheta1*math.pi/180) + l2*math.cos((oldtheta2 + oldtheta1)*math.pi/180))))
print(str(oldtheta1)+" oldtheta2:"+str(oldtheta2)+ " oldtheta3:"+str(oldtheta3))
ppr=1600  # Pulse Per Revolution

x = 34
y = height
z = 0

                        ##Error compensation for Linear Motion.
##y = (0.04 * (x - ox)) - y
##y = (0.04 * (ox - x)) - y

##y = (0.04 * (x - ox)) - y
##if ox == hx and oy == hy:
##    print(" Equal ")
##else:
##    y = (0.04 * (x - ox)) - y

##y = (0.04 * (x - ox)) - y        

theta2=-math.degrees(math.acos((x*x+y*y-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
theta1=math.degrees(math.atan(y/x) - math.atan((l2*math.sin(theta2*math.pi/180))/(l1 + l2*math.cos(theta2*math.pi/180))))
theta3=math.degrees(math.acos(z/(l1*math.cos(theta1*math.pi/180) + l2*math.cos((theta2 + theta1)*math.pi/180))))

# angles to be moved
oa1=oldtheta3 - htheta3 #base
oa2=oldtheta1 - htheta1 #link 1
oa3=oldtheta2 - htheta2 #link 2

na1=theta3 - htheta3 #base
na2=theta1 - htheta1 #link 1
na3=theta2 - htheta2 #link 2

a1 = na1 - oa1
a2 = na2 - oa2
a3 = na3 - oa3

print(str(theta1)+" theta2:"+str(theta2)+ " theta3:"+str(theta3))
print(str(a1)+" a2:"+str(a2)+ " a3:"+str(a3))

##a1=0  #base
##a2=-39  #link 1
##a3=0  #link 2

## Gear Ratios
g1=12.22222222222
g2=10
g3=10
 
# Calculation for step and Speed
step1=(ppr/360)*a1*g1  
#speed1=0.01

step2=(ppr/360)*a2*g2
#speed2=0.01

step3=(ppr/360)*a3*g3  
#speed3=0.01

# Calculation of timedelay for differnt motors
execTime=10

##td1=abs((execTime-(step1*0.002))/step1)
##td2=abs((execTime-(step2*0.002))/step2)
##td3=abs((execTime-(step3*0.002))/step3)

if (step1 == 0):
    td1 = 0
else :
##    td1=abs((execTime-(step1*0.002))/step1)
    td1 = execTime/step1

if (step2 == 0):
    td2 = 0
else:
##    td2=abs((execTime-(step2*0.002))/step2)
    td2 = execTime/step2

if (step3 == 0) :
    td3 = 0
else:
##    td3=abs((execTime-(step3*0.002))/step3)
    td3 = execTime/step3

print(td1)
print(td2)
print(td3)

if step1<0:
    dir1="r"
else:
    dir1="l"
    
if step2<0:
    dir2="l"
else:
    dir2="r"

if step3<0:
    dir3="l"
else:
    dir3="r"

_thread.start_new_thread( print_time, ("stepper-1", 0.2, s1,abs(step1),dir1,td1))
_thread.start_new_thread( print_time, ("stepper-2", 0.2, s2,abs(step2),dir2,td2))
_thread.start_new_thread( print_time, ("stepper-3", 0.2, s3,abs(step3),dir3,td3)) 


time.sleep(15)

for a in range(5):
    def func2():
        ox = [34,36,38,40,42,44,46,48,50,52,54,56,58]
        
        for x in ox:
            ##ox[5] = {40 45 50 55 60}
            
            oy = height
            oz = 0
            
            oldtheta2=-math.degrees(math.acos((x*x+oy*oy-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
            oldtheta1=math.degrees(math.atan(oy/x) - math.atan((l2*math.sin(oldtheta2*math.pi/180))/(l1 + l2*math.cos(oldtheta2*math.pi/180))))
            oldtheta3=math.degrees(math.acos(oz/(l1*math.cos(oldtheta1*math.pi/180) + l2*math.cos((oldtheta2 + oldtheta1)*math.pi/180))))

            print(" oldtheta1:" + str(oldtheta1)+" oldtheta2:"+ str(oldtheta2)+ " oldtheta3:"+ str(oldtheta3))
            ppr=1600  # Pulse Per Revolution

            nx = x+2 ##{45,50,55,60,65}
            ny = height
            nz = 0
            #ny = (0.04 * (nx - x)) - ny
            
            theta2=-math.degrees(math.acos((nx*nx+ny*ny-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
            theta1=math.degrees(math.atan(ny/nx) - math.atan((l2*math.sin(theta2*math.pi/180))/(l1 + l2*math.cos(theta2*math.pi/180))))
            theta3=math.degrees(math.acos(nz/(l1*math.cos(theta1*math.pi/180) + l2*math.cos((theta2 + theta1)*math.pi/180))))
                
            oa1=oldtheta3 - htheta3 #base
            oa2=oldtheta1 - htheta1 #link 1
            oa3=oldtheta2 - htheta2 #link 2

            na1=theta3 - htheta3 #base
            na2=theta1 - htheta1 #link 1
            na3=theta2 - htheta2 #link 2

            a1 = na1 - oa1
            a2 = na2 - oa2
            a3 = na3 - oa3
            
            ## Gear Ratios
            g1=12.22222222222
            g2=10
            g3=10
            # Calculation for step and Speed
            step1=(ppr/360)*a1*g1  
            step2=(ppr/360)*a2*g2
            step3=(ppr/360)*a3*g3
            
            # Calculation of timedelay for differnt motors ###############
            execTime=5
            
            if (step1 == 0):
                td1 = 0
            else :
                td1 = execTime/step1
            if (step2 == 0):
                td2 = 0
            else:
                td2 = execTime/step2
            if (step3 == 0) :
                td3 = 0
            else:
                td3 = execTime/step3
            print(td1)
            print(td2)
            print(td3)

            if step1<0:
                dir1="r"
            else:
                dir1="l"   
            if step2<0:
                dir2="l"
            else:
                dir2="r"
            if step3<0:
                dir3="l"
            else:
                dir3="r"    
            _thread.start_new_thread( print_time, ("stepper-1", 0.2, s1,abs(step1),dir1,td1))
            _thread.start_new_thread( print_time, ("stepper-2", 0.2, s2,abs(step2),dir2,td2))
            _thread.start_new_thread( print_time, ("stepper-3", 0.2, s3,abs(step3),dir3,td3))
            time.sleep(0.2)
            oy= oy + 0.75
            
            
    func2()

    time.sleep(5)

    def func3():
        ox = [60,58,56,54,52,50,48,46,44,42,40,38,36]
        for x in ox:
            ##ox[5] = {40 45 50 55 60}
            
            oy = height
            oz = 0
            
            oldtheta2=-math.degrees(math.acos((x*x+oy*oy-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
            oldtheta1=math.degrees(math.atan(oy/x) - math.atan((l2*math.sin(oldtheta2*math.pi/180))/(l1 + l2*math.cos(oldtheta2*math.pi/180))))
            oldtheta3=math.degrees(math.acos(oz/(l1*math.cos(oldtheta1*math.pi/180) + l2*math.cos((oldtheta2 + oldtheta1)*math.pi/180))))

            print(" oldtheta1:" + str(oldtheta1)+" oldtheta2:"+ str(oldtheta2)+ " oldtheta3:"+ str(oldtheta3))
            ppr=1600  # Pulse Per Revolution

            nx = x-2 ##{45,50,55,60,65}
            ny = height
            nz = 0
            #ny = (0.04 * (nx - x)) - ny
            
            theta2=-math.degrees(math.acos((nx*nx+ny*ny-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
            theta1=math.degrees(math.atan(ny/nx) - math.atan((l2*math.sin(theta2*math.pi/180))/(l1 + l2*math.cos(theta2*math.pi/180))))
            theta3=math.degrees(math.acos(nz/(l1*math.cos(theta1*math.pi/180) + l2*math.cos((theta2 + theta1)*math.pi/180))))
                
            oa1=oldtheta3 - htheta3 #base
            oa2=oldtheta1 - htheta1 #link 1
            oa3=oldtheta2 - htheta2 #link 2

            na1=theta3 - htheta3 #base
            na2=theta1 - htheta1 #link 1
            na3=theta2 - htheta2 #link 2

            a1 = na1 - oa1
            a2 = na2 - oa2
            a3 = na3 - oa3
            
            ## Gear Ratios
            g1=12.22222222222
            g2=10
            g3=10
            # Calculation for step and Speed
            step1=(ppr/360)*a1*g1  
            step2=(ppr/360)*a2*g2
            step3=(ppr/360)*a3*g3
            
            # Calculation of timedelay for differnt motors
            execTime=5
            
            if (step1 == 0):
                td1 = 0
            else :
                td1 = execTime/step1
            if (step2 == 0):
                td2 = 0
            else:
                td2 = execTime/step2
            if (step3 == 0) :
                td3 = 0
            else:
                td3 = execTime/step3
            print(td1)
            print(td2)
            print(td3)

            if step1<0:
                dir1="r"
            else:
                dir1="l"   
            if step2<0:
                dir2="l"
            else:
                dir2="r"
            if step3<0:
                dir3="l"
            else:
                dir3="r"    
            _thread.start_new_thread( print_time, ("stepper-1", 0.2, s1,abs(step1),dir1,td1))
            _thread.start_new_thread( print_time, ("stepper-2", 0.2, s2,abs(step2),dir2,td2))
            _thread.start_new_thread( print_time, ("stepper-3", 0.2, s3,abs(step3),dir3,td3))
            time.sleep(0.2)
            oy= oy - 0.75

    func3()

    time.sleep(5)

    step_count = 300
    delay = 0.005

    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        
ox = 34
oy = height
oz = 0
            
oldtheta2=-math.degrees(math.acos((ox*ox+oy*oy-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
oldtheta1=math.degrees(math.atan(oy/ox) - math.atan((l2*math.sin(oldtheta2*math.pi/180))/(l1 + l2*math.cos(oldtheta2*math.pi/180))))
oldtheta3=math.degrees(math.acos(oz/(l1*math.cos(oldtheta1*math.pi/180) + l2*math.cos((oldtheta2 + oldtheta1)*math.pi/180))))

print(" oldtheta1:" + str(oldtheta1)+" oldtheta2:"+ str(oldtheta2)+ " oldtheta3:"+ str(oldtheta3))
ppr=1600  # Pulse Per Revolution

nx = 17.8 
ny = 18.4
nz = 0
            #ny = (0.04 * (nx - x)) - ny
theta2=-math.degrees(math.acos((nx*nx+ny*ny-(l1*l1)-(l2*l2))/ (2*l1*l2)))  
theta1=math.degrees(math.atan(ny/nx) - math.atan((l2*math.sin(theta2*math.pi/180))/(l1 + l2*math.cos(theta2*math.pi/180))))
theta3=math.degrees(math.acos(nz/(l1*math.cos(theta1*math.pi/180) + l2*math.cos((theta2 + theta1)*math.pi/180))))
                
oa1=oldtheta3 - htheta3 #base
oa2=oldtheta1 - htheta1 #link 1
oa3=oldtheta2 - htheta2 #link 2

na1=theta3 - htheta3 #base
na2=theta1 - htheta1 #link 1
na3=theta2 - htheta2 #link 2

a1 = na1 - oa1
a2 = na2 - oa2
a3 = na3 - oa3
            
## Gear Ratios
g1=12.22222222222
g2=10
g3=10
# Calculation for step and Speed
step1=(ppr/360)*a1*g1
step2=(ppr/360)*a2*g2
step3=(ppr/360)*a3*g3

# Calculation of timedelay for differnt motors
execTime=5

if (step1 == 0):
    td1 = 0
else :
    td1 = execTime/step1
if (step2 == 0):
    td2 = 0
else:
    td2 = execTime/step2
if (step3 == 0) :
    td3 = 0
else:
    td3 = execTime/step3
    
print(td1)
print(td2)
print(td3)

if step1<0:
    dir1="r"
else:
    dir1="l"   
if step2<0:
    dir2="l"
else:
    dir2="r"
if step3<0:
    dir3="l"
else:
    dir3="r"    
            
_thread.start_new_thread( print_time, ("stepper-1", 0.2, s1,abs(step1),dir1,td1))
_thread.start_new_thread( print_time, ("stepper-2", 0.2, s2,abs(step2),dir2,td2))
_thread.start_new_thread( print_time, ("stepper-3", 0.2, s3,abs(step3),dir3,td3))
time.sleep(0.2)

step_count = 1800
delay = 0.005
GPIO.output(DIR, CCW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)


    


