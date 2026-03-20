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
| GND  | GND | Pin 34 |
|------|-----|--------|
| In 1 | 17  | 11     |
| In 2 | 22  | 15     |
| In 3 | 23  | 16     |
| In 4 | 24  | 18     |