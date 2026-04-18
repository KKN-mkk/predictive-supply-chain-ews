import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle

print("🌍 Starting ML Supply Chain Pipeline...")

# 1. Load the Data
print("Loading dataset (This might take a few seconds)...")
# Make sure this matches your downloaded file name exactly!
df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='latin-1')

# 2. Define our Product Features
# We want to predict risk based on how and where we are shipping
features = ['Shipping Mode', 'Order Region', 'Category Name', 'Days for shipment (scheduled)']
target = 'Late_delivery_risk' # In this dataset, 1 = Late, 0 = On Time

# Create a clean dataframe with just what we need
df_clean = df[features + [target]].dropna()

# 3. Clean and Encode the Data
# Machine Learning models can only read numbers, not text like "Air Freight".
# We use LabelEncoders to convert categories into numbers.
print("Encoding categorical data...")
encoders = {}
for col in ['Shipping Mode', 'Order Region', 'Category Name']:
    le = LabelEncoder()
    df_clean[col] = le.fit_transform(df_clean[col])
    encoders[col] = le  # We save these to use in our Streamlit app later

# 4. Split the Data
# We train the model on 80% of the data, and test it on the hidden 20%
X = df_clean[features]
y = df_clean[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train the Random Forest Algorithm
print("Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# 6. Score the Model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Model trained successfully! Accuracy: {accuracy * 100:.2f}%")

# 7. Package the Model for Streamlit (The PM Handoff)
# This saves the trained 'brain' into a file so our app can use it instantly.
with open('rf_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

print("📦 Model saved as 'rf_model.pkl' and 'encoders.pkl'. Ready for integration!")