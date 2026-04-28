from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import brands_router, sneakers_router

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="Sneaker Management API",
    description="A complete REST API for managing sneakers and brands",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(brands_router)
app.include_router(sneakers_router)


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sneaker Management API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
