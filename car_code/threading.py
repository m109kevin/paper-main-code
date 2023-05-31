import threading
import time
def threadfunc(n):
    for a in range(n):
        print(a)
        time.sleep(1)

t1 = threading.Thread(target = threadfunc, args=(5,))
t1.start()

for a in range(5):
    print('mainthread:',a)
    time.sleep(0.5)
t1.join()
print('Done')