# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from app.models.schemas import UserPreferences, MatchResponse
from app.services.matcher_service import match_pet

app = FastAPI(
    title="Pet Adoption Matcher API",
    description="Find your ideal cat or dog based on personality matching",
    version="1.0.0",
)

# Mount static files for images
app.mount("/images", StaticFiles(directory="data/images"), name="images")

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

@app.get("/image/{pet_type}/{filename}")
def get_pet_image(pet_type: str, filename: str):
    """
    Serve pet images from the local data/images directory.
    """
    # Validate pet type
    if pet_type not in ["dog", "cat"]:
        raise HTTPException(status_code=400, detail="pet_type must be 'dog' or 'cat'")
    
    # Construct file path
    image_path = Path(f"data/images/{pet_type}s/{filename}")
    
    # Check if file exists
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Return the image file
    return FileResponse(image_path)
