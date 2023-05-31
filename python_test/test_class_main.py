import time
import threading
from test_class import test_class

action = True
my_class = test_class(2)


t = threading.Thread(target = my_class.test_action) # 用 class無法把輸入全域變數
# t = threading.Thread(target = my_class.test_action()) 為什麼+括號布一樣
t.start()

# time.sleep(5)
time.sleep(5)
action = False
print('global action = ',action)

#　print(x)

