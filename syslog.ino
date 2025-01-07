#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "";
const char* password = "";

WiFiUDP udp;
unsigned int localUdpPort = 514;
char incomingPacket[255];

const int builtinled = LED_BUILTIN;

void setup() {
    Serial.begin(115200);
    pinMode(builtinled, OUTPUT);
    digitalWrite(builtinled, HIGH);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        digitalWrite(builtinled, LOW);
        delay(1000);
        digitalWrite(builtinled, HIGH);
    }
    Serial.printf("IP address: %s\n", WiFi.localIP().toString().c_str());
    udp.begin(localUdpPort);
    Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
}

void loop() {
    int packetSize = udp.parsePacket();
    if (packetSize) {
        int len = udp.read(incomingPacket, 255);
        if (len > 0) {
            incomingPacket[len] = '\0';
        }
        Serial.printf("Received packet of size %d from %s:%d\n", packetSize, udp.remoteIP().toString().c_str(), udp.remotePort());
        Serial.printf("Packet content: %s\n", incomingPacket);
        digitalWrite(builtinled, LOW);
        delay(100);
        digitalWrite(builtinled, HIGH);
        delay(100);
    }
    delay(10);
}