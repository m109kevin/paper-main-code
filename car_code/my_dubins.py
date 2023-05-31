import math
x = 70
y = 57.15
a = math.atan(x/y)
b = math.atan(x/y)
cosa = math.cos(a)
cosb = math.cos(b)
sina = math.sin(a)
sinb = math.sin(b)
D = math.sqrt(x**2 + y**2)
d = D/29.15


p = math.sqrt(d**2 - 2 + 2*math.cos(a - b) - 2*d*(sina + sinb))
t = a - math.atan((cosa + cosb)/(d - sina - sinb)) + math.atan(2/p)
q = b - math.atan((cosa + cosb)/(d - sina - sinb)) + math.atan(2/p)
print(t,p,q)

