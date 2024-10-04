from flask import Flask, request, jsonify, render_template, redirect, url_for
import joblib, os
import pandas as pd

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
csv_file = 'humidity_temperature_data.csv'

# Check if the CSV file exists, and create it with headers if not
if not os.path.exists(csv_file):
    with open(csv_file, 'w') as f:
        f.write('Timestamp,Temperature (°C),Humidity (%)\n')
        
        
        
@app.route("/home")
def home():
    return render_template("index.html", content="testing")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return  render_template("index.html")
    
@app.route("/<usr>")
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

        # Append new data to the CSV file
        new_data.to_csv(csv_file, mode='a', header=False, index=False)

        # Normalize new data and predict anomalies
        new_data_scaled = scaler.transform([[temperature, humidity]])
        prediction = svm_model.predict(new_data_scaled)

        # Return response
        response = {
            'timestamp': timestamp,
            'temperature': temperature,
            'humidity': humidity,
            'prediction': int(prediction[0]),  # 1 for normal, -1 for anomaly
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Invalid data received."}), 400

@app.route('/data', methods=['GET'])
def get_data():
    """Endpoint to retrieve stored data from the CSV file."""
    df = pd.read_csv(csv_file)
    return df.to_json(orient='records'), 200


if __name__ == '__main__':
    app.run(debug=True)