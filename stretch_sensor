// testkode til knyttet/åben hånd m. stretch sensor
const int sensorPin = A0;
int sensorValue = 0;

int threshold = 520; // juster efter kalibrering

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(sensorPin);

  Serial.print("Stretch value: ");
  Serial.println(sensorValue);

  if (sensorValue < threshold) {
    Serial.println("Hånd er KNYTTET");
  } else {
    Serial.println("Hånd er ÅBEN");
  }

  delay(200);
}
