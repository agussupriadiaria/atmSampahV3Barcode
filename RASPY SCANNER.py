'''
PROGRAM UNTUK BARCODE SCANNER DIRECT TO RASPI

Source:
https://circuitdigest.com/microcontroller-projects/interfacing-usb-barcode-scanner-with-raspberry-pi-4
'''

from time import sleep
from rpi_lcd import LCD
lcd = LCD() #inintialising the LCD by default it is for 16X2 alpha numeric Lcd
item_count=0   #For storing the no. of scanned items
scode="" #variable that will contain the scan code
lcd.text("Scan the Code... ", 1)   #welcome message that will display in first line of the display
while 1:   #for Endless scans
    scode= str(input())  #will wait to get the input from barcode reader
    lcd.text("Scanned Barcode is", 1)
    lcd.text(scode,2)  #displaying Scanned Barcode on 2nd Row
    sleep(2)   #Delay of 2 seconds
    lcd.text("   Item Added", 1)
    sleep(2)
    item_count=item_count+1   #count and will increase the count every time it scan a barcode
    IC=str(item_count)   #type casting item_count from Integer to STRING
    lcd.text("  Total Item = ",1)
    lcd.text(IC,2) 
    sleep(1)