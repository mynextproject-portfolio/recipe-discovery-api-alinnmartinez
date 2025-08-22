from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic models for request/response
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

# Updated in-memory sample data with all required fields
recipes = [
    {
        "id": 1,
        "title": "Spaghetti Carbonara",
        "ingredients": ["spaghetti", "eggs", "pancetta", "parmesan", "black pepper"],
        "steps": ["Cook pasta", "Fry pancetta", "Mix eggs and cheese", "Combine all with pasta"],
        "prepTime": "10 minutes",
        "cookTime": "15 minutes",
        "difficulty": "Medium",
        "cuisine": "Italian"
    },
    {
        "id": 2,
        "title": "Chicken Tikka Masala",
        "ingredients": ["chicken", "yogurt", "tomato sauce", "spices"],
        "steps": ["Marinate chicken", "Grill chicken", "Simmer in sauce", "Serve with rice"],
        "prepTime": "30 minutes",
        "cookTime": "25 minutes",
        "difficulty": "Hard",
        "cuisine": "Indian"
    },
    {
        "id": 3,
        "title": "Avocado Toast",
        "ingredients": ["bread", "avocado", "lemon", "salt", "pepper"],
        "steps": ["Toast bread", "Mash avocado with lemon, salt, pepper", "Spread and serve"],
        "prepTime": "5 minutes",
        "cookTime": "2 minutes",
        "difficulty": "Easy",
        "cuisine": "American"
    }
]

# Counter for generating IDs
next_id = 4

@app.get("/ping")
async def ping():
    return "pong"

# GET /recipes - return all recipes
@app.get("/recipes")
def get_recipes():
    return recipes

# GET /recipes/search - search recipes by title
@app.get("/recipes/search")
def search_recipes(q: Optional[str] = Query(None)):
    if not q:
        return []
    
    query_lower = q.lower()
    matching_recipes = []
    
    for recipe in recipes:
        if query_lower in recipe["title"].lower():
            matching_recipes.append(recipe)
    
    return matching_recipes

# GET /recipes/{id} - return a specific recipe by id
@app.get("/recipes/{id}")
def get_recipe(id: int):
    for recipe in recipes:
        if recipe["id"] == id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

# POST /recipes - create a new recipe
@app.post("/recipes", status_code=201)
def create_recipe(recipe: RecipeCreate):
    global next_id
    new_recipe = {
        "id": next_id,
        **recipe.model_dump()
    }
    recipes.append(new_recipe)
    next_id += 1
    return new_recipe

# PUT /recipes/{id} - update an existing recipe
@app.put("/recipes/{id}")
def update_recipe(id: int, recipe: RecipeCreate):
    for i, existing_recipe in enumerate(recipes):
        if existing_recipe["id"] == id:
            updated_recipe = {
                "id": id,
                **recipe.model_dump()
            }
            recipes[i] = updated_recipe
            return updated_recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

# DELETE /recipes/{id} - delete a recipe
@app.delete("/recipes/{id}", status_code=204)
def delete_recipe(id: int):
    for i, recipe in enumerate(recipes):
        if recipe["id"] == id:
            recipes.pop(i)
            return
    raise HTTPException(status_code=404, detail="Recipe not found")