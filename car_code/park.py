import time
import RPi.GPIO as GPIO
from MotorModule_2 import Motor2
import threading
from gpiozero import LineSensor
#-----------------------------------------------------
#servo control


#------------------------------------------------------
#line sensor
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50)

servo1.start(0)
    
GPIO.setup(8,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(7,GPIO.IN)
GPIO.setup(9,GPIO.IN)
GPIO.setup(25,GPIO.IN)

def line_sensor():
    time.sleep(2)
    while action:
        if go_sensor:
            left = GPIO.input(8)
            mid_left = GPIO.input(11)
            mid = GPIO.input(7)
            mid_right = GPIO.input(9)
            right = GPIO.input(25)
            if left == 0 and mid_left == 0 and mid == 1 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(8/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)
            elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 1 and right == 0:
                servo1.ChangeDutyCycle(7+(12/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)
            elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 1:
                servo1.ChangeDutyCycle(7+(17/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)        
            elif left == 0 and mid_left == 1 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(1/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)    
            elif left == 1 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(-6/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)

            else:
                servo1.ChangeDutyCycle(7+(6/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)

#------------------------------------------------------
#motor control
def motor_go_straight():
    # motor = Motor2(6,16,19,12,20,26)
    time.sleep(3)
    while action:
        if go_motor:
            motor.moveF_no_stop(25)
        # elif back:
            # motor.moveB_no_stop(25)
        else:
            motor.stop(2)
            # counter_average = (counter+counter2)/2
            print('counter:',counter)
            print('counter2:',counter2)
            # print('counter_average:',counter_average)

#----------------------------------------------------------------
#encoder
def encoder():
    # counter is right
    # counter2 is left
    global counter
    global counter2
    # global reset_counter
    A_pin = 17
    B_pin = 18
    
    A_pin2 = 22
    B_pin2 = 23


    GPIO.setup(A_pin,GPIO.IN)
    GPIO.setup(B_pin,GPIO.IN)
    
    GPIO.setup(A_pin2,GPIO.IN)
    GPIO.setup(B_pin2,GPIO.IN)

    outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
    last_AB = 0b00
    counter = 0

    outcome2 = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
    last_AB2 = 0b00
    counter2 = 0

    while True:
        # if reset_counter:
            # counter = 0
            # reset_counter = False
            
        A = GPIO.input(A_pin)
        B = GPIO.input(B_pin)
        current_AB = (A<<1) | B
        position = (last_AB<<2) | current_AB
        counter += outcome[position]
        last_AB = current_AB
        #if counter % 100 == 0:
        #print('disctance1:',counter)

        A2 = GPIO.input(A_pin2)
        B2 = GPIO.input(B_pin2)
        current_AB2 = (A2<<1) | B2
        position2 = (last_AB2<<2) | current_AB2
        counter2 += outcome2[position2]
        last_AB2 = current_AB2
        #print('distance2:',counter2)

#------------------------------------------------
#main program
def parking():
    i = 1
    global go_motor
    global go_sensor
    global action
    go = True
    while action:
        d = 1900
        # print('d',d)
        if counter2 >= d:
            go_motor = False
            time.sleep(1)
            go_sensor = False
            time.sleep(1)
            action = False
            print('arrive point')
            time.sleep(1)
            break

action = True
go_sensor = True
go_motor = True
# reset_counter = False


motor = Motor2(6,16,19,12,20,26) # motor set

t1 = threading.Thread(target = encoder)
t2 = threading.Thread(target = motor_go_straight)
t3 = threading.Thread(target = line_sensor)

t1.start()
'''
t3.start()
t2.start()
parking()
'''
#test rotation radius--------------------------------
servo1.ChangeDutyCycle(7+(-36/18))
time.sleep(1)
while counter2 >= -2000:    
    motor.moveB_no_stop(35)
# print(counter)
motor.stop(2)
servo1.ChangeDutyCycle(0)
print(counter)



# test straight------------------------------------------------------
# servo1.ChangeDutyCycle(7+(8/18))
# time.sleep(0.2)
# motor.moveF(30,10)
# motor.stop(0)
# servo1.ChangeDutyCycle(0)

'''
error = counter2 - 1800
print(error)
time.sleep(1)
if error >= 100:
    servo1.ChangeDutyCycle(7+(4/18))
    time.sleep(1)
    target = counter2-error*0.5
    print(target)
    while counter2 >= target:    
        motor.moveB_no_stop(25)
        # print(counter)
    servo1.ChangeDutyCycle(0)
    motor.stop(2)
    print('counter2_fix:',counter2)
    print('---------------')
    time.sleep(1)


#reset_counter = True
counter = 0
print('counter_L:',counter)

servo1.ChangeDutyCycle(7+(72/18))
time.sleep(1)
while counter >= -800:    
    motor.moveB_no_stop(30)
    # print(counter)
motor.stop(2)
print(counter)
error_L = counter + 800
print('error_L:',error_L)
time.sleep(1)

target = counter - error*0.5
print('target:',target)
while counter <= target:    
    motor.moveB_no_stop(25)
    # print(counter)
servo1.ChangeDutyCycle(0)
motor.stop(2)
print('counter_L_fix:',counter)
print('---------------')
time.sleep(1)

servo1.ChangeDutyCycle(0)
motor.stop(2)
print('counter_L:',counter)
print('---------------')
time.sleep(1)

#reset_counter = True
counter = 0
print('counter_S:',counter)
time.sleep(2)

servo1.ChangeDutyCycle(7+(4/18))
time.sleep(1)
while counter >= -1500:    
    motor.moveB_no_stop(25)
    # print(counter)
servo1.ChangeDutyCycle(0)
motor.stop(2)
print('counter_S:',counter)
print('---------------')
time.sleep(1)

# reset_counter = True
counter = 0
print('counter_R:',counter)
time.sleep(2)

servo1.ChangeDutyCycle(7+(-36/18))
time.sleep(1)
while counter >= -1300:    
    motor.moveB_no_stop(30)
    # print(counter)
servo1.ChangeDutyCycle(0)
motor.stop(2)
print('counter_R:',counter)
'''





