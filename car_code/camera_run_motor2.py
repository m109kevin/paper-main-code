from picamera import PiCamera
from MotorModule_2 import Motor2
import threading
import time

from gpiozero import LineSensor
import RPi.GPIO as GPIO
"""set camera"""
camera = PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 60
# 開啟預覽
camera.start_preview()
#---------------------------------
# linesensor set
'''
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

#----------------------------

def line_sensor():
    while action:
        if go:
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
                servo1.ChangeDutyCycle(7+(11/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)
            elif left == 0 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 1:
                servo1.ChangeDutyCycle(7+(18/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)        
            elif left == 0 and mid_left == 1 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(-3/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)    
            elif left == 1 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(-10/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)

            else:
                servo1.ChangeDutyCycle(7+(4/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)
                
'''
run = Motor2(6,16,19,12,20,26)
def Run():
    print('run')
    for n in range(60):
        for n in range(16):
            run.moveF(30,1)
            run.stop(2)
        # action = False
        for n in range(14):
            run.moveB(30,1)
            run.stop(2)
        # action = True
    run.stop(0)
def Ca(times,t):
    for i in range(times):
        n = i + 1
        camera.capture('/home/pi/Desktop/TensorFlow-2.x-YOLOv3/car_code/picture/pic/' + str(n) +'.jpg')
        #print(n)
        time.sleep(t)    

action = True
go = True
t1 = threading.Thread(target = Ca ,args=(600,0.1,))
t1.start()
t2 = threading.Thread(target = Run ,args=())
t2.start()
# line_sensor()



camera.stop_preview()
print('end')