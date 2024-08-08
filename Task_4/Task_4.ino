#include <Stepper.h>
#define one_rev_steps 64

Stepper uni1(one_rev_steps,8,9,10,11);
int b1 = 12, pot = A0;
byte go = 1;
bool clockwise = true;
void setup() {
  // put your setup code here, to run once:
  pinMode(b1, INPUT);
  pinMode(pot, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int val = map(analogRead(pot), 0,1023, 0,50);
  if (digitalRead(b1) == HIGH)
    go == 1 ? go++: go--;
    
  go == 1 ? driveStepper(-1, val) : driveStepper(1, val);
}

void driveStepper(short int dir, int val){
  uni1.setSpeed(val*dir);
  uni1.step(2);
}
