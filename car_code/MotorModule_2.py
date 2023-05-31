# A:6(EnA),16,19 (left)
# B:12(EnB),20,26 (right)
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor2:
    def __init__(self,EnA,In1A,In2A,EnB,In1B,In2B):
        self.EnA = EnA
        self.In1A = In1A
        self.In2A = In2A
        self.EnB = EnB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(EnA,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In1A,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In2A,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(EnB,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In1B,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In2B,GPIO.OUT,initial = GPIO.LOW)
        self.pwmA = GPIO.PWM(self.EnA,100)
        self.pwmB = GPIO.PWM(self.EnB,100)
        self.pwmA.start(0)
        self.pwmB.start(0)

    def moveF_no_stop(self,speed):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1A,GPIO.HIGH)
        GPIO.output(self.In2A,GPIO.LOW)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.In1B,GPIO.HIGH)
        GPIO.output(self.In2B,GPIO.LOW)
        
    def moveF(self,speed,t):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1A,GPIO.HIGH)
        GPIO.output(self.In2A,GPIO.LOW)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.In1B,GPIO.HIGH)
        GPIO.output(self.In2B,GPIO.LOW)
        time.sleep(t)
        
    def moveB_no_stop(self,speed):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1A,GPIO.LOW)
        GPIO.output(self.In2A,GPIO.HIGH)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.In1B,GPIO.LOW)
        GPIO.output(self.In2B,GPIO.HIGH)
        
        
    def moveB(self,speed,t):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1A,GPIO.LOW)
        GPIO.output(self.In2A,GPIO.HIGH)
        self.pwmB.ChangeDutyCycle(speed)
        GPIO.output(self.In1B,GPIO.LOW)
        GPIO.output(self.In2B,GPIO.HIGH)
        time.sleep(t)
    
    def stop(self,t):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        time.sleep(t)


def main():
    motor2.moveF(60,2)
    motor2.stop(2)
    motor2.moveF(60,2)
    motor2.stop(2)
    

    
    
    


