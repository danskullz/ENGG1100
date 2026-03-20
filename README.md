# ENGG1100 Team Codebase

### Setup on RPI
Initialise systemd module on raspberry pi at boot, and enable the service.
```bash
$ sudo systemctl enable pigpiod
```
```bash
$ sudo systemctl start pigpiod
```
### Setup on Host Computer
Install required python libraries:
```bash
$ pip3 install -r requirements.txt
```

### Usage
Set the local ip of the Raspberry Pi in the environment variable ```PIGPIO_ADDR``` prefacing the python command. For example:

```bash
$ PIGPIO_ADDR=192.168.0.1 python3 remote.py
```

### Hardware
Pin definitions:
GND:  GND:     Pin 34
In 1: GPIO 17: Pin 11
In 2: GPIO 22: Pin 15
In 3: GPIO 23: Pin 16
In 4: GPIO 24: Pin 18