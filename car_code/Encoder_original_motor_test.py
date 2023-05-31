#17 18 right
#22 23 left
import RPi.GPIO as GPIO
from MotorModule_1 import Motor1
GPIO.setmode(GPIO.BCM)

A_pin = 22
B_pin = 23
C_pin = 17
D_pin = 18
GPIO.setup(A_pin,GPIO.IN)
GPIO.setup(B_pin,GPIO.IN)
GPIO.setup(C_pin,GPIO.IN)
GPIO.setup(D_pin,GPIO.IN)

outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB = 0b00
last_CD = 0b00
counter1 = 0
counter2 = 0

motor_l = Motor1(6,16,19)
motor_r = Motor1(12,20,26)

while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    
    C = GPIO.input(C_pin)
    D = GPIO.input(D_pin)
    
    current_AB = (A<<1) | B
    position = (last_AB<<2) | current_AB
    counter1 += outcome[position]
    last_AB = current_AB
    
    current_CD = (C<<1) | D
    position2 = (last_CD<<2) | current_CD
    counter2 += outcome[position2]
    last_CD = current_CD
    print(counter1,'_____',counter2)
  
    if counter1 < 150:
        motor_l.moveF(50,0)
        motor_r.moveF(50,0)
        print('read1')
    else:
        break
'''
while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    
    C = GPIO.input(C_pin)
    D = GPIO.input(D_pin)
    
    current_AB = (A<<1) | B
    position = (last_AB<<2) | current_AB
    counter1 += outcome[position]
    last_AB = current_AB
    
    current_CD = (C<<1) | D
    position2 = (last_CD<<2) | current_CD
    counter2 += outcome[position2]
    last_CD = current_CD
    print(counter1,'_____',counter2)
    
    if counter1 > 0:
        motor_l.backF(50,0)
        motor_r.backF(50,0)
        print('read2')
    else:
        break
    
    
    
    
    

    
motor_l.stop(0)
motor_r.stop(0)
print('end')
 '''     
'''            
class Encoder:
    def __init__(self,A_pin,B_pin):
        self.A_pin = A_pin
        self.B_pin = B_pin
        GPIO.setup(self.A_pin,GPIO.IN)
        GPIO.setup(self.B_pin,GPIO.IN)
        
        self.outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
        self.last_AB = 0b00
        self.counter = 0
    
    
    def Run(self,left_right):
        while True:
            self.A = GPIO.input(self.A_pin)
            self.B = GPIO.input(self.B_pin)
            self.current_AB = (self.A<<1) | self.B
            self.position = (self.last_AB<<2) | self.current_AB
            self.counter += self.outcome[self.position]
            self.last_AB = self.current_AB
            self.left_right = left_right
            print(self.left_right,'disctance:',self.counter)

'''
        


