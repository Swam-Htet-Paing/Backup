#include"Servo.h"

Servo myServo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  myServo.attach(3);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String msg = Serial.readString();    
    short int angle = msg.toInt();
    
    if (angle > 180){
      myServo.write(180);
    }
    else if (angle < 0){
      myServo.write(0);
    }
    else{
      myServo.write(angle);
    }
  }  
}
