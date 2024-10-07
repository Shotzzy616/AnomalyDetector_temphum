from flask import Flask, request, jsonify, render_template, redirect, url_for
import joblib, os
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the trained model and scaler
model_path = 'one_class_svm_model.pkl'
scaler_path = 'scalar.pkl'

if os.path.exists(model_path) and os.path.exists(scaler_path):
    svm_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
else:
    raise FileNotFoundError("Model or scaler file not found.")

# Initialize CSV file for storing data
csv_file = 'data.csv'
csv_prediction = 'prediction.csv'

# Check if the CSV file exists, and create it with headers if not
if not os.path.exists(csv_file):
    with open(csv_file, 'w') as f:
        f.write('Timestamp,Temperature (°C),Humidity (%)\n')
        
if not os.path.exists(csv_prediction):
    with open(csv_prediction, 'w') as f:
        f.write('Timestamp,Temperature (°C),Humidity (%),Prediction\n')
        
        
        
@app.route("/")
def home():
    return render_template("index.html")  # Ensure your HTML file is named index.html and in the templates folder


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("index.html")
    
@app.route("/home")
def user(usr):
    return f"<h1>Welcome, {usr}!</h1>"


@app.route('/send_data', methods=['POST'])
def receive_data():
    global csv_file
    # Get JSON data from ESP32S3
    data = request.json
    
    # Extract temperature and humidity
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    timestamp = data.get('timestamp')
    
    if temperature is not None and humidity is not None:
        # Create a DataFrame for the new data
        new_data = pd.DataFrame({
            'Timestamp': [timestamp],
            'Temperature (°C)': [temperature],
            'Humidity (%)': [humidity]
        })
        test_data = new_data[['Temperature (°C)','Humidity (%)']]

        # Append new data to the CSV file
        new_data.to_csv(csv_file, mode='a', header=False, index=False)

        # Normalize new data and predict anomalies
        new_data_scaled = scaler.transform(test_data)
        prediction = svm_model.predict(new_data_scaled)

        # Return response
        response = {
            'timestamp': timestamp,
            'temperature': temperature,
            'humidity': humidity,
            'prediction': int(prediction[0]),  # 1 for normal, -1 for anomaly
        }
        
        predict = pd.DataFrame({
            'Timestamp': [timestamp],
            'Temperature (°C)': [temperature],
            'Humidity (%)': [humidity],
            'prediction': [int(prediction[0])]
        })

        # Append new data to the CSV file
        predict.to_csv(csv_prediction, mode='a', header=False, index=False)
        
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid data received."}), 400

@app.route('/get_data', methods=['GET'])
def send_data():
    render_template('data.html')
    # Load historical data for the last n entries
    data_history = pd.read_csv(csv_prediction)
    return jsonify(data_history.tail(10).to_dict(orient='records')), 200  # Returns the last 10 predictions

@app.route('/latest_data', methods=['GET'])
def latest_data():
    # Read the latest data from the CSV file
    if os.path.exists(csv_prediction):
        df = pd.read_csv(csv_prediction)
        # Get the latest entry
        latest_entry = df.tail(1).to_dict(orient='records')[0]
        return jsonify(latest_entry), 200
    else:
        return jsonify({"error": "No data available."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
