# A:6(EnA),16,19 (left)
# B:12(EnB),20,26 (right)
from picamera import PiCamera
from MotorModule_1 import Motor1
from Encoder_object import Encoder
import threading 
import time
"""set camera"""
camera = PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 60
# 開啟預覽
camera.start_preview()

def Camera(times,t):
    for i in range(times):
        camera.capture('/home/pi/Desktop/car_code/picture/' + str(i) +'.jpg')
        print(i+1)
        time.sleep(t) 


encoder_right = Encoder(17,18)
encoder_left = Encoder(22,23)

def en_right(right):
    encoder_right.Run(right)
def en_left(left):
    encoder_left.Run(left)

run_right = Motor1(12,20,26)
run_left = Motor1(6,16,19)
 
def Run_r(speed,t):
    print('run_r')
    run_right.moveF(100,0.5)
    run_right.moveF(speed,t)
    run_right.stop(0)
def Run_l(speed,t):
    print('run_l')
    run_left.moveF(100,0.5)
    run_left.moveF(speed,t)
    run_left.stop(0)
    
   

t1 = threading.Thread(target = en_right, args=('right',))
t1.start()
t2 = threading.Thread(target = en_left, args=('left',))
t2.start()

t3 = threading.Thread(target = Run_r ,args=(50,10,))
t3.start()
t4 = threading.Thread(target = Run_l ,args=(50,10,))
t4.start()

t5 = threading.Thread(target = Camera ,args=(5,0.5,))
t5.start()



camera.stop_preview()
print('end')