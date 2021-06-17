void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);    // sets the digital pin 13 as output
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(13, HIGH); // sets the digital pin 13 on
  delay(1000);            // waits for a second
  digitalWrite(13, LOW); // sets the digital pin 13 on
  delay(1000);            // waits for a second
  //Remember that analog pins are denoted by A0, A1, etc
  //Digital pins are denoted with simple integers upto 13
}
