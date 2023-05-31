# A:6(EnA),16,19 (left)
# B:12(EnB),20,26 (right)
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor1:
    def __init__(self,En,In1,In2):
        self.En = En
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(En,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In1,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In2,GPIO.OUT,initial = GPIO.LOW)
        self.pwmA = GPIO.PWM(self.En,100)
        self.pwmA.start(0)        

    def moveF(self,speed,t):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1,GPIO.HIGH)
        GPIO.output(self.In2,GPIO.LOW)
        time.sleep(t)
    def bakeF(self,speed,t):
        self.pwmA.ChangeDutyCycle(speed)
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.HIGH)
        time.sleep(t)
    
    def stop(self,t):
        self.pwmA.ChangeDutyCycle(0)
        time.sleep(t)
        
class Motor1_Encoder:
    def __init__(self,En,In1,In2,A_pin,B_pin):
        self.En = En
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(En,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In1,GPIO.OUT,initial = GPIO.LOW)
        GPIO.setup(In2,GPIO.OUT,initial = GPIO.LOW)
        self.pwmA_En = GPIO.PWM(self.En,100)
        self.pwmA_En.start(0)
        
        #for encoder    
        self.A_pin = A_pin
        self.B_pin = B_pin
        GPIO.setup(self.A_pin,GPIO.IN)
        GPIO.setup(self.B_pin,GPIO.IN)
        
        self.outcome = [0,-1,1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
        self.last_AB = 0b00
        self.counter = 0       
                          
    def encoder_stop(self,left_right,speed,value):
        while True:
            self.A = GPIO.input(self.A_pin)
            self.B = GPIO.input(self.B_pin)
            self.current_AB = (self.A<<1) | self.B
            self.position = (self.last_AB<<2) | self.current_AB
            self.counter += self.outcome[self.position]
            self.last_AB = self.current_AB
            self.left_right = left_right
            print(self.left_right,'disctance:',self.counter)
            if self.counter <= value:
                self.pwmA_En.ChangeDutyCycle(speed)
                GPIO.output(self.In1,GPIO.HIGH)
                GPIO.output(self.In2,GPIO.LOW)
                #time.sleep(1)
                print('read')
            else:
                self.pwmA_En.ChangeDutyCycle(0)
                break
                
            
def main():
    motor1.moveF(60,2)
    motor1.stop(2)
    motor1.moveF(60,2)
    motor1.stop(2)
'''    
if __name__=='__main__':
    motor1 = Motor1(6,16,19)
    main()
'''


print('end')
    


    
    
    
    
    
    
    
    
        
        
        
        
        
        
        
        


        
        
    