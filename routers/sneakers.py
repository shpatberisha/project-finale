import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.sneaker import Sneaker, SneakerCreate
from database import get_db_connection
from auth.security import get_api_key

router = APIRouter()


@router.get("/", response_model=List[Sneaker])
def get_sneakers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, brand_id, product_link, categories, price, release_year, colorway FROM sneakers")
    sneakers = cursor.fetchall()
    conn.close()

    return [
        {
            "id": sneaker[0],
            "name": sneaker[1],
            "brand_id": sneaker[2],
            "product_link": sneaker[3],
            "categories": sneaker[4].split(',') if sneaker[4] else [],  # Split category names into a list
            "price": sneaker[5],
            "release_year": sneaker[6],
            "colorway": sneaker[7]
        }
        for sneaker in sneakers
    ]


@router.post("/", response_model=Sneaker)
def create_sneaker(sneaker: SneakerCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        categories = ",".join(sneaker.categories)  # Convert list of category names to a comma-separated string
        cursor.execute("INSERT INTO sneakers (name, brand_id, product_link, categories, price, release_year, colorway) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (sneaker.name, sneaker.brand_id, sneaker.product_link, categories, sneaker.price, sneaker.release_year, sneaker.colorway))
        conn.commit()
        sneaker_id = cursor.lastrowid
        return Sneaker(id=sneaker_id, **sneaker.dict())
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The sneaker '{sneaker.name}' already exists."
        )
    finally:
        conn.close()


@router.put("/{sneaker_id}", response_model=Sneaker)
def update_sneaker(sneaker_id: int, sneaker: SneakerCreate, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    categories = ",".join(sneaker.categories)  # Convert list of category names to a comma-separated string
    cursor.execute(
        "UPDATE sneakers SET name = ?, brand_id = ?, product_link = ?, categories = ?, price = ?, release_year = ?, colorway = ? "
        "WHERE id = ?",
        (sneaker.name, sneaker.brand_id, sneaker.product_link, categories, sneaker.price, sneaker.release_year, sneaker.colorway, sneaker_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Sneaker not found")
    conn.commit()
    conn.close()
    return Sneaker(id=sneaker_id, **sneaker.dict())


@router.delete("/{sneaker_id}", response_model=dict)
def delete_sneaker(sneaker_id: int, _: str = Depends(get_api_key)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sneakers WHERE id = ?", (sneaker_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Sneaker not found")
    conn.commit()
    conn.close()
    return {"detail": "Sneaker deleted"}
