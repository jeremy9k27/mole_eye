import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from model_data import data

X = np.array([row[0:3] for row in data])
diff = X[:, 2] - X[:, 1]
X = np.hstack((X, diff.reshape(-1, 1)))
#X = X[:,(0,3)]
y = np.array([row[3] for row in data])

# Convert categorical target to numerical
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Create and train the Random Forest model
rf = RandomForestClassifier(n_estimators=50, random_state=42)
rf.fit(X_train, y_train)

# Make predictions
y_pred = rf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
#print(f"Accuracy: {accuracy * 100:.2f}%")
#print(X_test, y_test, y_pred)

def classify_single(X_test):
    return le.inverse_transform(rf.predict(X_test))