import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.ensemble import RandomForestClassifier
import joblib

# Sample data (in a real application, this would come from a proper dataset)
data = {
    'symptoms': [
        ['fever', 'cough', 'fatigue'],
        ['headache', 'fever', 'body_pain'],
        ['cough', 'sore_throat', 'fatigue'],
        ['nausea', 'dizziness', 'fatigue'],
        ['fever', 'headache', 'body_pain']
    ],
    'disease': [
        'Common Cold',
        'Flu',
        'Common Cold',
        'Vertigo',
        'Flu'
    ],
    'medicines': [
        ['Paracetamol', 'Cough Syrup'],
        ['Ibuprofen', 'Antiviral'],
        ['Paracetamol', 'Cough Syrup'],
        ['Antivert', 'Meclizine'],
        ['Ibuprofen', 'Antiviral']
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert symptoms to binary features
mlb = MultiLabelBinarizer()
symptoms_encoded = mlb.fit_transform(df['symptoms'])

# Split the data
X = symptoms_encoded
y = df['disease']

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save the model and the binarizer
joblib.dump(model, 'models/disease_predictor.pkl')
joblib.dump(mlb, 'models/symptoms_binarizer.pkl')

# Create a mapping of diseases to medicines
disease_medicine_map = dict(zip(df['disease'], df['medicines']))
joblib.dump(disease_medicine_map, 'models/disease_medicine_map.pkl')

print("Model training completed successfully!") 