#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#include <CodeCell.h>
CodeCell myCodeCell;

BLECharacteristic *pSensorCharacteristic = NULL;
#define SENSOR_UUID "abcd5678-abcd-5678-abcd-56789abcdef0"

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
     myCodeCell.Init(MOTION_ACCELEROMETER + MOTION_ROTATION + MOTION_LINEAR_ACC); // Initializer alle sensorer

    BLEDevice::init("CodeCell_Left"); // Name the BLE device
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
    if (myCodeCell.Run(10)) { // Read every 100ms (10Hz)
        float ax, ay, az;
        float rx, ry, rz;
        float lx, ly, lz;
        
        myCodeCell.Motion_AccelerometerRead(ax, ay, az);
        myCodeCell.Motion_RotationRead(rx, ry, rz);
        myCodeCell.Motion_LinearAccRead(lx, ly, lz);

        // Konverterer værdierne til en string  og sender derefter over Bluetooth
        String data = String(ax) + "," + String(ay) + "," + String(az) + "," + String(rx) + "," + String(ry) + "," + String(rz) + "," + String(lx) + "," + String(ly) + "," + String(lz);
        pSensorCharacteristic->setValue(data.c_str());
        pSensorCharacteristic->notify();
    }
}
