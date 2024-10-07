#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>

// DHT11 sensor configuration
#define DHTPIN D0          // Pin where the DHT11 is connected
#define DHTTYPE DHT11     // Define the sensor type (DHT11)
#define RED_PIN D1
#define GREEN_PIN D2
#define BLUE_PIN D3

DHT dht(DHTPIN, DHTTYPE);

// WiFi configuration
const char* ssid = "Shotzzy";       // Your WiFi SSID
const char* password = "cosmos1234"; // Your WiFi Password
const char* serverUrl = "http://192.168.100.62:5000/send_data"; // Your Flask server URL

// NTP time settings
const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;  // Adjust if you're not in GMT
const int daylightOffset_sec = 0;  // Adjust for daylight savings

void setup() {
  Serial.begin(115200);
  
  // Initialize DHT sensor
  dht.begin();

  // Initialize RGB LED pins
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  // Turn off the LED at the beginning
  digitalWrite(RED_PIN, LOW);
  digitalWrite(GREEN_PIN, LOW);
  digitalWrite(BLUE_PIN, LOW);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }

  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  // Initialize NTP for time synchronization
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

String getFormattedTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return "0000-00-00 00:00:00.000000";
  }
  
  char buffer[64];
  strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timeinfo);

  // Add milliseconds to the timestamp
  unsigned long ms = millis() % 1000;
  sprintf(buffer + strlen(buffer), ".%03lu", ms);

  return String(buffer);
}

// Function to blink blue LED with different frequencies based on error type
void blinkBlue(int frequency) {
  for (int i = 0; i < frequency; i++) {
    digitalWrite(BLUE_PIN, HIGH);
    delay(200);
    digitalWrite(BLUE_PIN, LOW);
    delay(200);
  }
}

void loop() {
  // Wait a few seconds between measurements
  delay(1000);

  // Read temperature and humidity
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Check if any reads failed and exit early
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    blinkBlue(2);
    return;
  }

  // Get formatted timestamp
  String timestamp = getFormattedTime();

  // Create JSON payload
  String postData = "{\"temperature\": " + String(temperature) +
                    ", \"humidity\": " + String(humidity) +
                    ", \"timestamp\": \"" + timestamp + "\"}";

  // Send the data to the Flask server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Specify content type and server endpoint
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Send POST request
    int httpResponseCode = http.POST(postData);

    // Check response
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("POST Response: " + response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
      blinkBlue(3);
    }

    // End HTTP connection
    http.end();
  } else {
    Serial.println("Error in WiFi connection");
  }
}
