'''
TESTING SERIAL KOMUNIKASI RASPI ARDUINO

connection usb /dev/ttyUSB0
'''

import serial
import time

def mainCode():
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	ser.flush()
	
	while True:
		ser.write(b"on\n")
		time.sleep(0.2)
		ser.write(b"off\n")
		time.sleep(0.2)

mainCode()