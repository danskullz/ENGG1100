from gpiozero import Motor
from time import sleep

motor_1 = Motor(forward=DEFINETHIS, backward=DEFINETHIS)
motor_2 = Motor(forward=DEFINETHIS, backward=DEFINETHIS)

def forward(sec):
    motor_1.forward()
    motor_2.forward()
    sleep(sec)
    stop()

def backward(sec):
    motor_1.backward()
    motor_2.backward()
    sleep(sec)
    stop()

def stop():
    motor_1.stop()
    motor_2.stop()