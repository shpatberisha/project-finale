from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database import get_db
from models import Brand, BrandCreate, BrandUpdate
from auth import verify_api_key

router = APIRouter(prefix="/api/brands", tags=["brands"])


@router.get("/", response_model=List[Brand])
def list_brands(db=Depends(get_db)):
    """Get all brands"""
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM brands ORDER BY name")
    brands = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return brands


@router.get("/{brand_id}", response_model=Brand)
def get_brand(brand_id: int, db=Depends(get_db)):
    """Get a specific brand by ID"""
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM brands WHERE id = ?", (brand_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"id": row[0], "name": row[1]}


@router.post("/", response_model=Brand)
def create_brand(brand: BrandCreate, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Create a new brand (requires API key)"""
    cursor = db.cursor()
    cursor.execute("INSERT INTO brands (name) VALUES (?)", (brand.name,))
    db.commit()
    brand_id = cursor.lastrowid
    return {"id": brand_id, "name": brand.name}


@router.put("/{brand_id}", response_model=Brand)
def update_brand(brand_id: int, brand: BrandUpdate, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Update a brand (requires API key)"""
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM brands WHERE id = ?", (brand_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    name = brand.name if brand.name else existing[1]
    cursor.execute("UPDATE brands SET name = ? WHERE id = ?", (name, brand_id))
    db.commit()
    return {"id": brand_id, "name": name}


@router.delete("/{brand_id}")
def delete_brand(brand_id: int, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Delete a brand (requires API key)"""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM brands WHERE id = ?", (brand_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Brand not found")
    
    cursor.execute("DELETE FROM brands WHERE id = ?", (brand_id,))
    db.commit()
    return {"message": "Brand deleted successfully"}
