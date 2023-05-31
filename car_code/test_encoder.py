# A:6(EnA),16,19 (left) encoder:22 23 (left)
# B:12(EnB),20,26 (right) encoder:17 18 (right)
from MotorModule_2 import Motor2
from EncoderModule import Encoder2
from EncoderModule import Encoder1
from MotorModule_1 import Motor1
from MotorModule_1 import Motor1_Encoder

import threading
import time


'''
test = Motor2(6,16,19,12,20,26)
test.moveF(30,3)
test.stop(2)

'''
def Encoder_Read():
    encoder_set = Encoder2(22,23,17,18)
    encoder_set.Encoder_Read2()
def Test():
    time.sleep(1)
    print()
    test = Motor2(6,16,19,12,20,26)
    test.moveF(30,8)
    test.stop(2)
def Encoder_Read1():
    time.sleep(1)
    test_1by1 = Encoder1(17,18)
    test_1by1.Encoder_Read1('right')
t1 = threading.Thread(target = Encoder_Read1 ,args=())
t1.start()
'''
t2 = threading.Thread(target = Test ,args=())
t2.start()
'''





'''
test_l_encoder = Motor1_Encoder(6,16,19,22,23)
test_l_encoder.encoder_stop(100,300)




test_r.moveF(50,6)
test_r.stop(0)
'''
print('end')

