#================================================================
#
#   File name   : detection_demo.py
#   Author      : PyLessons
#   Created date: 2020-09-27
#   Website     : https://pylessons.com/
#   GitHub      : https://github.com/pythonlessons/TensorFlow-2.x-YOLOv3
#   Description : object detection image and video example
#
#================================================================
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import cv2
import numpy as np
import tensorflow as tf
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp,draw_location,detect_realtime_little
from yolov3.configs import *

from gpiozero import LineSensor
from car_code.MotorModule_2 import Motor2 
import time
import RPi.GPIO as GPIO
import threading
import math

yolo = Load_Yolo_model()

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
                servo1.ChangeDutyCycle(7+(-1/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)    
            elif left == 1 and mid_left == 0 and mid == 0 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(-6/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)

            else:
                servo1.ChangeDutyCycle(7+(8/18))
                time.sleep(0.2)
                servo1.ChangeDutyCycle(0)


def motor_go_straight():
    motor = Motor2(6,16,19,12,20,26)
    while action:            
        if go_motor:
            motor.moveF_no_stop(24)
        # elif back:
            # motor.moveB_no_stop(25)            
        else:
            motor.stop(8)
            print('counter',counter)
            print('counter2',counter2)
   
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
        # if counter%100 == 0:
            # print('disctance1:',counter)

        A2 = GPIO.input(A_pin2)
        B2 = GPIO.input(B_pin2)
        current_AB2 = (A2<<1) | B2
        position2 = (last_AB2<<2) | current_AB2
        counter2 += outcome2[position2]
        last_AB2 = current_AB2
        # print('distance2:',counter2)


def main_program():
    i = 1
    global go_motor
    global back_motor
    global go_sensor
    global action
    while action:
        d = i*500
        # print('d',d)
        if counter >= d:
            go_motor = False
            time.sleep(1)
            go_sensor = False
            time.sleep(2)
            final_location = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))
            
            if final_location == None:
                print('detect_no_number')             
            else:
                # detect = final_location[0]
                # location = final_location[1]
                print('final_detect = ',final_location[0])
                print('final_location = ',final_location[1])
                if final_location[0] == 'detect_no_car':
                    return final_location[1]
                    break
            time.sleep(2)
            go_sensor = True
            time.sleep(1)
            go_motor = True
            i += 1
'''   
        if  d > 3000:
            go = False
            action = False
            return final_location
            break
'''            
action = True
go_motor = True
go_sensor = True
# back = False
detect = 'detect_no_car'

t1 = threading.Thread(target = encoder)
t2 = threading.Thread(target = motor_go_straight)
t3 = threading.Thread(target = line_sensor)



t1.start()
time.sleep(3)
t3.start()
# time.sleep(1)
t2.start()
final_location = main_program()
print('final_location',final_location)

counter = 0
unit_yolo_distance = 347/45
print('unit_yolo_distance',unit_yolo_distance)
real_distance = (final_location -350)/unit_yolo_distance
print('real_distance',real_distance)

unit_encoder_distance = 25
print('unit_encoder_distance',unit_encoder_distance)
target_distance = 81 - real_distance
print('target_distance',target_distance)
encoder_distance = target_distance*unit_encoder_distance
print('encoder_distanc',encoder_distance)
print('counter',counter)


time.sleep(2)
go_sensor = True
time.sleep(2)
go_motor = True
while True:
    if counter >= encoder_distance:
        go_motor = False
        time.sleep(1)
        go_sensor = False
        time.sleep(2)
        location_pre = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))
        if location_pre == None:
            print('cant catch')
        else:
            location_pre =  location_pre[1]
        break
print('location_pre',location_pre)

counter = 0
real_distance = (location_pre -350)/unit_yolo_distance
print('real_distance',real_distance)
target_distance = 28 - real_distance
print('target_distance',target_distance)
encoder_distance = target_distance*unit_encoder_distance
print('encoder_distance',encoder_distance)
print('counter',counter)
if target_distance <= 0:
    object_location = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))
    if object_location == None:
        print('cant catch')
    else:
        object_location =  object_location[1]
else:
    time.sleep(2)
    go_sensor = True
    time.sleep(2)
    go_motor = True
    while True:
        if counter >= encoder_distance:
            go_motor = False
            time.sleep(1)
            go_sensor = False
            time.sleep(2)
            object_location = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))
            if object_location == None:
                print('cant catch')
            else:
                object_location =  object_location[1]
            break
print('object_location',object_location)

dubins_y = (object_location-350)/unit_yolo_distance + 30
print('dubins_y',dubins_y)

x = 70
y = dubins_y
a = math.atan(x/y)
b = math.atan(x/y)
cosa = math.cos(a)
cosb = math.cos(b)
sina = math.sin(a)
sinb = math.sin(b)
D = math.sqrt(x**2 + y**2)
d = D/29.15


p = math.sqrt(d**2 - 2 + 2*math.cos(a - b) - 2*d*(sina + sinb))
t = a - math.atan((cosa + cosb)/(d - sina - sinb)) + math.atan(2/p)
q = b - math.atan((cosa + cosb)/(d - sina - sinb)) + math.atan(2/p)
print(t,p,q)

