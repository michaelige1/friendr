# app/services/matcher_service.py
import pandas as pd
from pathlib import Path
from ml_model import predict_match
from app.utils.data_loader import pet_loader

def match_pet(user_input: dict):
    """
    Match a user with the best pets based on preferences and type.
    user_input must include "pet_type" ("dog" or "cat") and personality features.
    """
    pet_type = user_input.get("pet_type")
    if pet_type not in ["dog", "cat"]:
        raise ValueError("User must specify pet_type as 'dog' or 'cat'")

    # Get pets from the data loader
    pets = pet_loader.get_pets_by_type(pet_type)
    
    # Convert to DataFrame for the ML model
    pet_data = pd.DataFrame(pets)
    
    # Ensure type column is lowercase for consistency
    pet_data['type'] = pet_data['type'].str.lower()

    # Predict matches (returns top 6 matches)
    matches = predict_match(user_input, pet_type, pet_data)

    # Select only fields we want to send back to frontend
    result = []
    for pet in matches:
        # Age is already in years from the data loader
        
        # Boost match percentage by 40% for demo purposes
        boosted_percentage = min(100.0, pet["match_percentage"] + 40.0)
        
        result.append({
            "name": pet["name"],
            "type": pet["type"],
            "age": pet["age"],  # Already in years
            "size": pet["size"],
            "weight": pet["weight"],
            "energy": pet["energy"],
            "affection": pet["affection"],
            "training": pet["training"],
            "new_people": pet["new_people"],
            "match_percentage": round(boosted_percentage, 2),
            "image_url": pet.get("image_url", None),
        })

    return {"matches": result}
