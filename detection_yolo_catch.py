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
from yolov3.utils import detect_image, detect_realtime, detect_video, Load_Yolo_model, detect_video_realtime_mp,draw_location,detect_realtime_little,detect_realtime_once
from yolov3.configs import *

from gpiozero import LineSensor
from car_code.MotorModule_2 import Motor2 
import time
import RPi.GPIO as GPIO
import threading

yolo = Load_Yolo_model()

detect = 'detect_no_car'

final_location = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))
# detect_realtime_once(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))

print('final_location',final_location)