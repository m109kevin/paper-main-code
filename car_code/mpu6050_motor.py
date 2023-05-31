from MPU6050Module import mpu6050
from MotorModule_2 import Motor2
import threading
import time
mpu = mpu6050(0x68)

def MPU():
    while True:
        print("Temp : "+str(mpu.get_temp()))
        print()

        accel_data = mpu.get_accel_data()
        print("Acc X : "+str(accel_data['x']))
        print("Acc Y : "+str(accel_data['y']))
        print("Acc Z : "+str(accel_data['z']))
        print()

        gyro_data = mpu.get_gyro_data()
        print("Gyro X : "+str(gyro_data['x']))
        print("Gyro Y : "+str(gyro_data['y']))
        print("Gyro Z : "+str(gyro_data['z']))
        print()
        print("-------------------------------")
        time.sleep(1)

def Motor_run():
    time.sleep(3)
    motor = Motor2(6,16,19,12,20,26)
    motor.moveF(30,10)
    motor.stop(2)   

t1 = threading.Thread(target = MPU ,args=())
t1.start()

t2 = threading.Thread(target = Motor_run ,args=())
t2.start()





