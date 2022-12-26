/*
 * PROGRAM TESTING
*/

String command;
int ledPin = 13;

void setup() {
  Serial.begin(9600);
  pinMode(ledPin, OUTPUT);
  delay(2000);
  Serial.println("Type Command on/off here!!!");
}

void loop() {
  if(Serial.available()){
    command = Serial.readStringUntil("\n");//Membaca data serial comm
    command.trim(); //White space serial monitor
    Serial.print("Command: ");
    Serial.print(command); //Data dari Raspi serial comm
    //Masukin program printer disini dan jangan lupa kasih tanda \n=============
  }
}
