import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.brand import Brand, BrandCreate
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()


@router.get("/", response_model=List[Brand])
def get_brands():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM brands")
    brands = cursor.fetchall()
    conn.close()
    return [{"id": brand[0], "name": brand[1]} for brand in brands]


@router.post("/", response_model=Brand)
def create_brand(
        brand: BrandCreate,
        _: str = Depends(get_api_key)  # Enforce API key
):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO brands (name) VALUES (?)", (brand.name,))
        conn.commit()
        brand_id = cursor.lastrowid
        return Brand(id=brand_id, name=brand.name)
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The brand '{brand.name}' already exists."
        )
    finally:
        conn.close()


@router.put("/{brand_id}", response_model=Brand)
def update_brand(
        brand_id: int,
        brand: BrandCreate,
        _: str = Depends(get_api_key)  # Enforce API key
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE brands SET name = ? WHERE id = ?", (brand.name, brand_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Brand not found")
    conn.commit()
    conn.close()
    return Brand(id=brand_id, name=brand.name)


@router.delete("/{brand_id}", response_model=dict)
def delete_brand(
        brand_id: int,
        _: str = Depends(get_api_key)  # Enforce API key
):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM brands WHERE id = ?", (brand_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Brand not found")
    conn.commit()
    conn.close()

    return {"detail": "Brand deleted"}
