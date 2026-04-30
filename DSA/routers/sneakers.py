from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database import get_db
from models import Sneaker, SneakerCreate, SneakerUpdate
from auth import verify_api_key

router = APIRouter(prefix="/api/sneakers", tags=["sneakers"])


@router.get("/", response_model=List[Sneaker])
def list_sneakers(db=Depends(get_db)):
    """Get all sneakers"""
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, brand_id, product_link, categories, price, release_year, colorway 
        FROM sneakers ORDER BY name
    """)
    sneakers = [
        {
            "id": row[0],
            "name": row[1],
            "brand_id": row[2],
            "product_link": row[3],
            "categories": row[4],
            "price": row[5],
            "release_year": row[6],
            "colorway": row[7]
        }
        for row in cursor.fetchall()
    ]
    return sneakers


@router.get("/{sneaker_id}", response_model=Sneaker)
def get_sneaker(sneaker_id: int, db=Depends(get_db)):
    """Get a specific sneaker by ID"""
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, brand_id, product_link, categories, price, release_year, colorway 
        FROM sneakers WHERE id = ?
    """, (sneaker_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Sneaker not found")
    return {
        "id": row[0],
        "name": row[1],
        "brand_id": row[2],
        "product_link": row[3],
        "categories": row[4],
        "price": row[5],
        "release_year": row[6],
        "colorway": row[7]
    }


@router.get("/brand/{brand_id}", response_model=List[Sneaker])
def get_sneakers_by_brand(brand_id: int, db=Depends(get_db)):
    """Get all sneakers by brand ID"""
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, brand_id, product_link, categories, price, release_year, colorway 
        FROM sneakers WHERE brand_id = ? ORDER BY name
    """, (brand_id,))
    sneakers = [
        {
            "id": row[0],
            "name": row[1],
            "brand_id": row[2],
            "product_link": row[3],
            "categories": row[4],
            "price": row[5],
            "release_year": row[6],
            "colorway": row[7]
        }
        for row in cursor.fetchall()
    ]
    return sneakers


@router.post("/", response_model=Sneaker)
def create_sneaker(sneaker: SneakerCreate, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Create a new sneaker (requires API key)"""
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO sneakers (name, brand_id, product_link, categories, price, release_year, colorway)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (sneaker.name, sneaker.brand_id, sneaker.product_link, sneaker.categories, 
          sneaker.price, sneaker.release_year, sneaker.colorway))
    db.commit()
    sneaker_id = cursor.lastrowid
    return {
        "id": sneaker_id,
        "name": sneaker.name,
        "brand_id": sneaker.brand_id,
        "product_link": sneaker.product_link,
        "categories": sneaker.categories,
        "price": sneaker.price,
        "release_year": sneaker.release_year,
        "colorway": sneaker.colorway
    }


@router.put("/{sneaker_id}", response_model=Sneaker)
def update_sneaker(sneaker_id: int, sneaker: SneakerUpdate, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Update a sneaker (requires API key)"""
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, name, brand_id, product_link, categories, price, release_year, colorway 
        FROM sneakers WHERE id = ?
    """, (sneaker_id,))
    existing = cursor.fetchone()
    if not existing:
        raise HTTPException(status_code=404, detail="Sneaker not found")
    
    name = sneaker.name if sneaker.name else existing[1]
    brand_id = sneaker.brand_id if sneaker.brand_id else existing[2]
    product_link = sneaker.product_link if sneaker.product_link else existing[3]
    categories = sneaker.categories if sneaker.categories else existing[4]
    price = sneaker.price if sneaker.price else existing[5]
    release_year = sneaker.release_year if sneaker.release_year else existing[6]
    colorway = sneaker.colorway if sneaker.colorway else existing[7]
    
    cursor.execute("""
        UPDATE sneakers SET name = ?, brand_id = ?, product_link = ?, categories = ?, 
                          price = ?, release_year = ?, colorway = ? WHERE id = ?
    """, (name, brand_id, product_link, categories, price, release_year, colorway, sneaker_id))
    db.commit()
    
    return {
        "id": sneaker_id,
        "name": name,
        "brand_id": brand_id,
        "product_link": product_link,
        "categories": categories,
        "price": price,
        "release_year": release_year,
        "colorway": colorway
    }


@router.delete("/{sneaker_id}")
def delete_sneaker(sneaker_id: int, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    """Delete a sneaker (requires API key)"""
    cursor = db.cursor()
    cursor.execute("SELECT id FROM sneakers WHERE id = ?", (sneaker_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Sneaker not found")
    
    cursor.execute("DELETE FROM sneakers WHERE id = ?", (sneaker_id,))
    db.commit()
    return {"message": "Sneaker deleted successfully"}
