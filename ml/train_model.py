import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
import joblib
import os

def train_models(data_path='data/student_data.csv', model_dir='ml/models'):
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}. Please run generate_data.py first.")
        return
        
    df = pd.read_csv(data_path)
    
    # Features
    X = df[['attendance_percentage', 'assignments_completed', 'quiz_average', 'previous_term_marks']]
    
    # Target 1: Continuous Marks (Regression)
    y_reg = df['final_exam_marks']
    
    # Target 2: Categories (Classification)
    y_clf = df['performance_category']
    
    # Split data
    X_train, X_test, y_reg_train, y_reg_test, y_clf_train, y_clf_test = train_test_split(
        X, y_reg, y_clf, test_size=0.2, random_state=42
    )
    
    # Train Regressor
    regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    regressor.fit(X_train, y_reg_train)
    reg_preds = regressor.predict(X_test)
    mse = mean_squared_error(y_reg_test, reg_preds)
    print(f"Regressor MSE: {mse:.2f}")
    
    # Train Classifier
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X_train, y_clf_train)
    clf_preds = classifier.predict(X_test)
    acc = accuracy_score(y_clf_test, clf_preds)
    print(f"Classifier Accuracy: {acc:.2f}")
    
    # Save models
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(regressor, os.path.join(model_dir, 'marks_predictor.pkl'))
    joblib.dump(classifier, os.path.join(model_dir, 'category_predictor.pkl'))
    print(f"Models saved to {model_dir}")

if __name__ == '__main__':
    train_models()
