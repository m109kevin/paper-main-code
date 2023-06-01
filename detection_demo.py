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

# 載入yolo model進行辨識座標
yolo = Load_Yolo_model()

GPIO.setmode(GPIO.BCM) # 使用GPIO的引腳編號（BCM編號）來標識GPIO引腳。
GPIO.setwarnings(False) # 清除GPIO設定

GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50) #設定角位，脈衝頻率，脈衝頻率越高馬達轉速越快

servo1.start(0)
    
# 設定5個紅外線感測器的角位，用來循跡前進
GPIO.setup(8,GPIO.IN)
GPIO.setup(11,GPIO.IN)
GPIO.setup(7,GPIO.IN)
GPIO.setup(9,GPIO.IN)
GPIO.setup(25,GPIO.IN)

# 伺服馬達的 10step = 180度 1step = 18度
# 定義7 = 90度 8 = 108度 6 = 72度....
def line_sensor():
    while action:
        if go_sensor:
            left = GPIO.input(8)
            mid_left = GPIO.input(11)
            mid = GPIO.input(7)
            mid_right = GPIO.input(9)
            right = GPIO.input(25)
            if left == 0 and mid_left == 0 and mid == 1 and mid_right == 0 and right == 0:
                servo1.ChangeDutyCycle(7+(8/18)) # 定義馬達旋轉角度
                time.sleep(0.2) # 給馬達0.2秒的時間旋轉
                servo1.ChangeDutyCycle(0) # 將馬達斷電
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

# 讓車直線前進
# 請看car_code.MotorModule_2 的 Motor2
def motor_go_straight():
    motor = Motor2(6,16,19,12,20,26) # 設定2個馬達輪子的腳位
    while action:            
        if go_motor:
            motor.moveF_no_stop(24)
        # elif back:
            # motor.moveB_no_stop(25)            
        else:
            motor.stop(8)
            print('counter',counter)
            print('counter2',counter2)

# 利用馬達上的旋轉編碼器計算距離 
def encoder():
    # counter is right
    # counter2 is left
    global counter  # 設定全域變數counter和counter2來計算2個輪胎前進的距離
    global counter2
    A_pin = 17 #設定右馬達角位
    B_pin = 18
    A_pin2 = 22 #設定左馬達角位
    B_pin2 = 23


    GPIO.setup(A_pin,GPIO.IN)
    GPIO.setup(B_pin,GPIO.IN)
    GPIO.setup(A_pin2,GPIO.IN)
    GPIO.setup(B_pin2,GPIO.IN)

    # 論文第40頁 
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
        position = (last_AB<<2) | current_AB # 前一瞬間跟後一瞬間的A,B值決定counter的變化
        counter += outcome[position] # 決定counter要+1, -1 or 不變
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

# 定義主程式
def main_program():
    i = 1
    global go_motor #控制車子前進
    global back_motor
    global go_sensor # 控制伺服馬達
    global action 
    while action:
        d = i*500 
        # print('d',d)
        if counter >= d: # 每500個counter
            go_motor = False # 車子停下來
            time.sleep(1)
            go_sensor = False # 伺服馬達斷電
            time.sleep(2)
            # detect_realtime_little 請看yolov3.utils 的detect_realtime_little函式
            # detect_realtime_little 由 detect_realtime修改
            final_location = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0))
            # final_location是一個大小為2的list
            # final_location[0] = 'detect_car' or 'detect_no_car'代表是否有在右方辨識出車子 
            # final_location[1] = 數字右邊框的座標
            
            if final_location == None: #沒辨識到數字時的情況，但基本上不應該發生
                print('detect_no_number')             
            else:
                # detect = final_location[0]
                # location = final_location[1]
                print('final_detect = ',final_location[0])
                print('final_location = ',final_location[1])
                if final_location[0] == 'detect_no_car': #如果右邊沒發現車子，代表發現停車位，return 數字右邊框的座標，停止while迴圈，準備停車程序
                    return final_location[1]

            # 沒發現車位時
            time.sleep(2)
            go_sensor = True # 伺服馬達啟動
            time.sleep(1)
            go_motor = True # 車輛繼續前進，直到發現車位
            i += 1
'''   
        if  d > 3000:
            go = False
            action = False
            return final_location
            
'''         
# 由於效能的限制，實驗中將yolov3辨識和編碼器以外的其他執行緒分開進行 
# 定義全域變數，控制車輛前進，伺服馬達控制和整個前進程序的開關  
# 辨識時關掉另外的程序，避免raspberry pi4負荷不了
action = True
go_motor = True
go_sensor = True
# back = False
detect = 'detect_no_car'

