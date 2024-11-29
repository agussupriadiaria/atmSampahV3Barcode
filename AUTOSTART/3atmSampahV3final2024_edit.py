'''
============== ATM SAMPAH 2024 ==============
Testing 2 Juli 2024

Target:
- Send data to spreadsheet
- Koreksi dari chatgpt, 2 November 2024
'''
from tkinter import *
import serial.tools.list_ports
import threading
import time
import sys
import signal
import RPi.GPIO as gp
import random
from escpos.printer import Serial
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Konfigurasi GPIO
gp.setwarnings(False)
gp.setmode(gp.BCM)
gp.setup(5, gp.OUT)
gp.output(5, gp.HIGH)
gp.setup(6, gp.IN, pull_up_down=gp.PUD_UP)
gp.setup(13, gp.OUT)
gp.output(13, gp.HIGH)
gp.setup(19, gp.OUT)
gp.output(19, gp.HIGH)
gp.setup(26, gp.IN, pull_up_down=gp.PUD_UP)

def setGsheet():
    global sheet
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/home/blacksheep/Desktop/AUTOSTART/atmsampah2024.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("ATMSAMPAH2024").sheet1

def signal_handler(signum, frame):
    sys.exit()
signal.signal(signal.SIGINT, signal_handler)

def mainPage():
    global root, timeStamp, dateStamp, barcodeLabel, jumlahLabel, ukuranLabel, nominalLabel, bottle, saldo, parameterLabel3, userIDLabel
    root = Tk()
    root.attributes('-fullscreen', True)
    root.title("Atm Sampah - PilahSampah")
    root.config(bg="white")

    titleLabel = Label(root, text="PilahSampah", font=("Helvatica", 18, "bold"), bg="white")
    titleLabel.place(relx=0.5, rely=0.1, anchor=CENTER)

    mainFrame = Frame(root, bg="white", bd=10, highlightbackground="green", highlightthickness=5)
    mainFrame.place(relx=0.025, rely=0.15, relwidth=0.95, relheight=0.80)

    stampFrame = Frame(mainFrame, bg="white", width=400, height=100)
    stampFrame.place(x=10, y=10)

    timeLabel = Label(stampFrame, text="Waktu   ", font=("Helvatica", 10, "bold"), bg="white")
    timeLabel.place(x=10, y=1)
    dateLabel = Label(stampFrame, text="Tanggal ", font=("Helvatica", 10, "bold"), bg="white")
    dateLabel.place(x=10, y=30)

    timeStamp = Label(stampFrame, text="00:00:00", font=("Helvatica", 10, "bold"), bg="white")
    timeStamp.place(x=100, y=1)
    dateStamp = Label(stampFrame, text="dd/mm/yy", font=("Helvatica", 10, "bold"), bg="white")
    dateStamp.place(x=100, y=30)

    ariaLabel = Label(mainFrame, text="[PilahSampah - Malang]", font=("Courier", 10, "bold"), bg="white")
    ariaLabel.place(x=560, y=10)

    parameterFrame = Frame(mainFrame, bg="white", width=350, height=200, highlightbackground="blue", highlightthickness=5)
    parameterFrame.place(x=10, y=75)

    parameterLabel1 = Label(parameterFrame, bg="white", text="TOTAL SALDO", font=("Helvatica", 15, "bold"))
    parameterLabel1.place(x=85, y=10)
    parameterLabel2 = Label(parameterFrame, text="Rp", font=("Helvatica", 30, "bold"), bg="white")
    parameterLabel2.place(x=65, y=80)
    parameterLabel3 = Label(parameterFrame, text="9999", font=("Helvatica", 30, "bold"), bg="white")
    parameterLabel3.place(x=140, y=80)

    transaksiFrame = Frame(mainFrame, bg="white", width=350, height=200, highlightbackground="red", highlightthickness=5)
    transaksiFrame.place(x=370, y=75)

    nameDataLabel = Label(transaksiFrame, bg="white", text="DATA", font=("Helvatica", 15, "bold"))
    nameDataLabel.place(x=135, y=10)
    nameUserIdLabel = Label(transaksiFrame, bg="white", text="User ID   ", font=("Helvatica", 10, "bold"))
    nameUserIdLabel.place(x=50, y=50)
    nameJumlahLabel = Label(transaksiFrame, bg="white", text="Jumlah    ", font=("Helvatica", 10, "bold"))
    nameJumlahLabel.place(x=50, y=75)
    nameUkuranLabel = Label(transaksiFrame, bg="white", text="Ukuran   ", font=("Helvatica", 10, "bold"))
    nameUkuranLabel.place(x=50, y=100)
    nameNominalLabel = Label(transaksiFrame, bg="white", text="Nominal            Rp", font=("Helvatica", 10, "bold"))
    nameNominalLabel.place(x=50, y=125)
    nameBarcodeLabel = Label(transaksiFrame, bg="white", text="Barcode  ", font=("Helvatica", 10, "bold"))
    nameBarcodeLabel.place(x=50, y=150)

    userIDLabel = Label(transaksiFrame, bg="white", text="99999", font=("Helvatica", 10, "bold"))
    userIDLabel.place(x=170, y=50)
    jumlahLabel = Label(transaksiFrame, bg="white", text="999", font=("Helvatica", 10, "bold"))
    jumlahLabel.place(x=170, y=75)
    ukuranLabel = Label(transaksiFrame, bg="white", text="Medium", font=("Helvatica", 10, "bold"))
    ukuranLabel.place(x=170, y=100)
    nominalLabel = Label(transaksiFrame, bg="white", text="999", font=("Helvatica", 10, "bold"))
    nominalLabel.place(x=210, y=125)
    barcodeLabel = Label(transaksiFrame, bg="white", text="9999999999999", font=("Helvatica", 10, "bold"))
    barcodeLabel.place(x=170, y=150)

    printButton = Button(mainFrame, text="Cetak Struk", font=("Helvatica", 10, "bold"), bg="green", fg="blue", width=10, height=3, command=resetCounter)
    printButton.place(x=55, y=290)

    printButton = Button(mainFrame, text="Scan Ulang", font=("Helvatica", 10, "bold"), bg="yellow", fg="blue", width=10, height=3, command=barcodeScanner)
    printButton.place(x=195, y=290)

    messageLabel = Label(mainFrame, text="Terima Kasih Sudah Ikut", font=("Helvatica", 10, "bold"), bg="white")
    messageLabel.place(x=457, y=300)
    messageLabel = Label(mainFrame, text="Menyelamatkan Lingkungan", font=("Helvatica", 10, "bold"), bg="white")
    messageLabel.place(x=445, y=325)

    bottle = 0
    saldo = 0

    connexion()
    updateTime()
    updateDate()
    userIDNum()

