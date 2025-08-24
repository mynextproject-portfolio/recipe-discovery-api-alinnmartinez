from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from app.models.recipe import Recipe, RecipeCreate
from app.services.recipe_service import RecipeService, get_recipe_service
from app.repositories.recipe_repository import RecipeRepository
from app.dependencies import get_recipe_repository

router = APIRouter(prefix="/recipes", tags=["recipes"])

def get_service(repository: RecipeRepository = Depends(get_recipe_repository)) -> RecipeService:
    """Get recipe service with injected repository"""
    return get_recipe_service(repository)

@router.get("")
def get_recipes(service: RecipeService = Depends(get_service)):
    """Get all recipes"""
    return service.get_all_recipes()

@router.get("/search")
def search_recipes(
    q: Optional[str] = Query(None),
    service: RecipeService = Depends(get_service)
):
    """Search recipes by title"""
    return service.search_recipes(q)

@router.get("/{id}")
def get_recipe(id: int, service: RecipeService = Depends(get_service)):
    """Get a specific recipe by ID"""
    recipe = service.get_recipe_by_id(id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.post("", status_code=201)
def create_recipe(
    recipe: RecipeCreate,
    service: RecipeService = Depends(get_service)
):
    """Create a new recipe"""
    return service.create_recipe(recipe)

@router.put("/{id}")
def update_recipe(
    id: int,
    recipe: RecipeCreate,
    service: RecipeService = Depends(get_service)
):
    """Update an existing recipe"""
    updated_recipe = service.update_recipe(id, recipe)
    if updated_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return updated_recipe

@router.delete("/{id}", status_code=204)
def delete_recipe(id: int, service: RecipeService = Depends(get_service)):
    """Delete a recipe"""
    deleted = service.delete_recipe(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found")