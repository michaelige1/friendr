from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class UserPreferences(BaseModel):
    compatibility_with_cats: int
    compatibility_with_dogs: int
    compatibility_with_people: int
    energy_level: int
    training_willingness: int
    affection_level: int

class Pet(BaseModel):
    type: Literal["dog", "cat"]
    name: str
    age: int
    weight: float
    dogs: int # 1-5 comfort level with dogs
    cats: int # 1-5 comfort level with cats
    kids: int # 1-5 comfort level with kids
    energy: int # 1-5 energy level
    affection: int # 1-5 affection level
    training: int # 1-5 training commitment
    image_url: str | None = None  # optional, if images are stored
