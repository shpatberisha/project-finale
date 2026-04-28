# Routers package
from .brands import router as brands_router
from .sneakers import router as sneakers_router

__all__ = ["brands_router", "sneakers_router"]
