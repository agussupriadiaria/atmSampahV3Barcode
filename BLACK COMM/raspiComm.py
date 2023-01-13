'''
TESTING SERIAL KOMUNIKASI RASPI ARDUINO

connection usb /dev/ttyUSB0
'''

import serial
import time

def mainCode():
	ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
	#ser.flush()
	
	while True:
		ser.write(b"on\n")
		time.sleep(4)
		ser.write(b"off\n")
		time.sleep(4)
		
		#Data yang dikirim diinput disini
		#ser.write(b"hahaha\n")

mainCode()