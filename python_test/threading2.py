import  threading
import time

def func1():
    for i in range(100):
        print(i)
        time.sleep(1)

def func2():
    for n in range(100):
        print(n)
        time.sleep(1)
t1 = threading.Thread(target = func1)
t2 = threading.Thread(target = func2)

t1.start()
time.sleep(5)
t2.start()