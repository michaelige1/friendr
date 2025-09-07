# app/main.py
from fastapi import FastAPI, HTTPException
from app.models.schemas import UserPreferences, Pet
from app.services.matcher_service import match_pet

app = FastAPI(
    title="Pet Adoption Matcher API",
    description="Find your ideal cat or dog based on personality matching",
    version="1.0.0",
)

@app.post("/match_pet")
def match_pet_endpoint(user_input: UserPreferences):
    """
    Takes user questionnaire data and returns the best pet matches.
    """
    try:
        result = match_pet(user_input.dict())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
