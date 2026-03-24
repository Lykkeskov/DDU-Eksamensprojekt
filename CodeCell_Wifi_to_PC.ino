#include <WiFi.h>
#include "esp_wpa2.h"
#include <CodeCell.h>
#include <WebServer.h>
#include <HTTPClient.h>

CodeCell myCodeCell;

const char* ssid = "eduroam";
const char* identity = ""; //SKOLE EMAIL
const char* username = ""; //SKOLE EMAIL
const char* password = ""; //KODEORD TIL EMAIL

WebServer server(80);

void handleRoot() {
      int proximity = myCodeCell.Light_ProximityRead();

    float ax, ay, az;
    float gx, gy, gz;

    myCodeCell.Motion_AccelerometerRead(ax, ay, az);
    myCodeCell.Motion_GyroRead(gx, gy, gz);

    // Build JSON json
    String json = "{";
    json += "\"proximity\":" + String(proximity) + ",";

    json += "\"accelerometer\":{";
    json += "\"x\":" + String(ax) + ",";
    json += "\"y\":" + String(ay) + ",";
    json += "\"z\":" + String(az) + "},";

    json += "\"gyroscope\":{";
    json += "\"x\":" + String(gx) + ",";
    json += "\"y\":" + String(gy) + ",";
    json += "\"z\":" + String(gz) + "}";

    json += "}";

    server.send(200, "application/json", json);

}

void sendData(int value) {
    HTTPClient http;

    http.begin("http://10.147.131.95:5000/data"); // your computer server
    http.addHeader("Content-Type", "application/json");
    
    float ax, ay, az;
    float gx, gy, gz;

    myCodeCell.Motion_AccelerometerRead(ax, ay, az);
    myCodeCell.Motion_GyroRead(gx, gy, gz);

    // Build JSON json
    String json = "{";
    json += "\"accelerometer\":{";
    json += "\"x\":" + String(ax) + ",";
    json += "\"y\":" + String(ay) + ",";
    json += "\"z\":" + String(az) + "},";

    json += "\"gyroscope\":{";
    json += "\"x\":" + String(gx) + ",";
    json += "\"y\":" + String(gy) + ",";
    json += "\"z\":" + String(gz) + "}";

    json += "}";


    int httpResponseCode = http.POST(json);

    Serial.println(httpResponseCode);

    http.end();
}

void setup() {
    Serial.begin(115200);
    myCodeCell.Init(LIGHT); // Set up CodeCell's light sensor
    WiFi.disconnect(true);
    WiFi.mode(WIFI_STA);

    esp_wifi_sta_wpa2_ent_set_identity((uint8_t *)identity, strlen(identity));
    esp_wifi_sta_wpa2_ent_set_username((uint8_t *)username, strlen(username));
    esp_wifi_sta_wpa2_ent_set_password((uint8_t *)password, strlen(password));

    esp_wifi_sta_wpa2_ent_enable();

    WiFi.begin(ssid);

    Serial.print("Connecting to eduroam");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nConnected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    server.on("/", handleRoot);
    server.begin();
    Serial.println("HTTP server started");
}

void loop() {
   // Run every 10Hz
    if (myCodeCell.Run(10)) {     // Run every 10 Hz
    int value = myCodeCell.Light_ProximityRead();
    sendData(value);
  }
}
