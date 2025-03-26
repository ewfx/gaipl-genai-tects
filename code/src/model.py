# Description: This file contains the code to train a simple logistic regression model and save it to disk.
# The model is trained on the preprocessed data and saved to disk using joblib.
from sklearn.linear_model import LogisticRegression
import joblib
from .preprocess import load_and_preprocess_data
import os
from sklearn.metrics import accuracy_score

def train_and_save_model():   
    X_train, X_test, y_train, y_test, vectorizer = load_and_preprocess_data("code\data\incidents-generated-data-v3.csv")

    # Train a simple model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate model accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Save the model and vectorizer
    joblib.dump(model, "src/model.pkl")
    joblib.dump(vectorizer, "src/vectorizer.pkl")

    print("Model training completed and saved!")

if __name__ == "__main__":
    train_and_save_model()