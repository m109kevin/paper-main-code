import threading
import time

action = True
def motor():
    while action:
        if go:
            print('motor go = ',go)
            time.sleep(1)
def count_time():
    global go
    for i in range(5):
        go = True
        print('count_time go = ',go)
        time.sleep(3)
        go = False
        print('count_time go = ',go)
        time.sleep(3)

t1 = threading.Thread(target = count_time)
t1.start()
t2 = threading.Thread(target = motor)
t2.start()

#　count_time()print(action)