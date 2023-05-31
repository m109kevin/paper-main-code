# 7,11,8,9,25

# left = 8
# mid_left = 11
# mid = 7
# mid_right = 9
# right = 25
from gpiozero import LineSensor
from MotorModule_2 import Motor2
import time
import RPi.GPIO as GPIO
import threading


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
                servo1.ChangeDutyCycle(7+(4/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)
            elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 1 and right == 0:
                servo1.ChangeDutyCycle(7+(9/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)
            elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 1:
                servo1.ChangeDutyCycle(7+(16/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)        
            elif left == 0 and mid_left == 1 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(-1/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)    
            elif left == 1 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(-8/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)

            else:
                servo1.ChangeDutyCycle(7+(4/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)


def motor_go_straight():
    motor = Motor2(6,16,19,12,20,26)
    time.sleep(3)
    while action:
        if go_motor:
            motor.moveF_no_stop(25)
        # elif back:
            # motor.moveB_no_stop(25)
        else:
            motor.stop(5)
            # counter_average = (counter+counter2)/2
            print('counter:',counter)
            print('counter2:',counter2)
            # print('counter_average:',counter_average)
            
        
   
def encoder():
    # counter is right
    # counter2 is left
    global counter
    global counter2
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

    while action:
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


def main_program():
    i = 1
    global go_motor
    global go_sensor
    global action
    go = True
    while action:
        d = i*1000
        # print('d',d)
        if counter2 >= d:
            go_motor = False
            time.sleep(1)
            go_sensor = False
            time.sleep(2)
            print('yolo detect')
            time.sleep(2)
            go_sensor = True
            time.sleep(1)
            go_motor = True
            i += 1
        if d > 8000:
            go_motor = False
            go_sensor = False
            action = False
            break
'''
def move_back():
    i = 3
    global back
    global action
    back = True
    while action:
        d = i*1000
        # print('d',d)
        if counter <= d:
            back = False
            time.sleep(2)
            print('yolo detect')
            time.sleep(2)
            back = True
            i -= 1
        if d < 0:
            back = False
            break
'''       
action = True
go_sensor = True
go_motor = True
counter = 0
# back = False
t1 = threading.Thread(target = encoder)
t2 = threading.Thread(target = motor_go_straight)
t3 = threading.Thread(target = line_sensor)



t1.start()
t3.start()
t2.start()
main_program()


        
