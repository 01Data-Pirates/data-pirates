import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def load_data():
    print("Loading preprocessed data...")
    X_train = pd.read_csv('processed_data/X_train.csv')
    X_test = pd.read_csv('processed_data/X_test.csv')
    y_train = pd.read_csv('processed_data/y_train.csv')
    y_test = pd.read_csv('processed_data/y_test.csv')
    
    # Convert y values to 1D array
    y_train = y_train.values.ravel()
    y_test = y_test.values.ravel()
    
    return X_train, X_test, y_train, y_test

def train_and_evaluate_models():
    # Load data
    X_train, X_test, y_train, y_test = load_data()
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Initialize models
    models = {
        'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
        'svm': SVC(kernel='rbf', probability=True, random_state=42)
    }
    
    # Train and evaluate each model
    results = {}
    best_accuracy = 0
    best_model_name = None
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Save results
        results[name] = {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        # Save model
        joblib.dump(model, f'models/{name}_model.joblib')
        
        # Update best model
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model_name = name
        
        print(f"{name} Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(results[name]['classification_report'])
    
    # Save the name of the best model
    with open('models/best_model.txt', 'w') as f:
        f.write(best_model_name)
    
    print(f"\nBest performing model: {best_model_name}")
    print(f"Best accuracy: {best_accuracy*100:.4f}")
    
    return results, best_model_name

if __name__ == "__main__":
    results, best_model = train_and_evaluate_models() 