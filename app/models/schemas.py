from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class UserPreferences(BaseModel):
    pet_type: Literal["dog", "cat"] = Field(..., description="Type of pet the user wants to adopt")
    dogs: int = Field(..., ge=1, le=5, description="Comfort level with dogs (1-5)")
    cats: int = Field(..., ge=1, le=5, description="Comfort level with cats (1-5)")
    kids: int = Field(..., ge=1, le=5, description="Comfort level with kids (1-5)")
    energy: int = Field(..., ge=1, le=5, description="Energy level preference (1-5)")
    affection: int = Field(..., ge=1, le=5, description="Affection level preference (1-5)")
    training: int = Field(..., ge=1, le=5, description="Training commitment level (1-5)")

class Pet(BaseModel):
    type: Literal["dog", "cat"]
    name: str
    age: int
    weight: float
    dogs: int  # 1-5 comfort level with dogs
    cats: int  # 1-5 comfort level with cats
    kids: int  # 1-5 comfort level with kids
    energy: int  # 1-5 energy level
    affection: int  # 1-5 affection level
    training: int  # 1-5 training commitment
    match_percentage: Optional[float] = None
    image_url: Optional[str] = None

class PetMatch(BaseModel):
    name: str
    type: Literal["dog", "cat"]
    match_percentage: float
    image_url: Optional[str] = None

class MatchResponse(BaseModel):
    matches: List[PetMatch]
