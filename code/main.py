import joblib
from src.model import train_and_save_model
import os

# File paths
MODEL_PATH = "src/model.pkl"
VECTORIZER_PATH = "src/vectorizer.pkl"

print(os.path.dirname(os.path.abspath(__file__)))

# Check if model exists, else train it
if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    print("Model not found! Training a new model...")
    train_and_save_model()  # Calls the train function from model.py

# Load Model & Vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_debugging_step(incident_description):
    # Load the trained model and vectorizer
    #model = joblib.load("src/model.pkl")
    #vectorizer = joblib.load("src/vectorizer.pkl")

    # Transform the input description
    description_tfidf = vectorizer.transform([incident_description])

    # Predict the debugging step
    prediction = model.predict(description_tfidf)

    return prediction[0]  # Get the first (and only) predicted step

if __name__ == "__main__":
    # Example test case
    sample_description = "Salesforce connection failure"
    predicted_step = predict_debugging_step(sample_description)
    print(f"Predicted Debugging Step: {predicted_step}")
