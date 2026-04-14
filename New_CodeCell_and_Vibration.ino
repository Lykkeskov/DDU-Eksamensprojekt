#include <WiFi.h>
#include "esp_wpa2.h"
#include <CodeCell.h>
#include <HTTPClient.h>
#include <WebServer.h>

CodeCell myCodeCell;

const char* ssid = ""; // navn på netværk
const char* password = ""; // password

const char* identity = ""; // email
const char* username = ""; // email

const char* serverUrl = "";

WebServer server(80);

const int motorPin = 3;

bool vibrating = false;
unsigned long vibrateStart = 0;
int vibrateDuration = 200;

// SEND SENSOR DATA
void sendData() {
    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    float ax, ay, az;
    float rx, ry, rz;
    float lx, ly, lz;

    myCodeCell.Motion_AccelerometerRead(ax, ay, az);
    myCodeCell.Motion_RotationRead(rx, ry, rz);
    myCodeCell.Motion_LinearAccRead(lx, ly, lz);

    String json = "{";
    json += "\"accelerometer\":{";
    json += "\"x\":" + String(ax, 3) + ",";
    json += "\"y\":" + String(ay, 3) + ",";
    json += "\"z\":" + String(az, 3) + "},";

    json += "\"motion\":{";
    json += "\"roll\":" + String(rx, 3) + ",";
    json += "\"pitch\":" + String(ry, 3) + ",";
    json += "\"yaw\":" + String(rz, 3) + "},";

    json += "\"lin\":{";
    json += "\"lx\":" + String(lx, 3) + ",";
    json += "\"ly\":" + String(ly, 3) + ",";
    json += "\"lz\":" + String(lz, 3) + "}";

    json += "}";

    int httpResponseCode = http.POST(json);
    Serial.println(httpResponseCode);

    http.end();
}

void vibrate(int duration) {
    digitalWrite(motorPin, HIGH);
    delay(duration);
    digitalWrite(motorPin, LOW);
}

// HANDLE VIBRATION REQUEST
void handleVibrate() {
    Serial.println("VIBRATE TRIGGERED");

    digitalWrite(motorPin, HIGH);
    vibrating = true;
    vibrateStart = millis();

    server.send(200, "text/plain", "OK");
}

void setup() {
    Serial.begin(115200);

    myCodeCell.Init(MOTION_ACCELEROMETER + MOTION_ROTATION + MOTION_LINEAR_ACC);

    pinMode(motorPin, OUTPUT);
    digitalWrite(motorPin, LOW);

    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);

    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)identity, strlen(identity));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)username, strlen(username));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)password, strlen(password));
    esp_wifi_sta_wpa2_ent_enable();

    WiFi.begin(ssid, password);

    Serial.print("Connecting...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Start vibration server
    server.on("/vibrate", handleVibrate);
    server.begin();
}

void loop() {
    server.handleClient();

    if (myCodeCell.Run(5)) {
        sendData();
    }
    // Handle vibration timing
    if (vibrating && millis() - vibrateStart > vibrateDuration) {
        digitalWrite(motorPin, LOW);
        vibrating = false;
}
}