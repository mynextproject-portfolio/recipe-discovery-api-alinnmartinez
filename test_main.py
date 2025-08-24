import pytest
from fastapi.testclient import TestClient
from main import app
from app.dependencies import get_recipe_repository, reset_recipe_repository
from app.repositories.recipe_repository import MemoryRecipeRepository

# Test data for creating recipes
sample_recipe = {
    "title": "Test Recipe",
    "ingredients": ["ingredient1", "ingredient2"],
    "steps": ["step1", "step2", "step3"],
    "prepTime": "15 minutes",
    "cookTime": "30 minutes",
    "difficulty": "Easy",
    "cuisine": "Test"
}

updated_recipe = {
    "title": "Updated Test Recipe",
    "ingredients": ["updated ingredient1", "updated ingredient2"],
    "steps": ["updated step1", "updated step2"],
    "prepTime": "20 minutes",
    "cookTime": "25 minutes",
    "difficulty": "Medium",
    "cuisine": "Updated Test"
}

@pytest.fixture
def client():
    """Create a test client with dependency override"""
    # Create a shared test repository instance
    test_repository = MemoryRecipeRepository()
    
    # Override the dependency to use the same repository for all operations
    def get_test_repository():
        return test_repository
    
    app.dependency_overrides[get_recipe_repository] = get_test_repository
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides.clear()

def test_ping(client):
    """Test the ping endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"

def test_get_all_recipes(client):
    """Test getting all recipes"""
    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert isinstance(recipes, list)
    assert len(recipes) >= 3  # We have 3 sample recipes
    
    # Verify recipe structure
    for recipe in recipes:
        assert "id" in recipe
        assert "title" in recipe
        assert "ingredients" in recipe
        assert "steps" in recipe
        assert "prepTime" in recipe
        assert "cookTime" in recipe
        assert "difficulty" in recipe
        assert "cuisine" in recipe

def test_get_recipe_by_id(client):
    """Test getting a specific recipe by ID"""
    # Test existing recipe
    response = client.get("/recipes/1")
    assert response.status_code == 200
    recipe = response.json()
    assert recipe["id"] == 1
    assert recipe["title"] == "Spaghetti Carbonara"
    
    # Test non-existing recipe
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"

def test_create_recipe(client):
    """Test creating a new recipe"""
    response = client.post("/recipes", json=sample_recipe)
    assert response.status_code == 201
    
    created_recipe = response.json()
    assert created_recipe["title"] == sample_recipe["title"]
    assert created_recipe["ingredients"] == sample_recipe["ingredients"]
    assert created_recipe["steps"] == sample_recipe["steps"]
    assert created_recipe["prepTime"] == sample_recipe["prepTime"]
    assert created_recipe["cookTime"] == sample_recipe["cookTime"]
    assert created_recipe["difficulty"] == sample_recipe["difficulty"]
    assert created_recipe["cuisine"] == sample_recipe["cuisine"]
    assert "id" in created_recipe
    assert created_recipe["id"] > 0

def test_update_recipe(client):
    """Test updating an existing recipe"""
    # First create a recipe
    create_response = client.post("/recipes", json=sample_recipe)
    assert create_response.status_code == 201
    created_recipe = create_response.json()
    recipe_id = created_recipe["id"]
    
    # Update the recipe
    response = client.put(f"/recipes/{recipe_id}", json=updated_recipe)
    assert response.status_code == 200
    
    updated = response.json()
    assert updated["id"] == recipe_id
    assert updated["title"] == updated_recipe["title"]
    assert updated["ingredients"] == updated_recipe["ingredients"]
    assert updated["steps"] == updated_recipe["steps"]
    assert updated["prepTime"] == updated_recipe["prepTime"]
    assert updated["cookTime"] == updated_recipe["cookTime"]
    assert updated["difficulty"] == updated_recipe["difficulty"]
    assert updated["cuisine"] == updated_recipe["cuisine"]

def test_update_nonexistent_recipe(client):
    """Test updating a recipe that doesn't exist"""
    response = client.put("/recipes/999", json=updated_recipe)
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"

def test_delete_recipe(client):
    """Test deleting a recipe"""
    # First create a recipe
    create_response = client.post("/recipes", json=sample_recipe)
    assert create_response.status_code == 201
    created_recipe = create_response.json()
    recipe_id = created_recipe["id"]
    
    # Delete the recipe
    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204
    
    # Verify it's deleted by trying to get it
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_recipe(client):
    """Test deleting a recipe that doesn't exist"""
    response = client.delete("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"

def test_search_recipes_with_query(client):
    """Test searching recipes with various queries"""
    # Search for existing recipe
    response = client.get("/recipes/search?q=chicken")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert "Chicken" in results[0]["title"]
    
    # Case insensitive search
    response = client.get("/recipes/search?q=CHICKEN")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert "Chicken" in results[0]["title"]
    
    # Search for partial match
    response = client.get("/recipes/search?q=spagh")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert "Spaghetti" in results[0]["title"]
    
    # Search with no matches
    response = client.get("/recipes/search?q=pizza")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0

def test_search_recipes_no_query(client):
    """Test searching recipes without query parameter"""
    response = client.get("/recipes/search")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0

def test_search_recipes_empty_query(client):
    """Test searching recipes with empty query"""
    response = client.get("/recipes/search?q=")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 0

def test_happy_path_crud_and_search(client):
    """Test complete CRUD + search cycle end-to-end"""
    # 1. Create a recipe
    create_response = client.post("/recipes", json=sample_recipe)
    assert create_response.status_code == 201
    created_recipe = create_response.json()
    recipe_id = created_recipe["id"]
    
    # 2. Get the created recipe
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 200
    retrieved_recipe = get_response.json()
    assert retrieved_recipe["id"] == recipe_id
    assert retrieved_recipe["title"] == sample_recipe["title"]
    
    # 3. Search for the recipe
    search_response = client.get(f"/recipes/search?q={sample_recipe['title']}")
    assert search_response.status_code == 200
    search_results = search_response.json()
    assert len(search_results) >= 1
    found_recipe = next(r for r in search_results if r["id"] == recipe_id)
    assert found_recipe["title"] == sample_recipe["title"]
    
    # 4. Update the recipe
    update_response = client.put(f"/recipes/{recipe_id}", json=updated_recipe)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["id"] == recipe_id
    assert updated["title"] == updated_recipe["title"]
    
    # 5. Verify the update by getting the recipe again
    verify_response = client.get(f"/recipes/{recipe_id}")
    assert verify_response.status_code == 200
    verified_recipe = verify_response.json()
    assert verified_recipe["title"] == updated_recipe["title"]
    assert verified_recipe["ingredients"] == updated_recipe["ingredients"]
    
    # 6. Search for the updated recipe
    updated_search_response = client.get(f"/recipes/search?q={updated_recipe['title']}")
    assert updated_search_response.status_code == 200
    updated_search_results = updated_search_response.json()
    found_updated = next(r for r in updated_search_results if r["id"] == recipe_id)
    assert found_updated["title"] == updated_recipe["title"]
    
    # 7. Clean up - delete the recipe
    delete_response = client.delete(f"/recipes/{recipe_id}")
    assert delete_response.status_code == 204
    
    # 8. Verify deletion
    final_get_response = client.get(f"/recipes/{recipe_id}")
    assert final_get_response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__])