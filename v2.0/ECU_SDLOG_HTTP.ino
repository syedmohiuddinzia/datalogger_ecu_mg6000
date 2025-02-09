#include "FS.h"
#include "SD.h"
#include "SPI.h"

// ============================================================================

#include "WiFi.h"
#include "ESPAsyncWebServer.h"

// ============================================================================

// Set up a buffer to hold the received data packet
#define PACKET_SIZE 256 //82
char dataPacket[PACKET_SIZE + 1];  // +1 for null termination
const char* csvData;
String packet;

// ============================================================================

const char* ssid = "ECU_dataLogger";
const char* password = "44445555";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// ============================================================================

unsigned long previousMillis = 0;  // Stores last time the message was sent
const long interval = 1000;  // Interval in milliseconds

// ============================================================================

#define NET_LED 15
#define REC_LED 2
#define MMC_LED 4  

// ============================================================================


// Delete file
void deleteFile(fs::FS &fs, const char *path) {
  Serial.printf("Deleting file: %s\r\n", path);
  if (fs.remove(path)) {
    Serial.println("- file deleted");
  } else {
    Serial.println("- delete failed");
  }
}


void setup() {

    pinMode(NET_LED, OUTPUT);
    pinMode(REC_LED, OUTPUT);
    pinMode(MMC_LED, OUTPUT);
    
    Serial.begin(115200, SERIAL_8N1); // 9600 baud rate, 8 data bits, no parity, 1 stop bit
    while (!Serial);
    Serial2.begin(115200, SERIAL_8N1, 16, 17); // 9600 baud rate, 8 data bits, no parity, 1 stop bit
    while (!Serial2);
    // ============================================================================

#ifdef REASSIGN_PINS
    SPI.begin(sck, miso, mosi, cs);
    if (!SD.begin(cs)) {
#else
    if (!SD.begin()) {
#endif
        Serial.println("Card Mount Failed");
        return;
    }

    uint8_t cardType = SD.cardType();
    if (cardType == CARD_NONE) {
        Serial.println("No SD card attached");
        return;
    }

    Serial.print("SD Card Type: ");
    if (cardType == CARD_MMC) {
        Serial.println("MMC");
    } else if (cardType == CARD_SD) {
        Serial.println("SDSC");
    } else if (cardType == CARD_SDHC) {
        Serial.println("SDHC");
    } else {
        Serial.println("UNKNOWN");
    }

    // Setting the ESP as an access point
    Serial.println("Setting AP (Access Point)…");
    // You can remove the password parameter if you want the AP to be open.
    // a valid password must have more than 7 characters
    if (!WiFi.softAP(ssid, password)) {
      log_e("Soft AP creation failed.");
      while (1);
    }
    IPAddress myIP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(myIP);

    // Handle the root URL
    server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
      request->send(SD, "/index.html", "text/html");
    });

    // Handle the download button
  server.on("/download", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SD, "/hello.txt", String(), true);
  });

  // Handle the View Data button
  server.on("/view-data", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(SD, "/hello.txt", "text/plain", false);
  });

  // Handle the delete button
  server.on("/delete", HTTP_GET, [](AsyncWebServerRequest *request) {
    deleteFile(SD, "/hello.txt");
    request->send(200, "text/plain", "data.txt was deleted.");
  });
  
    server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
        request->send_P(200, "text/plain", packet.c_str());
    });

    // Start server
    server.begin();
}

// ============================================================================

void appendFile(fs::FS &fs, const char *path, const char *message) {
    Serial.printf("Appending to file: %s\n", path);
    File file = fs.open(path, FILE_APPEND);
    if (!file) {
        Serial.println("Failed to open file for appending");
        return;
    }
    if (file.print(message)) {
        Serial.println("Message appended");
        digitalWrite(MMC_LED, HIGH);  // GET /L turns the LED off
    } else {
        Serial.println("Append failed");
    }
    file.close();
}

//void ECUdata() {
//    digitalWrite(REC_LED, LOW);  // GET /L turns the LED off
//    unsigned long currentMillis = millis();
//    if (currentMillis - previousMillis >= interval) {
//        previousMillis = currentMillis;  // Update last sent time
//        // Send the character 'a' to request a data packet
//        Serial2.println("a");  // Send "a" via Serial2
//        Serial.println("Sent: a");  // Debug output in Serial Monitor
//    }
//    if (Serial2.available()) {
//    digitalWrite(REC_LED, HIGH);  // GET /L turns the LED off
//    // Read the 82-byte data packet from the SoftwareSerial
//    size_t bytesRead = Serial2.readBytes(dataPacket, PACKET_SIZE);
//    dataPacket[bytesRead] = '\0';  // Ensure null-termination
//    Serial.println(dataPacket);
//    csvData = dataPacket;  // Assign pointer
//    appendFile(SD, "/hello.txt", csvData);
//    }
//    digitalWrite(MMC_LED, LOW);  // GET /L turns the LED off
//}

void ECUdata() {
    digitalWrite(REC_LED, LOW);  // GET /L turns the LED off
    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;  // Update last sent time
        // Send the character 'a' to request a data packet
        Serial2.write("a");  // Send "a" via Serial2
//        Serial.println("Sent: a");  // Debug output in Serial Monitor
        Serial.println(packet);
        appendFile(SD, "/hello.txt", packet.c_str());
    }
    static String hexData = "";  
    digitalWrite(REC_LED, HIGH);  // GET /L turns the LED off
    // Read the 82-byte data packet from the SoftwareSerial
    while (Serial2.available()) {byte data = Serial2.read();hexData += (data < 0x10 ? "0" : "") + String(data, HEX) + " ";}
    if (!hexData.isEmpty()) {Serial.println("ECU Response: " + hexData); packet= hexData; hexData = "";}  // Clear after printing
    digitalWrite(MMC_LED, LOW);  // GET /L turns the LED off
}

void loop() {
    ECUdata();
    int numClients = WiFi.softAPgetStationNum();  // Get number of connected clients
//    Serial.print("Connected Clients: ");
//    Serial.println(numClients);
    if (numClients > 0) {
//        Serial.println("At least one client is connected!");
        digitalWrite(NET_LED, HIGH);  // GET /L turns the LED off
    } else {
//      Serial.println("No clients connected.");
        digitalWrite(NET_LED, LOW);  // GET /L turns the LED off
    }
}
