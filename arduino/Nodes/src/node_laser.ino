void setup() {
  pinMode(9,OUTPUT);
  Serial.begin(115200);
}

void loop() {
  Serial.println("ciao"):
  digitalWrite(9,HIGH);
  delay(700);
  digitalWrite(9,LOW);
  delay(700);
}
