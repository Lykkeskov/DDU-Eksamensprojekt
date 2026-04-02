void setup() {
  Serial.begin(115200);  // Start USB serial at 115200 baud (enable USB_CDC_On_Boot for Serial)

  myCodeCell.Init(LIGHT);  // Enable Light + Proximity sensing

  // Add your custom initialization below
}

void loop() {
  if (myCodeCell.Run(10)) {     // Run every 10 Hz
    myCodeCell.PrintSensors();  // Print all enabled sensor values
  }
}
