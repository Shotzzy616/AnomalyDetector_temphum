# AnomalyDetector_temphum
ESP32 Temperature and Humidity Monitoring System with Machine Learning

Here’s a brief description you can use for your GitHub project:

---

# Temperature and Humidity Monitoring System with Anomaly Detection

---

## Overview

---

This project implements a real-time temperature and humidity monitoring system using an ESP32S3 microcontroller and a DHT11 sensor. The system sends sensor data to a Flask server for storage and anomaly detection using a One-Class Support Vector Machine (SVM) model.

## Components Used

- **ESP32S3**: A powerful microcontroller with Wi-Fi capabilities, used for collecting sensor data and transmitting it to the server.
- **DHT11 Sensor**: A digital temperature and humidity sensor that provides accurate readings.
- **Flask**: A lightweight web framework for Python used to build the server.
- **One-Class SVM**: A machine learning model employed to detect anomalies in the sensor data.

## Project Features

- **Real-time Data Collection**: The ESP32S3 reads temperature and humidity data from the DHT11 sensor and sends it to the server in real-time.
- **Data Storage**: Sensor readings are stored in a CSV file on the server for further analysis and historical reference.
- **Anomaly Detection**: The One-Class SVM model predicts whether the incoming data is normal or anomalous based on previously collected data.
- **RESTful API**: The Flask server provides endpoints for data submission and retrieval, allowing for easy integration and access.

## Installation and Setup

1. Clone the repository to your local machine.
2. Set up the Flask server and ensure the model and scaler are trained and available.
3. Configure the ESP32S3 with the correct Wi-Fi credentials and server URL.
4. Upload the code to the ESP32S3 and monitor the data transmission through the Serial Monitor.

## Usage

- Send temperature and humidity data from the ESP32S3 to the Flask server.
- Monitor the predictions for anomalies in the sensor readings.
- Retrieve stored data from the server via the provided API endpoints.

## Future Improvements

- Implement a database for more robust data storage.
- Enhance the anomaly detection model with additional features.
- Create a web dashboard for real-time data visualization.

---
