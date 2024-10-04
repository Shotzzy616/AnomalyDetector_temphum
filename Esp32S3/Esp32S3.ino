#include <WiFi.h>
#include <HTTPClient.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

#define DHTPIN D0     // D0 pin connected to the DHT11
#define DHTTYPE DHT11 // DHT11 sensor
DHT dht(DHTPIN, DHTTYPE);

// RGB LED pins
#define redPin D1   // D1
#define greenPin D2 // D2
#define bluePin D3  // D3

// WiFi credentials
const char* ssid = "Shotzzy";
const char* password = "cosmos1234";
const char* serverURL = "http://127.0.0.1:5000/data";

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Initialize the RGB LED pins
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void setRGBColor(int red, int green, int blue) {
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}

void loop() {
  // Read temperature and humidity from the DHT11 sensor
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if the readings are valid
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Send data to the server if WiFi is connected
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    // Create a JSON payload with the sensor data
    String jsonPayload = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);

      // Parse the prediction from the server response (assumes the prediction is returned as "Normal" or "Anomaly")
      if (response.indexOf("Normal") > 0) {
        setRGBColor(0, 255, 0); // Green for normal prediction
      } else if (response.indexOf("Anomaly") > 0) {
        setRGBColor(255, 0, 0); // Red for anomaly
      }

    } else {
      Serial.println("Error in sending POST request");
      setRGBColor(0, 0, 255); // Blue for an error
    }

    http.end();
    delay(1000); // Send data every 1 seconds
  }
}
