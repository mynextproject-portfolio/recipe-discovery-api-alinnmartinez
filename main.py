from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory sample data
recipes = [
    {
        "id": 1,
        "title": "Spaghetti Carbonara",
        "ingredients": ["spaghetti", "eggs", "pancetta", "parmesan", "black pepper"],
        "instructions": "Cook pasta. Fry pancetta. Mix eggs and cheese. Combine all with pasta."
    },
    {
        "id": 2,
        "title": "Chicken Tikka Masala",
        "ingredients": ["chicken", "yogurt", "tomato sauce", "spices"],
        "instructions": "Marinate chicken. Grill. Simmer in sauce. Serve with rice."
    },
    {
        "id": 3,
        "title": "Avocado Toast",
        "ingredients": ["bread", "avocado", "lemon", "salt", "pepper"],
        "instructions": "Toast bread. Mash avocado with lemon, salt, pepper. Spread and serve."
    }
]

@app.get("/ping")
async def ping():
    return "pong"

# GET /recipes - return all recipes
@app.get("/recipes")
def get_recipes():
    return recipes

# GET /recipes/{id} - return a specific recipe by id
@app.get("/recipes/{id}")
def get_recipe(id: int):
    for recipe in recipes:
        if recipe["id"] == id:
            return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")