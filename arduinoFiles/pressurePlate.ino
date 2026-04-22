#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>


BLECharacteristic *pSensorCharacteristic = NULL;
#define SENSOR_UUID "abcd5678-abcd-5678-abcd-56789abcdef0"

const int fsrPin = 34;   // Analog pin (GPIO34 is input-only, perfect for this)
int fsrValue = 0;
bool stepActive = false;
int stepValue = 0;

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *pServer) override {
    Serial.println("BLE Connected");
    delay(1000);
  }

  void onDisconnect(BLEServer *pServer) override {
    Serial.println("BLE Disconnected");
    delay(500);
    BLEDevice::startAdvertising(); // Restart advertising
  }
};


void setup() {
  Serial.begin(115200);
  analogReadResolution(12);  // ESP32 uses 12-bit ADC (0–4095)¨

  BLEDevice::init("StepSensor_Left"); // Name the BLE device
    BLEServer *bleServer = BLEDevice::createServer();
    bleServer->setCallbacks(new MyServerCallbacks());

    BLEService *bleService = bleServer->createService(BLEUUID("12345678-1234-5678-1234-56789abcdef0"));

    // Create BLE characteristic for sensor data
    pSensorCharacteristic = bleService->createCharacteristic(
        SENSOR_UUID,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
    );
    pSensorCharacteristic->addDescriptor(new BLE2902());

    bleService->start();

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID("12345678-1234-5678-1234-56789abcdef0");
    BLEDevice::startAdvertising();
}

void loop() {
  stepValue = analogRead(fsrPin);

  if (stepValue > 500) {
    stepActive = true;
  } else {
    stepActive = false;
  }


  Serial.println("FSR Value: ");
  Serial.println(stepValue);

  // Konverterer værdierne til en string  og sender derefter over Bluetooth
        String data = String(stepActive);
        pSensorCharacteristic->setValue(data.c_str());
        pSensorCharacteristic->notify();

  delay(50);
}

