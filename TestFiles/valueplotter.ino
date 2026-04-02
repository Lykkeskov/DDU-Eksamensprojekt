#include <CodeCell.h>

CodeCell myCodeCell;

void setup() {
  Serial.begin(115200);

  myCodeCell.Init(MOTION_LINEAR_ACC);

  // Optional: give plotter time to start
  delay(1000);
}

void loop() {
  if (myCodeCell.Run(10)) {  // 100 ms = 10 Hz
    float x, y, z;

    myCodeCell.Motion_LinearAccRead(x, y, z);

    // Proper Serial Plotter format (tab-separated + labels)
    Serial.print("X:");
    Serial.print(x);
    Serial.print("\t");

    Serial.print("Y:");
    Serial.print(y);
    Serial.print("\t");

    Serial.print("Z:");
    Serial.println(z);
  }
}
