import joblib
import numpy as np
import pandas as pd
import requests
from sklearn.preprocessing import StandardScaler

def receive_data():
    url = "http://127.0.0.1:5000/send"
    response = requests.get(url)
    data = response.json()
    return data

def send_data(data):
    url = "http://127.0.0.1:5000/voice"
    response = requests.post(url, json=data)
    return response.status_code == 200

svm_model = joblib.load('one_class_svm_model.pkl')
scaler = joblib.load('scaler.pkl')

new_data = receive_data()
print(new_data)
new_data_scaled = scaler.transform(new_data)

predictions = svm_model.predict(new_data_scaled)
print(predictions)


