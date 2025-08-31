import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 1. data load
df = pd.read_csv("urldata_features10.csv")

# 2. using feature
features = [
    'hostname_length', 'count_dir', 'count-www',
    'url_length', 'fd_length', 'count-', 'count.',
    'tld_length', 'count-digits', 'count='
]

X = df[features]
y = df['label']

# 3. train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 4. model training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. model performance evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=["Benign", "Malicious"])

print("model performance evaluation:")
print(f"Accuracy: {accuracy:.4f}")
print(report)

# 6. model save
joblib.dump(model, "url_model_new.pkl")
print("model training and saving clear! (url_model_new.pkl)")