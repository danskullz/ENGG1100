import network
import socket
import time
import struct
import hashlib
import binascii
from machine import Pin

# motor 1
IN1 = Pin(4, Pin.OUT)
IN2 = Pin(5, Pin.OUT)

# motor 2 yo
IN3 = Pin(6, Pin.OUT)
IN4 = Pin(7, Pin.OUT)

# start stop functions
def stop():
    IN1.off(); IN2.off()
    IN3.off(); IN4.off()
 
def forward():
    IN1.on();  IN2.off()
    IN3.on();  IN4.off()
 
def backward():
    IN1.off(); IN2.on()
    IN3.off(); IN4.on()
 
stop()