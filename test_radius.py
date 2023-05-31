import time
import RPi.GPIO as GPIO
from car_code.MotorModule_2 import Motor2
import threading

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

motor = Motor2(6,16,19,12,20,26)
    
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50)
servo1.start(0)

t1 = threading.Thread(target = encoder)
t1.start()


servo1.ChangeDutyCycle(7+(67/18))
time.sleep(2)
while counter2 >= -4000:    
    motor.moveB_no_stop(35)
    # print(counter)
# print(counter)
motor.stop(2)
servo1.ChangeDutyCycle(0)
print(counter2)




