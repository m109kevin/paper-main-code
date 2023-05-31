from picamera import PiCamera
import time
"""set camera"""
camera = PiCamera()
camera.resolution = (1920,1080)
camera.framerate = 60
# 開啟預覽
camera.start_preview()
for i in range(5):
    camera.capture('/home/pi/Desktop/car_code/picture/' + str(i) +'.jpg')
    time.sleep(0.5)
    print(i)
camera.stop_preview()
print('end')