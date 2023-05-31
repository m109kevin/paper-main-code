x = 1

'''
# 外部變數x可輸入def function
def test():
    print(x)
test()



def test2():
    x += 1 # 無法做計算，會出錯
    print(x)
test2()


'''
def test3(x):
    x += 1 # 用輸入之變數可做計算
    print(x)
test3(1)
print('global x = ',x) # 運算後的x不會改變外面的x


'''
def test4():
    global x # 定義全域變數，可做計算
    x += 1
    print(x)
test4()
print('global x = ',x)
'''