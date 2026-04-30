from pydantic import BaseModel
from typing import Optional


class BrandBase(BaseModel):
    name: str


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: Optional[str] = None


class Brand(BrandBase):
    id: int

    class Config:
        from_attributes = True
