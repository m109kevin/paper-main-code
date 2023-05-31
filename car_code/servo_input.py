import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(27,GPIO.OUT)
servo1 = GPIO.PWM(27,50)

servo1.start(0)
print('begin')


try:
    while True:
        angle = float(input('enter angle between -36 t0 72:'))
        if angle <= 72 and angle >= -36:
            servo1.ChangeDutyCycle(7+(angle/18))
            time.sleep(0.5)
            servo1.ChangeDutyCycle(0)
        else:
            break
        
finally:
    servo1.stop()
    GPIO.cleanup()
    print('end')
    