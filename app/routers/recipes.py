from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.recipe import Recipe, RecipeCreate
from app.services.recipe_service import recipe_service

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("")
def get_recipes():
    """Get all recipes"""
    return recipe_service.get_all_recipes()

@router.get("/search")
def search_recipes(q: Optional[str] = Query(None)):
    """Search recipes by title"""
    return recipe_service.search_recipes(q)

@router.get("/{id}")
def get_recipe(id: int):
    """Get a specific recipe by ID"""
    recipe = recipe_service.get_recipe_by_id(id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.post("", status_code=201)
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe"""
    return recipe_service.create_recipe(recipe)

@router.put("/{id}")
def update_recipe(id: int, recipe: RecipeCreate):
    """Update an existing recipe"""
    updated_recipe = recipe_service.update_recipe(id, recipe)
    if updated_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@router.delete("/{id}", status_code=204)
def delete_recipe(id: int):
    """Delete a recipe"""
    deleted = recipe_service.delete_recipe(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")