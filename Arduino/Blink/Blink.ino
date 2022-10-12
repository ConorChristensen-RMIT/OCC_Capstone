/*
  Blink

  Turns an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino
  model, check the Technical Specs of your board at:
  https://www.arduino.cc/en/Main/Products

  modified 8 May 2014
  by Scott Fitzgerald
  modified 2 Sep 2016
  by Arturo Guadalupi
  modified 8 Sep 2016
  by Colby Newman

  This example code is in the public domain.

  https://www.arduino.cc/en/Tutorial/BuiltInExamples/Blink
*/

int preamble[9] = {1, 1, 1, 1, 1, 1, 1, 0, 0};
int packet[8] = {0, 0, 1, 0, 0, 1, 0, 0};
int parity[2] = {0, 0};
int loop_counter = -1;



// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(2, OUTPUT);
//  int camera_h = 720;
//  int camera_hz = 30;
//  double period_ms = 1000/(camera_hz*camera_h);
//  delay_ms = period_ms/2;
}

// the loop function runs over and over again forever
void loop() {
  loop_counter++;
  if (loop_counter < 9) {
    if (preamble[loop_counter] == 0) {digitalWrite(2, LOW);}
    else {digitalWrite(2, HIGH);}
  }
  else if (loop_counter < 17) {
    if (packet[loop_counter-9] == 0) {digitalWrite(2, LOW);}
    else {digitalWrite(2, HIGH);}
  }
  else if (loop_counter < 19) {
    if (parity[loop_counter-17] == 0) {digitalWrite(2, LOW);}
    else {digitalWrite(2, HIGH);}
  }
  else {loop_counter = -1;}
  
  delayMicroseconds(350);
//  // TO KEEP 1 THEN 0 FOR 2 SEPERATE PERIODS
//  digitalWrite(2, HIGH);   // turn the LED on (HIGH is the voltage level)
//  delayMicroseconds(300);                       // Should be 1929, but for some reason 1926 appears best
//  digitalWrite(2, LOW);    // turn the LED off by making the voltage LOW
//  delayMicroseconds(300);                       // Should be 1929, but for some reason 1926 appears best
}
