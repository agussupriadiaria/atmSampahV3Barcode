/*
 * PROGRAM ARDUINO THERMAL PRINTER AUTO CUTTER
 * 
*/

#include "USBPrinter.h"
#include "ESC_POS_Printer.h"

class PrinterOper : public USBPrinterAsyncOper
{
  public:
    uint8_t OnInit(USBPrinter *pPrinter);
};

uint8_t PrinterOper::OnInit(USBPrinter *pPrinter)
{
  Serial.println(F("USB Printer OnInit"));
  Serial.println(F("Bidirectional="));
  Serial.println(pPrinter->isBidirectional());
  return 0;
}
//Logic untuk usb shield arduino==============
USB myusb;
PrinterOper AsyncOper;
USBPrinter uprinter(&myusb, &AsyncOper); //RX dan RX =================
ESC_POS_Printer printer (&uprinter);

void setup(){
  Serial.begin(115200);
  while (!Serial && millis() < 3000) delay(1);

  if(myusb.Init()){
    Serial.println(F("USB host failed to initialize"));
    while(1) delay(1);
  }
  Serial.println(F("USB host init OK"));
}

void loop(){
  myusb.Task();
//Make sure usb printer found and ready==============
  if(uprinter.isReady()){
    printer.begin();
    Serial.println(F("Init ESC POS Printer"));

//DATA YANG DIPRINT DIMASUKIN SINI================
    //printer.setSize('M'); // L for Large
    printer.println(F("Hello Printer"));
    printer.feed(5);
    autocutter();
//================
    
    //Do this one time to avoid wasting paper
    while(1) delay(1); //looping trap biar nggak terulang dan keluar terus sampai alat dimatikan
  }
}

void autocutter(){
  uprinter.write(29);
  uprinter.write(86);
  uprinter.write(48);
}
