from fastapi import FastAPI
from app.routers import health, recipes

def create_app() -> FastAPI:
    app = FastAPI(
        title="Recipe Discovery API",
        description="A simple API for managing recipes",
        version="1.0.0"
    )
    
    # Include routers
    app.include_router(health.router)
    app.include_router(recipes.router)
    
    return app

app = create_app()