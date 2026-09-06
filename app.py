import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger_config import setup_logging
from api import router

# Initialize logging
setup_logging(app_name="nutrition_coach", level=logging.INFO)
logger = logging.getLogger(__name__)
def create_app() -> FastAPI:
    """Define the FastAPI application."""
    logger.info("Initializing FastAPI application")
    app = FastAPI(title="AI Nutrition Coach", version="1.0.0", description="An AI-powered nutrition coaching application.")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router.router, tags=["Chat"])
    logger.info("FastAPI application initialized successfully")
    return app

app = create_app()