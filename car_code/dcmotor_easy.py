import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

EnA=6
In1=16
In2=19
EnB=12
In3=20
In4=26

GPIO.setup(EnA,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(In1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(In2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(EnB,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(In3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(In4,GPIO.OUT,initial=GPIO.LOW)

def motor_forward():
    print('motor forward')
    GPIO.output(EnA,True)
    GPIO.output(In1,True)
    GPIO.output(In2,False)
    GPIO.output(EnB,True)
    GPIO.output(In3,True)
    GPIO.output(In4,False)
    
def motor_stop():
    print('motor stop')
    GPIO.output(In1,False)
    GPIO.output(In2,False)
    GPIO.output(In3,False)
    GPIO.output(In4,False)

motor_forward()
time.sleep(3)
motor_stop()
time.sleep(3)

print('end')




