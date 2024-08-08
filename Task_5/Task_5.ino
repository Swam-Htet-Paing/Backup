#include <LiquidCrystal_I2C.h>
#include <Bonezegei_DHT11.h>
#include <SD.h>
#include <SPI.h>

LiquidCrystal_I2C lcd(0x27,16,2);
Bonezegei_DHT11 dht(2);
File datafile;
float temp = 0;
int hum = 0;
unsigned long previous = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  lcd.init();
  lcd.backlight();
  if(!SD.begin(10)){
    Serial.println("SD card initialization failed.");
  }
  Serial.println("SD card initialization done.");
  datafile = SD.open("Temperature_And_Humidity_Data.txt", FILE_WRITE);
  if (datafile){
    datafile.println("Data recording for every one hour started.");
    datafile.close();
  }
  else
    Serial.println("Error opening txt file.");
}

void loop() {
  // put your main code here, to run repeatedly:
  unsigned long wait_1hour = millis();
  if (wait_1hour - previous >= 3600000){
    previous = wait_1hour; 
    if (dht.getData()){
      temp = dht.getTemperature();
      hum = dht.getHumidity();
    }
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Temp(C): ");
    lcd.setCursor(11,0);
    lcd.print(String(temp));
    lcd.setCursor(0,1);
    lcd.print("Humidity: ");
    lcd.setCursor(11,1);
    lcd.print(String(hum));
    datafile = SD.open("Temperature_And_Humidity_Data.txt", FILE_WRITE);
    if (datafile){
      datafile.print("Temperature in Deg C : ");
      datafile.println(String(temp));
      datafile.print("Humidity : ");
      datafile.println(String(hum));
      datafile.close();
    }
    else
      Serial.println("Error opening txt file.");
    Serial.print("Temperature in Deg C : ");
    Serial.println(temp);
    Serial.print("Humidity : ");
    Serial.println(hum);
  }  
}
