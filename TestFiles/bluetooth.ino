#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#include <CodeCell.h>
CodeCell myCodeCell;

BLECharacteristic *pSensorCharacteristic = NULL; //'*' er en pointer, hvilket begynder den gemmer på memory adresser. Man bruger null så den ikke pointer til en random memory adresse.
#define SENSOR_UUID "abcd5678-abcd-5678-abcd-56789abcdef0" 

class MyServerCallbacks : public BLEServerCallbacks { //Class fortæller hvis nogen forbinder og afbryder forbindelsen. 
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
    BLEServer *bleServer = BLEDevice::createServer(); //Laver CodeCell c3 til en BLE server
    bleServer->setCallbacks(new MyServerCallbacks()); //Serveren ved hvornår noget forbinder og afbryder forbindelsen. 

    BLEService *bleService = bleServer->createService(BLEUUID("12345678-1234-5678-1234-56789abcdef0")); //serveren laver en service (hvilket er en obtainer/gruppe) som vil indholde charateristic

    // Create BLE characteristic for sensor data
    pSensorCharacteristic = bleService->createCharacteristic( 
        SENSOR_UUID,
        BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY //computeren kan både læse, men også få dataen. 
    );
    pSensorCharacteristic->addDescriptor(new BLE2902()); //laver en standard BLE descriptor ( Descriptors are defined attributes that describe a characteristic value)

    bleService->start(); 

    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising(); //gør så man kan forbinde computeren til CodeCell c3
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
