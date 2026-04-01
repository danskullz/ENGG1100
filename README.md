# ENGG1100 Team Codebase

### Setup on RPI
#### Uploading micropython to rpi
Hold the BOOTSEL button and plug the pi into the computer.
Copy the ```.ufw2``` file to the **RPI-RP2** drive
The pi will reboot, and it is now running micropython.

### Setup on client computer
Install required python libraries:
```bash
$ pip3 install -r requirements.txt
```
The easiest way to interface with the pi is to install [Thonny](https://thonny.org/).
Opening the ```view``` tab and selecting ```files``` lets you view and upload files to the RPI

### Usage
Upload ```main.py``` and ```wetsock.py``` to the pi to use, then press run program.
On the client:
```bash
python3 client.py
```
This will then run the client script and attempt to connect to the RPI, where you can then control it