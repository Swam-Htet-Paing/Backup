#include<Wire.h>
const int MPU_addr=0x68;
int16_t axis_X,axis_Y,axis_Z;
int minVal=265;
int maxVal=402;
double x;
double y;
double z;
double angle = 0.0;
float prevAngle = 0.0;
double drive = 0;
unsigned long loop_time;
float integral;

double PID(short int setPoint, short int reading, unsigned char dt);
double get_angle();
void drive_motors(double val);

void setup(){
  pinMode(9,OUTPUT);
  pinMode(5,OUTPUT);
  pinMode(6,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
  Serial.begin(9600);
  loop_time = millis() + 4;
}
void loop(){
  angle = get_angle();
  drive = PID(0, angle, 4); 
  drive_motors(drive);
  while (loop_time > millis());
  loop_time += 4;
}

double PID(short int setPoint, short int reading, unsigned char dt){
  float Kp = 0.4;
  float Ki = 0.7;
  float Kd = 0.3;
  
  float error = (float)setPoint - (float)reading;
  integral += error * dt;
  
  float PID_output = (Kp * error) + (Ki * integral) + (Kd * ((prevAngle - reading)/dt)); 
  if(PID_output > 255)
    PID_output = 255;
  else if (PID_output < 0)
    PID_output = 0;
  return PID_output;
}

void drive_motors(double val){
  analogWrite(9,val);
  digitalWrite(5,HIGH);
  digitalWrite(6,LOW);
  analogWrite(11,val);
  digitalWrite(7,HIGH);
  digitalWrite(8,LOW);
}

double get_angle(){  
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);
  axis_X=Wire.read()<<8|Wire.read();
  axis_Y=Wire.read()<<8|Wire.read();
  axis_Z=Wire.read()<<8|Wire.read();
    int xAng = map(axis_X,minVal,maxVal,-90,90);
    int yAng = map(axis_Y,minVal,maxVal,-90,90);
    int zAng = map(axis_Z,minVal,maxVal,-90,90);
       x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
       y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
       z= RAD_TO_DEG * (atan2(-yAng, -xAng)+PI);
     //Serial.print("Angle of inclination in X axis = ");
//     Serial.print(x);
//     Serial.println((char)176);
//     Serial.print("Angle of inclination in Y axis= ");
     if (y <=0.7)
       y = 0;
     else if (y > 90 && y <= 270)
      y = 0;
     else if (y > 270)
      y -= 361;
     return y;
}
