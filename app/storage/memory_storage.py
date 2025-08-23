from typing import List, Dict, Optional

class MemoryStorage:
    def __init__(self):
        self.recipes = [
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
        self.next_id = 4
    
    def get_all_recipes(self) -> List[Dict]:
        return self.recipes.copy()
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict]:
        for recipe in self.recipes:
            if recipe["id"] == recipe_id:
                return recipe.copy()
        return None
    
    def create_recipe(self, recipe_data: Dict) -> Dict:
        new_recipe = {
            "id": self.next_id,
            **recipe_data
        }
        self.recipes.append(new_recipe)
        self.next_id += 1
        return new_recipe.copy()
    
    def update_recipe(self, recipe_id: int, recipe_data: Dict) -> Optional[Dict]:
        for i, recipe in enumerate(self.recipes):
            if recipe["id"] == recipe_id:
                updated_recipe = {
                    "id": recipe_id,
                    **recipe_data
                }
                self.recipes[i] = updated_recipe
                return updated_recipe.copy()
        return None
    
    def delete_recipe(self, recipe_id: int) -> bool:
        for i, recipe in enumerate(self.recipes):
            if recipe["id"] == recipe_id:
                self.recipes.pop(i)
                return True
        return False
    
    def search_recipes(self, query: str) -> List[Dict]:
        if not query:
            return []
        
        query_lower = query.lower()
        matching_recipes = []
        
        for recipe in self.recipes:
            if query_lower in recipe["title"].lower():
                matching_recipes.append(recipe.copy())
        
        return matching_recipes

# Create a global instance
storage = MemoryStorage()