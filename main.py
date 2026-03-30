import network
import socket
import time
from machine import Pin
from 1websocket import websocket_handshake, WebSocketError


# motor 1
IN1 = Pin(4, Pin.OUT)
IN2 = Pin(5, Pin.OUT)

# motor 2 yo
IN3 = Pin(6, Pin.OUT)
IN4 = Pin(7, Pin.OUT)

# wifi
SSID     = "Daniel's iPhone"
PASSWORD = ""
PORT     = 788

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


# connecting to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

for i in range(30):
    if wlan.isconnected():
        break
    print(".", end="")
    time.sleep(0.5)

if not wlan.isconnected():
    print("\ncould not connect to the 'fi")
    raise RuntimeError("could not connect to the 'fi")

ip = wlan.ifconfig()[0]
print(f"\nconnected to the 'fi \nip: {ip}  \nport: {PORT}")