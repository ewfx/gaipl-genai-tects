import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
#print(sys.path)

import joblib
import os
from Platform.prediction_model.model import train_and_save_model
from Platform.prediction_model.transform_debugging_steps import format_debugging_steps
from Platform.prediction_model.structure_debugging_steps import format_debugging_steps_with_llm


# Get the base directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# File paths
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

# Check if model exists, else train it
if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    print("Model not found! Training a new model...")
    train_and_save_model()  # Calls the train function from model.py

# Load Model & Vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_debugging_step(incident_description):
    """
    Predicts the debugging step for a given incident description.
    """
    # Transform the input description
    description_tfidf = vectorizer.transform([incident_description])

    # Predict the debugging step
    prediction = model.predict(description_tfidf)

    # Format the debugging steps using the LLM
    formatted_steps = format_debugging_steps_with_llm(prediction[0])

    return formatted_steps  # Get the formatted predicted steps


if __name__ == "__main__":
    # Example test case
    sample_description = "Cloud backup failure"
    predicted_step = predict_debugging_step(sample_description)
    print(f"Predicted Debugging Step: {predicted_step}")
