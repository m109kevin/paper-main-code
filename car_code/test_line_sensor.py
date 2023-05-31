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



while True:
    left = GPIO.input(8)
    mid_left = GPIO.input(11)
    mid = GPIO.input(7)
    mid_right = GPIO.input(9)
    right = GPIO.input(25)
    if left == 0 and mid_left == 0 and mid == 1 and mid_right == 0 and right == 0:
        servo1.ChangeDutyCycle(7+(4/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
    elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 1 and right == 0:
        servo1.ChangeDutyCycle(7+(14/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
    elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 1:
        servo1.ChangeDutyCycle(7+(24/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)        
    elif left == 0 and mid_left == 1 and mid == 0 and mid_right == 0 and right == 0:
        servo1.ChangeDutyCycle(7+(-6/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)    
    elif left == 1 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 0:
        servo1.ChangeDutyCycle(7+(-16/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)

    else:
        servo1.ChangeDutyCycle(7+(4/18))
        time.sleep(0.5)
        servo1.ChangeDutyCycle(0)
