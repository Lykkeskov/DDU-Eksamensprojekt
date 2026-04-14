// testkode til knyttet/åben hånd m. stretch sensor
// Nu bruger vi CodeCell C3 i stedet for Arduino UNO. Se tidligere commit for Arduino version: https://github.com/Lykkeskov/DDU-Eksamensprojekt/commit/e09e7cadb47d8a1a6825ed94518d2c57081b8c6f#diff-555a3769563a6809d7aa18cfc66e36a1efeb52e8dcc6c21aba2c164891c4e84f
const int sensorPin = 2;  // GPIO2
int sensorValue = 0;

int threshold = 2400; // ESP32 har højere opløsning (0–4095)

void setup() {
  Serial.begin(115200);
}

void loop() {
  sensorValue = analogRead(sensorPin);

  Serial.print("Stretch value: ");
  Serial.println(sensorValue);

  if (sensorValue < threshold) {
    Serial.println("KNYTTET");
  } else {
    Serial.println("ÅBEN");
  }

  delay(200);
}
