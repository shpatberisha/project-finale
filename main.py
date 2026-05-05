from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import brands, sneakers, api_key, auth
from database import create_database

# Initialize FastAPI app
app = FastAPI(
    title="Nike Sneakers Management System",
    description="An API for managing Nike sneakers, brands, and categories with user authentication.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(brands.router, prefix="/api/brands", tags=["Brands"])
app.include_router(sneakers.router, prefix="/api/sneakers", tags=["Sneakers"])
app.include_router(api_key.router, prefix="/api/validate_key")


@app.on_event("startup")
def startup():
    # Initialize the database tables
    create_database()
