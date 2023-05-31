from EncoderModule import Encoder1
from MotorModule_2 import Motor2
import threading
import time

encoder_right = Encoder1(17,18)
encoder_left = Encoder1(22,23)
def en_right(right):
    encoder_right.Encoder_Read1(right)
def en_left(left):
    encoder_left.Encoder_Read1(left)


t1 = threading.Thread(target = en_right, args=('right',))
t1.start()
t2 = threading.Thread(target = en_left, args=('left',))
t2.start()

run = Motor2(6,16,19,12,20,26)
run.moveF(50,3)
run.stop(0)
print(encoder_right.counter)

print('Done')




