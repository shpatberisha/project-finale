# Nike Sneakers Management System

A full-stack application for managing Nike sneakers with FastAPI backend and Streamlit frontend.

## Features

- **User Authentication**: Register and login with secure password hashing
- **Sneakers Management**: Create, read, update, and delete sneaker records
- **Brands Management**: Manage sneaker brands (Nike, Jordan, etc.)
- **Dashboard**: Visualizations and statistics for your sneaker collection
- **API Key Authentication**: Secure write operations with API key validation
- **SQLite Database**: Lightweight persistent storage

## Requirements

- Python 3.8+
- pip

## How to Run

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the FastAPI Backend

Open a terminal and run:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Step 3: Start the Streamlit Frontend

Open a second terminal and run:

```bash
streamlit run app.py
```

The frontend will open in your browser at `http://localhost:8501`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info

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

## Project Structure

```
.
├── main.py              # FastAPI application entry point
├── app.py               # Streamlit frontend
├── database.py          # SQLite database setup and queries
├── requirements.txt     # Python dependencies
├── models/
│   ├── sneaker.py       # Sneaker Pydantic model
│   ├── brand.py         # Brand Pydantic model
│   └── user.py          # User Pydantic model
├── routers/
│   ├── sneakers.py      # Sneakers API endpoints
│   ├── brands.py        # Brands API endpoints
│   ├── auth.py          # Authentication endpoints
│   └── api_key.py       # API key validation
└── auth/
    ├── security.py      # Security utilities
    └── generate_key.py  # API key generation
```

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive Swagger documentation.
