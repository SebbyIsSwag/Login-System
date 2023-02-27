import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from flask import Flask, request, jsonify

X, y = make_classification(n_samples=1000, n_features=10, random_state=42)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    x = np.array(data['features']).reshape(1, -1)
    
    y_pred = rf.predict(x)
    
    response = {'prediction': int(y_pred[0])}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
