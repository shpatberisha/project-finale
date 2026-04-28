from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_db
from models import Brand, Sneaker, SneakerBase, BrandBase, SneakerWithBrand
from security import verify_api_key

app = FastAPI(title="Sneaker Management API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup():
    init_db()

# ========== BRANDS ENDPOINTS ==========

@app.get("/api/brands", response_model=list[Brand])
def get_brands():
    """Get all brands"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM brands ORDER BY name")
        brands = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return brands

@app.get("/api/brands/{brand_id}", response_model=Brand)
def get_brand(brand_id: int):
    """Get specific brand by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM brands WHERE id = ?", (brand_id,))
        row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"id": row[0], "name": row[1]}

@app.post("/api/brands", response_model=Brand, dependencies=[Depends(verify_api_key)])
def create_brand(brand: BrandBase):
    """Create a new brand (requires API key)"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO brands (name) VALUES (?)", (brand.name,))
            conn.commit()
            brand_id = cursor.lastrowid
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"id": brand_id, "name": brand.name}

@app.put("/api/brands/{brand_id}", response_model=Brand, dependencies=[Depends(verify_api_key)])
def update_brand(brand_id: int, brand: BrandBase):
    """Update a brand (requires API key)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM brands WHERE id = ?", (brand_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Brand not found")
        try:
            cursor.execute("UPDATE brands SET name = ? WHERE id = ?", (brand.name, brand_id))
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return {"id": brand_id, "name": brand.name}

@app.delete("/api/brands/{brand_id}", dependencies=[Depends(verify_api_key)])
def delete_brand(brand_id: int):
    """Delete a brand (requires API key)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM brands WHERE id = ?", (brand_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Brand not found")
        cursor.execute("DELETE FROM brands WHERE id = ?", (brand_id,))
        conn.commit()
    return {"message": "Brand deleted successfully"}

# ========== SNEAKERS ENDPOINTS ==========

@app.get("/api/sneakers", response_model=list[SneakerWithBrand])
def get_sneakers():
    """Get all sneakers with brand info"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, s.brand_id, s.product_link, s.categories, 
                   s.price, s.release_year, s.colorway, b.id, b.name
            FROM sneakers s
            JOIN brands b ON s.brand_id = b.id
            ORDER BY s.name
        """)
        sneakers = []
        for row in cursor.fetchall():
            sneaker = {
                "id": row[0],
                "name": row[1],
                "brand_id": row[2],
                "product_link": row[3],
                "categories": row[4],
                "price": row[5],
                "release_year": row[6],
                "colorway": row[7],
                "brand": {"id": row[8], "name": row[9]}
            }
            sneakers.append(sneaker)
    return sneakers

@app.get("/api/sneakers/{sneaker_id}", response_model=SneakerWithBrand)
def get_sneaker(sneaker_id: int):
    """Get specific sneaker by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, s.brand_id, s.product_link, s.categories, 
                   s.price, s.release_year, s.colorway, b.id, b.name
            FROM sneakers s
            JOIN brands b ON s.brand_id = b.id
            WHERE s.id = ?
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
        "colorway": row[7],
        "brand": {"id": row[8], "name": row[9]}
    }

@app.post("/api/sneakers", response_model=Sneaker, dependencies=[Depends(verify_api_key)])
def create_sneaker(sneaker: SneakerBase):
    """Create a new sneaker (requires API key)"""
    with get_db() as conn:
        cursor = conn.cursor()
        # Verify brand exists
        cursor.execute("SELECT id FROM brands WHERE id = ?", (sneaker.brand_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Brand not found")
        
        cursor.execute("""
            INSERT INTO sneakers (name, brand_id, product_link, categories, price, release_year, colorway)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sneaker.name, sneaker.brand_id, sneaker.product_link, sneaker.categories,
              sneaker.price, sneaker.release_year, sneaker.colorway))
        conn.commit()
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

@app.put("/api/sneakers/{sneaker_id}", response_model=Sneaker, dependencies=[Depends(verify_api_key)])
def update_sneaker(sneaker_id: int, sneaker: SneakerBase):
    """Update a sneaker (requires API key)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sneakers WHERE id = ?", (sneaker_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Sneaker not found")
        
        cursor.execute("""
            UPDATE sneakers SET name = ?, brand_id = ?, product_link = ?, 
                   categories = ?, price = ?, release_year = ?, colorway = ?
            WHERE id = ?
        """, (sneaker.name, sneaker.brand_id, sneaker.product_link, sneaker.categories,
              sneaker.price, sneaker.release_year, sneaker.colorway, sneaker_id))
        conn.commit()
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

@app.delete("/api/sneakers/{sneaker_id}", dependencies=[Depends(verify_api_key)])
def delete_sneaker(sneaker_id: int):
    """Delete a sneaker (requires API key)"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sneakers WHERE id = ?", (sneaker_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Sneaker not found")
        cursor.execute("DELETE FROM sneakers WHERE id = ?", (sneaker_id,))
        conn.commit()
    return {"message": "Sneaker deleted successfully"}

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}
