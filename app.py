from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
def create_app() -> FastAPI:
    """Define the FastAPI application."""
    app = FastAPI(name="AI Nutrition Coach", version="1.0.0", description="An AI-powered nutrition coaching application.")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router.router, tags=["Chat"])
    return app

app =  create_app()