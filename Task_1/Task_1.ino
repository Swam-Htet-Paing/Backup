#include "Servo.h"

int ADC_val = 0;
Servo s1;
void setup() {
  // put your setup code here, to run once:
  s1.attach(3);
  pinMode(A0,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  ADC_val = analogRead(A0);
  if (ADC_val > 782)
    s1.write(90);
  else
    s1.write(0);
}
