# ml_model/predictor.py
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

SAVE_DIR = Path("saved_models")

def load_model(pet_type: str):
    if pet_type == "dog":
        return joblib.load(SAVE_DIR / "kmeans_dog.pkl")
    elif pet_type == "cat":
        return joblib.load(SAVE_DIR / "kmeans_cat.pkl")
    else:
        raise ValueError("pet_type must be 'dog' or 'cat'")

def predict_match(user_input: dict, pet_type: str, pet_data: pd.DataFrame):
    # Load appropriate model + scaler
    (kmeans, scaler) = load_model(pet_type)

    feature_cols = [
        "compatibility_with_cats",
        "compatibility_with_dogs",
        "compatibility_with_people",
        "energy_level",
        "training_willingness",
        "affection_level"
    ]

    # Convert user input into numpy array and scale
    user_vector = np.array([[user_input[col] for col in feature_cols]])
    user_vector_scaled = scaler.transform(user_vector)

    # Predict cluster for user
    cluster = kmeans.predict(user_vector_scaled)[0]

    # Filter pets of that type
    pets = pet_data[pet_data["type"] == pet_type]

    # Scale the pet dataset with the same scaler
    pets_scaled = scaler.transform(pets[feature_cols])

    # Compute similarity (Euclidean distance to user_vector)
    distances = np.linalg.norm(pets_scaled - user_vector_scaled, axis=1)

    # Convert distances to similarity %
    similarities = 100 * (1 - (distances / distances.max()))

    # Attach similarity to pets
    pets = pets.copy()
    pets["match_percentage"] = similarities

    # Return top 5 matches
    top_matches = pets.sort_values("match_percentage", ascending=False).head(5)
    return top_matches.to_dict(orient="records")
