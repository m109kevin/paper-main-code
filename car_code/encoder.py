#17 18 right
#22 23 left
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


A_pin = 17
B_pin = 18
A_pin2 = 22
B_pin2 = 23


GPIO.setup(A_pin,GPIO.IN)
GPIO.setup(B_pin,GPIO.IN)
GPIO.setup(A_pin2,GPIO.IN)
GPIO.setup(B_pin2,GPIO.IN)

outcome = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB = 0b00
counter = 0

outcome2 = [0,1,-1,0,-1,0,0,1,1,0,0,-1,0,-1,1,0]
last_AB2 = 0b00
counter2 = 0

while True:
    A = GPIO.input(A_pin)
    B = GPIO.input(B_pin)
    current_AB = (A<<1) | B
    position = (last_AB<<2) | current_AB
    counter += outcome[position]
    last_AB = current_AB
    print('disctance1:',counter)
    
    A2 = GPIO.input(A_pin2)
    B2 = GPIO.input(B_pin2)
    current_AB2 = (A2<<1) | B2
    position2 = (last_AB2<<2) | current_AB2
    counter2 += outcome2[position2]
    last_AB2 = current_AB2
    print('distance2:',counter2)
    if counter == 0:
        continue
    else:
        while counter % 1000 == 0:
            print(counter)
            break
        
    
    
    
    
    
    
    