def userIDNum():
    global userID
    userID = random.randrange(10000, 100000)
    userIDLabel["text"] = userID

def bottleCounter():
    global bottle
    bottle += 1
    parameterLabel3["text"] = saldo
    jumlahLabel["text"] = bottle

def resetCounter():
    global bottle, saldo
    thermalPrinterX()
    bottle = 0
    saldo = 0
    parameterLabel3["text"] = saldo
    nominalLabel["text"] = saldo
    jumlahLabel["text"] = bottle
    ukuranLabel["text"] = "-"
    barcodeLabel["text"] = "0"
    userIDNum()
    print("Reset Jumlah Botol: ", bottle)
    print("Reset Jumlah Saldo: Rp", saldo)
    print("")

def thermalPrinterX():
    p = Serial(devfile='/dev/serial0', baudrate=9600, bytesize=8, parity='N', stopbits=1, timeout=1.00, dsrdtr=True)
    p.set(font="a", height=1, align="center", bold=True, double_height=False)
    p.text("ATM SAMPAH\n")
    p.text("Pilah Sampah\n\n")
    p.text("Jumlah Botol: ")
    p.text(str(bottle) + " Pcs\n")
    p.text("Total Saldo: Rp ")
    p.text(str(saldo) + "\n\n")
    p.text(str(userID) + "\n")
    p.text(time.asctime() + "\n")
    p.text("Terima kasih\n\n\n")

def saveData():
    sheet.append_row([str(userID), str(bottle), str(saldo), time.asctime()])

def barcodeScanner():
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = ports[0].device
    serialInst.open()
    if serialInst.is_open:
        serialInst.flush()
        data = serialInst.readline().decode('utf-8').strip()
        barcodeLabel["text"] = data
        processBarcode(data)
    serialInst.close()

def processBarcode(data):
    global saldo
    if data == "8999999012300":
        saldo = bottle * 50
        nominalLabel["text"] = saldo
        ukuranLabel["text"] = "Small"
        saveData()
    elif data == "8999999012317":
        saldo = bottle * 100
        nominalLabel["text"] = saldo
        ukuranLabel["text"] = "Medium"
        saveData()
    elif data == "8999999012324":
        saldo = bottle * 150
        nominalLabel["text"] = saldo
        ukuranLabel["text"] = "Large"
        saveData()

def connexion():
    thread = threading.Thread(target=waitingGPIO)
    thread.setDaemon(True)
    thread.start()

def waitingGPIO():
    while True:
        buttonState = gp.input(6)
        if buttonState == gp.LOW:
            bottleCounter()
            print("Jumlah Botol: ", bottle)
            print("Jumlah Saldo: Rp", saldo)
            print("")

def updateTime():
    currentTime = time.strftime("%H:%M:%S")
    timeStamp["text"] = currentTime
    root.after(1000, updateTime)

def updateDate():
    currentDate = time.strftime("%d/%m/%Y")
    dateStamp["text"] = currentDate
    root.after(1000, updateDate)

if __name__ == '__main__':
    setGsheet()
    mainPage()
    root.mainloop()
