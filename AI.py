import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X = np.load('login_attempts.npy')
y = np.load('login_labels.npy')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

rf = RandomForestClassifier(n_estimators=10)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print('Model accuracy:', accuracy)

login_attempts = [...]
login_features = [...]
if rf.predict(login_features).mean() > 0.9:
    print('Brute-force attack detected!')
