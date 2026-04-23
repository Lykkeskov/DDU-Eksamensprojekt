#include <CodeCell.h>

CodeCell myCodeCell;

void setup() {
  Serial.begin(115200);
  myCodeCell.Init(MOTION_ACCELEROMETER);
}

void loop() {
  myCodeCell.Run(10);

  float x, y, z;
  myCodeCell.Motion_AccelerometerRead(x, y, z);

  if (y > 2) {
    Serial.println("jump");
  }

  delay(50);
}
