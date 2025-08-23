from pydantic import BaseModel
from typing import List

class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[str]
    prepTime: str
    cookTime: str
    difficulty: str
    cuisine: str

class Recipe(BaseModel):
    id: int
    title: str
    ingredients: List[str]
    steps: List[str]
    prepTime: str
    cookTime: str
    difficulty: str
    cuisine: str