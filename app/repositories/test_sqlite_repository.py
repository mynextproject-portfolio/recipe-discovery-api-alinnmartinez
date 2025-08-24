from .sqlite_repository import SQLiteRecipeRepository

class InMemorySQLiteRecipeRepository(SQLiteRecipeRepository):
    """SQLite repository for testing - uses in-memory database"""
    
    def __init__(self):
        # Use in-memory database for testing
        super().__init__(db_path=":memory:")