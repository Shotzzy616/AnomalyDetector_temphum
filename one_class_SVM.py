from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd

data = pd.read_csv('humidity_temperature_data.csv')

x = data[['Temperature (°C)','Humidity (%)']]

scalar = StandardScaler()
x_scaled = scalar.fit_transform(x)
print(x.head())

svm_model = OneClassSVM(kernel='rbf', gamma='auto', nu=0.05)
svm_model.fit(x_scaled)

joblib.dump(svm_model, "one_class_svm_model.pkl")
joblib.dump(scalar, "scalar.pkl")

predictions = svm_model.predict(x_scaled)
print(predictions)

data['predictions'] = predictions
print(data.head())