//Task 2

int Buzz = 8, Trig = 3, Echo = 7, LED = 12;

void setup() {
  // put your setup code here, to run once:
  pinMode(Trig, OUTPUT);
  pinMode(Buzz, OUTPUT);
  pinMode(LED, OUTPUT);
  pinMode(Echo, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int s = distance();
  if(s > 50){
    flash();
    digitalWrite(Buzz, LOW);
  }
  else{
    digitalWrite(LED, HIGH);
    digitalWrite(Buzz, HIGH);
  }
}

int distance(){
  digitalWrite(Trig,HIGH);
  delayMicroseconds(10);
  digitalWrite(Trig,LOW);
  int duration = pulseIn(Echo,HIGH);
  int distance = 0.0343 * duration / 2;
  Serial.println(distance);
  return distance;
}

void flash(){
  digitalWrite(LED,HIGH);
  delay(200);
  digitalWrite(LED,LOW);
  delay(200);
}
