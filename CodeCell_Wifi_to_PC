#include <WiFi.h>
#include "esp_wpa2.h"
#include <CodeCell.h>
#include <WebServer.h>
#include <HTTPClient.h>

CodeCell myCodeCell;

const char* ssid = "eduroam";
const char* identity = "at102570@edu.aarhustech.dk"; //SKOLE EMAIL
const char* username = "at102570@edu.aarhustech.dk"; //SKOLE EMAIL
const char* password = "***REMOVED***"; //KODEORD TIL EMAIL

WebServer server(80);

void handleRoot() {
    int proximityValue = myCodeCell.Light_ProximityRead(); // Read proximity sensor
    String response = "Proximity: "; 
    response += String(proximityValue);
    server.send(200, "text/html", response);  

}

void sendData(int value) {
    HTTPClient http;

    http.begin("http://10.147.131.14:5000/data"); // your computer server
    http.addHeader("Content-Type", "application/json");

    String json = "{\"proximity\":" + String(value) + "}";

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
