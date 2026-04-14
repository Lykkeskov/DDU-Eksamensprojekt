// testkode til at måle knyttet hånd m. flex sensor
const int flexPin = A0;   // Flex sensor på analog pin A0
int flexValue = 0;

int threshold = 225;      // Juster  efter målinger

void setup() {
  Serial.begin(9600);
}

void loop() {
  flexValue = analogRead(flexPin);

  Serial.print("Flex value: ");
  Serial.println(flexValue);

  if (flexValue < threshold) {
    Serial.println("Hånd er KNYTTET");
  } else {
    Serial.println("Hånd er ÅBEN");
  }

  delay(200);
}
