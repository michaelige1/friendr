# app/services/matcher_service.py
import pandas as pd
from pathlib import Path
from ml_model import predict_match

DATA_PATH = Path("data/pet_data.csv")

def match_pet(user_input: dict):
    """
    Match a user with the best pets based on preferences and type.
    user_input must include "type" ("dog" or "cat") and personality features.
    """
    pet_type = user_input.get("type")
    if pet_type not in ["dog", "cat"]:
        raise ValueError("User must specify pet type as 'dog' or 'cat'")

    # Load dataset
    pet_data = pd.read_csv(DATA_PATH)

    # Predict matches
    matches = predict_match(user_input, pet_type, pet_data)

    # Select only fields we want to send back to frontend
    result = [
        {
            "id": pet["id"],
            "name": pet["name"],
            "type": pet["type"],
            "match_percentage": pet["match_percentage"],
            "image_url": pet.get("image_url", None),
        }
        for pet in matches
    ]

    return {"matches": result}
