from pydantic import BaseModel


# Base model for Brand with only the name field
class BrandBase(BaseModel):
    name: str


# Model for creating a new brand, which includes only the name
class BrandCreate(BrandBase):
    pass


# Model for the response of a brand, which includes both id and name
class BrandResponse(BaseModel):
    id: int
    name: str


# Model for a brand with id, inheriting from BrandBase
class Brand(BrandBase):
    id: int
