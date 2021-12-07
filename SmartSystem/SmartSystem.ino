#include <dht.h>

dht DHT;

#define DHT11_PIN 22
#define FLOAT_SENSOR  24
#define PUMP 4
#define MOISTURE A0
#define LIGHT A1
#define LIGHT_SWITCH 2

int powerPin = 13;
int temp;
int hum;
int moistureValue;
int lightValue;
int incomingByte;
//bool pumpOn = false;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(powerPin, OUTPUT);
  pinMode(PUMP, OUTPUT);
  pinMode(LIGHT_SWITCH, OUTPUT);
  pinMode(FLOAT_SENSOR, INPUT_PULLUP);
  digitalWrite(powerPin, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  incomingByte = Serial.read();
  char buffer[20];
  int chk = DHT.read11(DHT11_PIN);
  temp = DHT.temperature;
  hum = DHT.humidity;
  moistureValue = analogRead(MOISTURE);
  lightValue = analogRead(LIGHT);
  if(digitalRead(FLOAT_SENSOR) == LOW){
    sprintf(buffer, "%d,%d,%d,%d,HIGH,%d", temp, hum, moistureValue, lightValue, incomingByte);
    Serial.println(buffer);
  }else{
    sprintf(buffer, "%d,%d,%d,%d,LOW,%d", temp, hum, moistureValue, lightValue, incomingByte);
    Serial.println(buffer);
  }
  
  switch(incomingByte){
    case 65:
      digitalWrite(PUMP, HIGH);
      break;
    case 66:
      digitalWrite(PUMP, LOW);
      break;
    case 67:
      digitalWrite(LIGHT_SWITCH, HIGH);
      break;
    case 68:
      digitalWrite(LIGHT_SWITCH, LOW);
      break;
  }
  delay(2000);
}
