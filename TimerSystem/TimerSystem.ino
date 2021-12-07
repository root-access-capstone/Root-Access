#define FLOAT_SENSOR  24
#define PUMP 4
#define LIGHT A1
#define LIGHT_SWITCH 2

int powerPin = 13;
int incomingByte;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(powerPin, OUTPUT);
  pinMode(PUMP, OUTPUT);
  pinMode(FLOAT_SENSOR, INPUT_PULLUP);
  digitalWrite(powerPin, HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
  incomingByte = Serial.read();
  char buffer[20];
  lightValue = analogRead(LIGHT);
  if(digitalRead(FLOAT_SENSOR) == LOW){
    Serial.println('LOW');
  }else{
    Serial.println('HIGH');
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
