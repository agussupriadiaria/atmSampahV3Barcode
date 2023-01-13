/*
 * PROGRAM TESTING
 * 
 * Desc:
 * Program serial comm untuk arduino thermal printer.
 * Work just fine 27 Desember 2022
*/

//SERIAL COMM==========
String command;
//TPRINTER LIBRARY==========
#include "USBPrinter.h"
#include "ESC_POS_Printer.h"

//TPRINTER VARIABEL============
class PrinterOper : public USBPrinterAsyncOper{
  public:
    uint8_t OnInit(USBPrinter *pPrinter);
};

uint8_t PrinterOper::OnInit(USBPrinter *pPrinter){
  Serial.println(pPrinter->isBidirectional());
  return 0;
}
//Logic untuk usb shield arduino==============
USB myusb;
PrinterOper AsyncOper;
USBPrinter uprinter(&myusb, &AsyncOper); //RX dan RX =================
ESC_POS_Printer printer (&uprinter);

void setup() {
  Serial.begin(9600);
  Serial.println("Type Command here!!!");
//TPRINTER==================
  while (!Serial && millis() < 3000) delay(1);

  if(myusb.Init()){
    Serial.println(F("USB host failed to initialize"));
    while(1) delay(1);
  }
  Serial.println(F("USB host init OK"));
}

void loop() {
//TPRINTER===========
  myusb.Task();
  if(Serial.available()){
    command = Serial.readStringUntil("\n");//Membaca data serial comm
    command.trim(); //White space serial monitor
    if(uprinter.isReady()){
      printer.begin();
      //Sett format huruf yang diprint===========
      if(command == "ARIA"){
        printer.justify('C');
        printer.setSize('L');
        printer.boldOn();
        printer.println(command);
      }
      else if(command == " "){
        printer.justify('C');
        printer.println("");
      }
      else{
        printer.justify('C');
        printer.println(' ');
        printer.println(command);
      }
      
      //printer.feed(5);
      //autocutter();
    }
    Serial.print("Command: ");
    Serial.print(command); //Data dari Raspi serial comm
    //Masukin program printer disini dan jangan lupa kasih tanda \n=============
  }
}

void autocutter(){
  uprinter.write(29);
  uprinter.write(86);
  uprinter.write(48);
}
