#17 18 right
#22 23 left
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

class Encoder1:
    def __init__(self,A_pin,B_pin):
        self.A_pin = A_pin
        self.B_pin = B_pin
        GPIO.setup(self.A_pin,GPIO.IN)
        GPIO.setup(self.B_pin,GPIO.IN)
        
        self.outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
        self.last_AB = 0b00
        self.counter = 0
    
    
    def Encoder_Read1(self,left_right):
        while True:
            self.A = GPIO.input(self.A_pin)
            self.B = GPIO.input(self.B_pin)
            self.current_AB = (self.A<<1) | self.B
            self.position = (self.last_AB<<2) | self.current_AB
            self.counter += self.outcome[self.position]
            self.last_AB = self.current_AB
            self.left_right = left_right
            
            #print(self.left_right,'disctance:',self.counter)

class Encoder2:
    def __init__(self,A_pin,B_pin,C_pin,D_pin):
        self.A_pin = A_pin
        self.B_pin = B_pin
        self.C_pin = C_pin
        self.D_pin = D_pin
        GPIO.setup(self.A_pin,GPIO.IN)
        GPIO.setup(self.B_pin,GPIO.IN)
        GPIO.setup(self.C_pin,GPIO.IN)
        GPIO.setup(self.D_pin,GPIO.IN)        
        self.outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
        self.last_AB = 0b00
        self.last_CD = 0b00        
        self.counter1 = 0
        self.counter2 = 0    
    
    def Encoder_Read2(self):
        print('read')
        while True:
            self.A = GPIO.input(self.A_pin)
            self.B = GPIO.input(self.B_pin)

            self.current_AB = (self.A<<1) | self.B
            self.position1 = (self.last_AB<<2) | self.current_AB
            self.counter1 += self.outcome[self.position1]
            self.last_AB = self.current_AB


            self.C = GPIO.input(self.C_pin)
            self.D = GPIO.input(self.D_pin)
            self.current_CD = (self.C<<1) | self.D
            self.position2 = (self.last_CD<<2) | self.current_CD
            self.counter2 += self.outcome[self.position2]
            self.last_CD = self.current_CD
            
            print('disctance:',self.counter1,'_________',self.counter2)
'''
encoder = Encoder2(22,23,17,18)
encoder.Encoder_Read2()
'''