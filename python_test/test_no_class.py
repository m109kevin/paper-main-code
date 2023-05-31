import time
import threading
# 結論:
# def function 運算時可以使用外部變數， 但已def(裡面變數)優先，並且外部變數無法計算，只能用來做判斷
# 如果要用def function計算外部變數並且輸出到外面，使用global

action = True
def test_action():
    # global action #有打>global action = False 會改變外部的action 沒打的話2個action記憶體是分開的 有打會變成1個action記憶體
    # action = True
    # action = False # 外面變數會輸入，但以裡面的優先
    while action:
        print(action)
        time.sleep(1)
    else:
        print(action)

t = threading.Thread(target = test_action)
t.start()

time.sleep(5)
action = False
print('global action = ',action)