t1 = threading.Thread(target = encoder)
t2 = threading.Thread(target = motor_go_straight)
t3 = threading.Thread(target = line_sensor)

t1.start() # 開啟編碼器程序
time.sleep(3)
t3.start() # 開啟紅外線追跡程序
# time.sleep(1)
t2.start() # 車輛前進
final_location = main_program() # 運行主程序main_program()，直到return 數字右邊框座標
print('final_location',final_location)

# 得到數字右邊框座標後，計算車輛與車位的y方向相對座標(參考論文36-40頁)

counter = 0
unit_yolo_distance = 347/45 # 參考論文38頁(分別取278, -10)和(625, 35)2個點，625 - 278 = 347，35 -(-10) = 45，由於數據非常近似線性關係，所以相除後可以得到座標和實際距離的關係
print('unit_yolo_distance',unit_yolo_distance)
real_distance = (final_location -350)/unit_yolo_distance # 自走車在座標原點時，辨識數字的x座標為350，由此公式得出實際y座標
print('real_distance',real_distance)

unit_encoder_distance = 25 # 經過多次測量平均，自走車每前進1cm，編碼器的counter約增加25，相除後得到每前進1單位(cm)編碼器增加的值
print('unit_encoder_distance',unit_encoder_distance)
target_distance = 81 - real_distance # 由於實驗環境，車位大小...等因素，理想的目標為y = 81處，81 - real_distance得到需前進的距離
print('target_distance',target_distance)
encoder_distance = target_distance*unit_encoder_distance # 由需前進的距離，乘上unit_encoder_distance後得到需前進多少counter
print('encoder_distanc',encoder_distance)
print('counter',counter)


time.sleep(2)
go_sensor = True # 開啟紅外線追跡
time.sleep(2)
go_motor = True # 車輛前進
while True:
    if counter >= encoder_distance: # 如果到達目的地
        go_motor = False # 車輛停止
        time.sleep(1)
        go_sensor = False # 紅外線追跡停止
        time.sleep(2)
        # 因為車子沒煞車，所以基本上不會準確地停在目的地
        # 所以要在辨識一次座標，避免誤差
        location_pre = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0)) 
        if location_pre == None:
            print('cant catch')
        else:
            location_pre =  location_pre[1]
        break
print('location_pre',location_pre)

# 同上辨識座標流程，但這次辨識的目標為之前辨識數字的下一號(例如上面辨識的數字為2，此次辨識的目標就為3)
# 參考論文第53頁
counter = 0
real_distance = (location_pre -350)/unit_yolo_distance # 算出實際距離
print('real_distance',real_distance)
target_distance = 28 - real_distance # 目的地約為28cm處
print('target_distance',target_distance)
encoder_distance = target_distance*unit_encoder_distance
print('encoder_distance',encoder_distance)
print('counter',counter)
if target_distance <= 0: # 自走車超過28cm處
    object_location = detect_realtime_little(yolo, '', input_size=YOLO_INPUT_SIZE, show=True, rectangle_colors=(255, 0, 0)) # 在辨識一次座標
    if object_location == None:
        print('cant catch')
    else:
        object_location =  object_location[1] # 得到實際座標object_location
else: # 座標小於28時怕y座標值不夠導致無法計算出正確的dubins曲線(參考論文44-46)，所以要在前進一小段距離後再辨識座標
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

# 以下參考論文44-46頁和53頁
# 算得3倒車的3段路徑p, t, q
dubins_y = (object_location-350)/unit_yolo_distance + 39.25
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
d = D/29.15 # 用伺服馬達調整前輪角度，使得前輪造成的旋轉半徑為29.5公分(參考論文第35頁)


p = math.sqrt(d**2 - 2 + 2*math.cos(a - b) - 2*d*(sina + sinb))
t = a - math.atan((cosa + cosb)/(d - sina - sinb)) + math.atan(2/p)
q = b - math.atan((cosa + cosb)/(d - sina - sinb)) + math.atan(2/p)
print(t,p,q)

# 後續為倒車程序
# 有p, t, q後，車輛倒退時由編碼器計算距離，當計算的距離 = p, t, q時停車，走完3段路徑即完成自動停車
# 後續程序放在實驗室雲端
