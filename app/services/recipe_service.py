from typing import List, Optional
from app.models.recipe import Recipe, RecipeCreate
from app.storage.memory_storage import storage

class RecipeService:
    def __init__(self):
        self.storage = storage
    
    def get_all_recipes(self) -> List[dict]:
        return self.storage.get_all_recipes()
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[dict]:
        return self.storage.get_recipe_by_id(recipe_id)
    
    def create_recipe(self, recipe: RecipeCreate) -> dict:
        recipe_data = recipe.model_dump()
        return self.storage.create_recipe(recipe_data)
    
    def update_recipe(self, recipe_id: int, recipe: RecipeCreate) -> Optional[dict]:
        recipe_data = recipe.model_dump()
        return self.storage.update_recipe(recipe_id, recipe_data)
    
    def delete_recipe(self, recipe_id: int) -> bool:
        return self.storage.delete_recipe(recipe_id)
    
    def search_recipes(self, query: Optional[str]) -> List[dict]:
        if not query:
            return []
        return self.storage.search_recipes(query)

# Create a global instance
recipe_service = RecipeService()