from pydantic import BaseModel
from typing import List, Optional


# Base model for Sneaker with relevant fields
class SneakerBase(BaseModel):
    name: str
    brand_id: int
    product_link: str
    categories: List[str]  # List of category names (e.g., Running, Basketball, Lifestyle)
    price: Optional[float] = None
    release_year: Optional[int] = None
    colorway: Optional[str] = None


# Model for creating a new sneaker
class SneakerCreate(SneakerBase):
    pass


# Model for the response of a sneaker, which includes both id and all fields
class SneakerResponse(SneakerBase):
    id: int


# Model for a sneaker with id, inheriting from SneakerBase
class Sneaker(SneakerBase):
    id: int
