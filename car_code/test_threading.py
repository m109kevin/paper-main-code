import time
import threading

def detect():
    while action:
        if not go:
            print('yolo detect')
            time.sleep(5)
def line_sensor():
    while action:
        if go:
            print('senser go = ',go)
            time.sleep(1)
def encoder():
    global encoder
    encoder = 0
    while action:
        print('encoder = ',encoder)
        encoder += 1
        time.sleep(1)
        
def motor():
    while action:
        if go:
            print('motor go = ',go)
            time.sleep(1)

def main_program():
    i = 1
    global go
    while action:
        d = i*10
        # print('d',d)
        if encoder >= d:
            go = False
            # print('go',go)
            time.sleep(1)
            print('yolo detect')
            time.sleep(5)
            go = True
            # print('go',go)
            i += 1
        
        
    

go = True
action = True
   
t1 = threading.Thread(target = line_sensor)
t2 = threading.Thread(target = encoder)
t3 = threading.Thread(target = motor)
t4 = threading.Thread(target = main_program)

t2.start()
t1.start()
t3.start()
t4.start()

time.sleep(30)
action = False
'''
a = False
while not a:
    print(a)
    time.sleep(5)
'''















