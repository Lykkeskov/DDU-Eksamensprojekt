#include <WiFi.h>
#include "esp_wpa2.h"

const char* ssid = "eduroam";
const char* identity = "email"; //SKOLE EMAIL
const char* username = "email"; //SKOLE EMAIL
const char* password = "kodeord"; //KODEORD TIL EMAIL

void setup() {
    Serial.begin(9600);

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
    Serial.println(WiFi.localIP());
}

void loop() {}





