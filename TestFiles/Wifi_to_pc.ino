
#include <WiFi.h>
#include "esp_wpa2.h"
#include <CodeCell.h>
#include <WebServer.h>
#include <HTTPClient.h>

CodeCell myCodeCell;

const char* ssid = "";
const char* password = ""; //KODEORD TIL EMAIL


const char* identity = ""; //SKOLE EMAIL
const char* username = ""; //SKOLE EMAIL 


void sendData() {
    HTTPClient http;

    http.begin("http://000.00.000:5000/data");
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

    Serial.println(json);  // DEBUG

    int httpResponseCode = http.POST(json);
    Serial.println(httpResponseCode);

    http.end();
}

void setup() {
    Serial.begin(115200);
    myCodeCell.Init(MOTION_ACCELEROMETER + MOTION_ROTATION + MOTION_LINEAR_ACC); // Set up CodeCell's light sensor
    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);

    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)identity, strlen(identity));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)username, strlen(username));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)password, strlen(password));  

    esp_wifi_sta_wpa2_ent_enable();   

    WiFi.begin(ssid, password);

    Serial.print("Connecting to eduroam");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

}

void loop() {
   // Run every 10Hz
    if (myCodeCell.Run(5)) {     // Run every 5 Hz
    sendData();
  }
}
