from app.repositories.recipe_repository import RecipeRepository, MemoryRecipeRepository

# Create a global instance that will be shared across requests
_recipe_repository_instance = None

def get_recipe_repository() -> RecipeRepository:
    """Dependency provider for recipe repository"""
    global _recipe_repository_instance
    if _recipe_repository_instance is None:
        _recipe_repository_instance = MemoryRecipeRepository()
    return _recipe_repository_instance

def reset_recipe_repository():
    """Reset the repository instance - useful for testing"""
    global _recipe_repository_instance
    _recipe_repository_instance = None