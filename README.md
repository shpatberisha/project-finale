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

## Installation

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Documentation

Once running, visit `/docs` for interactive Swagger documentation.
