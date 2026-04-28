from pydantic import BaseModel
from typing import Optional, List

class BrandBase(BaseModel):
    name: str

class Brand(BrandBase):
    id: int

class SneakerBase(BaseModel):
    name: str
    brand_id: int
    product_link: Optional[str] = None
    categories: Optional[str] = None
    price: Optional[float] = None
    release_year: Optional[int] = None
    colorway: Optional[str] = None

class Sneaker(SneakerBase):
    id: int

class SneakerWithBrand(Sneaker):
    brand: Brand
