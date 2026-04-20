const int fsrPin = 34;   // Analog pin GPIO34 
int fsrValue = 0;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);  // 12-bit 
}

void loop() {
  fsrValue = analogRead(fsrPin);

  Serial.println("FSR Value: ");
  Serial.println(fsrValue);

  delay(200);
}
