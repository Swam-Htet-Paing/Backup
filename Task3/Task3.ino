#include <LiquidCrystal_I2C.h>

int T1 = 5, E1 = 4, T2 = 6, E2 = 7, m1 = 10, m2 = 12, motor = 11; 
int onTrack = 0, sent = 0;
LiquidCrystal_I2C lcd(0x27,16,2);

void setup() {
  // put your setup code here, to run once:
  lcd.init();
  lcd.backlight();
  pinMode(T1,OUTPUT);
  pinMode(E1,INPUT);
  pinMode(T2,OUTPUT);
  pinMode(E2,INPUT);
  pinMode(motor,OUTPUT);
  pinMode(m1,OUTPUT);
  pinMode(m2,OUTPUT);  
}

void loop() {
  // put your main code here, to run repeatedly:
//  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("on track: ");
  lcd.setCursor(0,1);
  lcd.print("Exported: ");
  int d1 = distance(T1, E1);
  int d2 = distance(T2, E2);
  if(d1 >= 5 && d1 <= 15){
     onTrack++;
     lcd.setCursor(11,0);
     lcd.print(String(onTrack));
     delay(1000);
  }
  if(d2 >= 5 && d2 <= 15){
     onTrack--;
     sent++;
     lcd.setCursor(11,1);
     lcd.print(String(sent));
     delay(1000);
  }
  if(onTrack == 0)
     Drive(0);
  else if(onTrack != 0)
     Drive(65);
}

int distance(int Trig, int Echo){
  digitalWrite(Trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig,LOW);
  int duration = pulseIn(Echo,HIGH);
  int distance = 0.0343 * duration / 2;
  Serial.println(distance);
  return distance;
}

void Drive(int val){
  analogWrite(motor,val);
  digitalWrite(m1,HIGH);
  digitalWrite(m1,LOW);
}
