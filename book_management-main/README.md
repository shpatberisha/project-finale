# Nike Sneakers Management API

A FastAPI-based REST API for managing Nike sneakers and brands.

## Features

- **Sneakers Management**: Create, read, update, and delete sneaker records
- **Brands Management**: Manage sneaker brands (Nike, Jordan, etc.)
- **API Key Authentication**: Secure write operations with API key validation
- **SQLite Database**: Lightweight persistent storage

## API Endpoints

### Sneakers
- `GET /api/sneakers/` - List all sneakers
- `POST /api/sneakers/` - Create a new sneaker (requires API key)
- `PUT /api/sneakers/{id}` - Update a sneaker (requires API key)
- `DELETE /api/sneakers/{id}` - Delete a sneaker (requires API key)

### Brands
- `GET /api/brands/` - List all brands
- `POST /api/brands/` - Create a new brand (requires API key)
- `PUT /api/brands/{id}` - Update a brand (requires API key)
- `DELETE /api/brands/{id}` - Delete a brand (requires API key)

## Sneaker Model

```json
{
  "name": "Air Jordan 1 Retro High OG",
  "brand_id": 1,
  "product_link": "https://nike.com/...",
  "categories": ["Basketball", "Lifestyle"],
  "price": 180.00,
  "release_year": 2023,
  "colorway": "Chicago"
}
```

## Installation & Running

### 1. Navigate to the project directory
```bash
cd book_management-main
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate an API key (for protected routes)
```bash
python auth/generate_key.py
```
This creates a `.env` file with your API key. Use this key in the `api-key` header for POST/PUT/DELETE requests.

### 5. Run the FastAPI server
```bash
uvicorn main:app --reload
```

### 6. Access the API
- **API Base URL**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

The project uses **SQLite** (`sneakers.db`). The database file is automatically created on first startup with two tables:
- `brands` - Stores brand information
- `sneakers` - Stores sneaker details with foreign key to brands

## Authentication

Protected endpoints (POST, PUT, DELETE) require an API key:
```bash
curl -X POST "http://localhost:8000/api/brands/" \
  -H "api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Nike"}'
```

## Documentation

Once running, visit `/docs` for interactive Swagger documentation.
