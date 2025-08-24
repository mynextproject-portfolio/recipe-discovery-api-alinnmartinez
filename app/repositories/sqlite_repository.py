import sqlite3
import json
from typing import List, Dict, Optional
from .recipe_repository import RecipeRepository

class SQLiteRecipeRepository(RecipeRepository):
    """SQLite implementation of recipe repository"""
    
    def __init__(self, db_path: str = "recipes.db"):
        self.db_path = db_path
        self.connection = None
        if db_path == ":memory:":
            # For in-memory databases, keep a persistent connection
            self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self._init_database()
        self._seed_initial_data()
    
    def _get_connection(self):
        """Get database connection"""
        if self.connection:
            return self.connection
        return sqlite3.connect(self.db_path)
    
    def _init_database(self):
        """Initialize the database and create tables"""
        if self.connection:
            # For in-memory databases
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    ingredients TEXT NOT NULL,
                    steps TEXT NOT NULL,
                    prep_time TEXT NOT NULL,
                    cook_time TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    cuisine TEXT NOT NULL
                )
            """)
            self.connection.commit()
        else:
            # For file databases
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS recipes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        ingredients TEXT NOT NULL,
                        steps TEXT NOT NULL,
                        prep_time TEXT NOT NULL,
                        cook_time TEXT NOT NULL,
                        difficulty TEXT NOT NULL,
                        cuisine TEXT NOT NULL
                    )
                """)
                conn.commit()
    
    def _seed_initial_data(self):
        """Add initial sample data if database is empty"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM recipes")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert sample data
            sample_recipes = [
                (
                    "Spaghetti Carbonara",
                    json.dumps(["spaghetti", "eggs", "pancetta", "parmesan", "black pepper"]),
                    json.dumps(["Cook pasta", "Fry pancetta", "Mix eggs and cheese", "Combine all with pasta"]),
                    "10 minutes",
                    "15 minutes",
                    "Medium",
                    "Italian"
                ),
                (
                    "Chicken Tikka Masala",
                    json.dumps(["chicken", "yogurt", "tomato sauce", "spices"]),
                    json.dumps(["Marinate chicken", "Grill chicken", "Simmer in sauce", "Serve with rice"]),
                    "30 minutes",
                    "25 minutes",
                    "Hard",
                    "Indian"
                ),
                (
                    "Avocado Toast",
                    json.dumps(["bread", "avocado", "lemon", "salt", "pepper"]),
                    json.dumps(["Toast bread", "Mash avocado with lemon, salt, pepper", "Spread and serve"]),
                    "5 minutes",
                    "2 minutes",
                    "Easy",
                    "American"
                )
            ]
            
            cursor.executemany("""
                INSERT INTO recipes (title, ingredients, steps, prep_time, cook_time, difficulty, cuisine)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, sample_recipes)
            
            if self.connection:
                self.connection.commit()
            else:
                conn.commit()
        
        if not self.connection:
            conn.close()
    
    def _row_to_dict(self, row) -> Dict:
        """Convert database row to dictionary"""
        return {
            "id": row[0],
            "title": row[1],
            "ingredients": json.loads(row[2]),
            "steps": json.loads(row[3]),
            "prepTime": row[4],
            "cookTime": row[5],
            "difficulty": row[6],
            "cuisine": row[7]
        }
    
    def get_all_recipes(self) -> List[Dict]:
        """Get all recipes from database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes")
        rows = cursor.fetchall()
        
        if not self.connection:
            conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def get_recipe_by_id(self, recipe_id: int) -> Optional[Dict]:
        """Get a specific recipe by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        row = cursor.fetchone()
        
        if not self.connection:
            conn.close()
        
        return self._row_to_dict(row) if row else None
    
    def create_recipe(self, recipe_data: Dict) -> Dict:
        """Create a new recipe"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO recipes (title, ingredients, steps, prep_time, cook_time, difficulty, cuisine)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            recipe_data["title"],
            json.dumps(recipe_data["ingredients"]),
            json.dumps(recipe_data["steps"]),
            recipe_data["prepTime"],
            recipe_data["cookTime"],
            recipe_data["difficulty"],
            recipe_data["cuisine"]
        ))
        recipe_id = cursor.lastrowid
        
        if self.connection:
            self.connection.commit()
        else:
            conn.commit()
            conn.close()
        
        # Return the created recipe
        return self.get_recipe_by_id(recipe_id)
    
    def update_recipe(self, recipe_id: int, recipe_data: Dict) -> Optional[Dict]:
        """Update an existing recipe"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE recipes 
            SET title = ?, ingredients = ?, steps = ?, prep_time = ?, cook_time = ?, difficulty = ?, cuisine = ?
            WHERE id = ?
        """, (
            recipe_data["title"],
            json.dumps(recipe_data["ingredients"]),
            json.dumps(recipe_data["steps"]),
            recipe_data["prepTime"],
            recipe_data["cookTime"],
            recipe_data["difficulty"],
            recipe_data["cuisine"],
            recipe_id
        ))
        
        if cursor.rowcount == 0:
            if not self.connection:
                conn.close()
            return None
        
        if self.connection:
            self.connection.commit()
        else:
            conn.commit()
            conn.close()
            
        return self.get_recipe_by_id(recipe_id)
    
    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        deleted = cursor.rowcount > 0
        
        if self.connection:
            self.connection.commit()
        else:
            conn.commit()
            conn.close()
            
        return deleted
    
    def search_recipes(self, query: str) -> List[Dict]:
        """Search recipes by title"""
        if not query:
            return []
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM recipes WHERE title LIKE ?",
            (f"%{query}%",)
        )
        rows = cursor.fetchall()
        
        if not self.connection:
            conn.close()
        
        return [self._row_to_dict(row) for row in rows]
    
    def __del__(self):
        """Close connection when object is destroyed"""
        if self.connection:
            self.connection.close()