from typing import List, Optional
from app.models.recipe import Recipe, RecipeCreate
from app.repositories.recipe_repository import RecipeRepository

class RecipeService:
    def __init__(self, repository: RecipeRepository):
        self.repository = repository
    
    def get_all_recipes(self) -> List[dict]:
        return self.repository.get_all_recipes()
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[dict]:
        return self.repository.get_recipe_by_id(recipe_id)
    
    def create_recipe(self, recipe: RecipeCreate) -> dict:
        recipe_data = recipe.model_dump()
        return self.repository.create_recipe(recipe_data)
    
    def update_recipe(self, recipe_id: int, recipe: RecipeCreate) -> Optional[dict]:
        recipe_data = recipe.model_dump()
        return self.repository.update_recipe(recipe_id, recipe_data)
    
    def delete_recipe(self, recipe_id: int) -> bool:
        return self.repository.delete_recipe(recipe_id)
    
    def search_recipes(self, query: Optional[str]) -> List[dict]:
        if not query:
            return []
        return self.repository.search_recipes(query)

def get_recipe_service(repository: RecipeRepository) -> RecipeService:
    """Factory function for recipe service"""
    return RecipeService(repository)