import time
class test_class:
    def __init__(self,x):
        self.x = x

    def test_action(self):
        global action
        action = True
        while action:
            print(action)
            time.sleep(1)
        else:
            print(action)



# my_class = test_class(2,3)
# my_class.test_plus()
