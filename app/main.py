# app/main.py
from fastapi import FastAPI, HTTPException
from app.models.schemas import UserPreferences, MatchResponse
from app.services.matcher_service import match_pet

app = FastAPI(
    title="Pet Adoption Matcher API",
    description="Find your ideal cat or dog based on personality matching",
    version="1.0.0",
)

@app.post("/match_pet", response_model=MatchResponse)
def match_pet_endpoint(user_input: UserPreferences):
    """
    Takes user questionnaire data and returns the best pet matches.
    
    The user input should include:
    - pet_type: "dog" or "cat"
    - dogs, cats, kids: comfort levels (1-5)
    - energy, affection, training: preference levels (1-5)
    """
    try:
        result = match_pet(user_input.dict())
        return MatchResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Pet Adoption Matcher API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
