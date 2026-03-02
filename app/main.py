import json
import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pathlib import Path

from app.db import engine
from app import models
from app.routes import auth as auth_router
from app.routes import jobs as jobs_router
from app.routes import match as match_router
from app.routes import resumes as resumes_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Intelligent Job Recommendation Service",
    description="ML-powered job recommendation system with resume matching",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error for {request.url.path}: {exc.error_count()} errors")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "type": "validation_error"
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception for {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "type": "internal_error"
        },
    )


@app.on_event("startup")
def startup_event():
    """Initialize database and load mock data"""
    logger.info("Application starting up...")
    
    try:
        logger.info("Creating database tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}", exc_info=True)
        raise
    
    try:
        logger.info("Loading mock jobs...")
        path = Path(__file__).parent.parent / "data" / "jobs_mock.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                app.state.jobs = json.load(f)
                logger.info(f"Successfully loaded {len(app.state.jobs)} jobs from {path}")
        else:
            app.state.jobs = []
            logger.warning(f"jobs_mock.json not found at {path}")
    except Exception as e:
        logger.error(f"Failed to load mock jobs: {str(e)}", exc_info=True)
        app.state.jobs = []
    
    logger.info("Application startup complete")


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down...")


@app.get("/health", tags=["health"])
def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Intelligent Job Recommendation Service"
    }


# Include routers
app.include_router(auth_router.router)
app.include_router(jobs_router.router)
app.include_router(match_router.router)
app.include_router(resumes_router.router)

