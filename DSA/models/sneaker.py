from pydantic import BaseModel
from typing import Optional


class SneakerBase(BaseModel):
    name: str
    brand_id: int
    product_link: str
    categories: str
    price: float
    release_year: int
    colorway: str


class SneakerCreate(SneakerBase):
    pass


class SneakerUpdate(BaseModel):
    name: Optional[str] = None
    brand_id: Optional[int] = None
    product_link: Optional[str] = None
    categories: Optional[str] = None
    price: Optional[float] = None
    release_year: Optional[int] = None
    colorway: Optional[str] = None


class Sneaker(SneakerBase):
    id: int

    class Config:
        from_attributes = True
