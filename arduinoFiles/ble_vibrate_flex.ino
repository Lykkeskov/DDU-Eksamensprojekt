#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <BLE2902.h>

#include <CodeCell.h>
CodeCell myCodeCell;

// UUIDs
#define SERVICE_UUID        "12345678-1234-5678-1234-56789abcdef0"
#define SENSOR_UUID         "abcd5678-abcd-5678-abcd-56789abcdef0"
#define COMMAND_UUID        "dcba4321-dcba-4321-dcba-4321fedcba98"

// Pins
const int motorPin = 3;
const int flexPin = 2;

// BLE
BLECharacteristic *sensorCharacteristic;
BLECharacteristic *commandCharacteristic;

// Vibration
bool vibrating = false;
unsigned long vibrateStart = 0;
int vibrateDuration = 200;

// Flex threshold
// High values = open hand, low values = closed fist
int threshold = 1150;

// RECEIVE COMMAND
class CommandCallback : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) override {
    String value = pCharacteristic->getValue();

    if (value == "V") {
      Serial.println("VIBRATE");

      digitalWrite(motorPin, HIGH);
      vibrating = true;
      vibrateStart = millis();
    }
  }
};

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("BOOTED");

    myCodeCell.Init(MOTION_ACCELEROMETER + MOTION_ROTATION + MOTION_LINEAR_ACC);

    pinMode(motorPin, OUTPUT);
    digitalWrite(motorPin, LOW);

    pinMode(flexPin, INPUT);

    analogReadResolution(12); // 0-4095

    BLEDevice::init("CodeCell_1");

    BLEServer *server = BLEDevice::createServer();
    BLEService *service = server->createService(SERVICE_UUID);

    sensorCharacteristic = service->createCharacteristic(
        SENSOR_UUID,
        BLECharacteristic::PROPERTY_NOTIFY
    );
    sensorCharacteristic->addDescriptor(new BLE2902());

    commandCharacteristic = service->createCharacteristic(
        COMMAND_UUID,
        BLECharacteristic::PROPERTY_WRITE
    );
    commandCharacteristic->setCallbacks(new CommandCallback());

    service->start();

    BLEAdvertising *advertising = BLEDevice::getAdvertising();
    advertising->addServiceUUID(SERVICE_UUID);
    BLEDevice::startAdvertising();

    Serial.println("BLE READY");
}

void loop() {
    if (myCodeCell.Run(10)) {
        float ax, ay, az;
        float rx, ry, rz;
        float lx, ly, lz;

        myCodeCell.Motion_AccelerometerRead(ax, ay, az);
        myCodeCell.Motion_RotationRead(rx, ry, rz);
        myCodeCell.Motion_LinearAccRead(lx, ly, lz);

        int flexValue = analogRead(flexPin);

        bool isFist = flexValue < 1150;

        Serial.print("Flex: ");
        Serial.print(flexValue);
        Serial.print(" | ");
        Serial.println(isFist ? "FIST" : "OPEN");

        String data = "{";
        data += "\"flex\":" + String(flexValue) + ",";
        data += "\"fist\":" + String(isFist ? "true" : "false") + ",";
        data += "\"ax\":" + String(ax) + ",";
        data += "\"ay\":" + String(ay) + ",";
        data += "\"az\":" + String(az) + ",";
        data += "\"rx\":" + String(rx) + ",";
        data += "\"ry\":" + String(ry) + ",";
        data += "\"rz\":" + String(rz) + ",";
        data += "\"lx\":" + String(lx) + ",";
        data += "\"ly\":" + String(ly) + ",";
        data += "\"lz\":" + String(lz);
        data += "}";

        sensorCharacteristic->setValue(data.c_str());
        sensorCharacteristic->notify();
    }

    if (vibrating && millis() - vibrateStart > vibrateDuration) {
        digitalWrite(motorPin, LOW);
        vibrating = false;
    }
}
