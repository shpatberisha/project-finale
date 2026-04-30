# 👟 Sneaker Management System

A full-stack application built with **FastAPI** (backend) and **Streamlit** (frontend) to manage sneaker and brand information with SQLite database.

## Features

- ✅ View all sneakers and brands
- ✅ Add new sneakers and brands
- ✅ Update sneaker and brand information
- ✅ Delete sneakers and brands
- ✅ API key authentication for data modifications
- ✅ SQLite database for persistence
- ✅ Interactive Streamlit UI
- ✅ RESTful API with full documentation

## Installation & Setup

### 1. Navigate to project directory
```
cd C:\Users\Student\python\project-finale444
```

### 2. Create virtual environment
```
python -m venv venv
```

### 3. Activate virtual environment (Windows PowerShell)
```
.\venv\Scripts\Activate
```

### 4. Install dependencies
```
pip install -r requirements.txt
```

### 5. Generate API key (required for modifications)
```
python generate_key.py
```

This creates a `.env` file with your API key. You'll need this key for adding/editing/deleting data.

## Running the Application

### Terminal 1: Start FastAPI Backend
```
uvicorn main:app --reload
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Terminal 2: Start Streamlit Frontend
```
streamlit run app.py
```

The frontend will open at: http://localhost:8501

## Usage

### In Streamlit App (Frontend)

1. **View Sneakers**: See all sneakers with brand, price, release year, and colorway
2. **View Brands**: Browse all available brands
3. **Add Sneaker**: Add a new sneaker (requires API key)
4. **Add Brand**: Create a new brand (requires API key)
5. **Manage**: Delete brands or sneakers (requires API key)

### API Endpoints

#### Brands
- `GET /api/brands` - Get all brands
- `GET /api/brands/{id}` - Get specific brand
- `POST /api/brands` - Create brand (requires API key)
- `PUT /api/brands/{id}` - Update brand (requires API key)
- `DELETE /api/brands/{id}` - Delete brand (requires API key)

#### Sneakers
- `GET /api/sneakers` - Get all sneakers
- `GET /api/sneakers/{id}` - Get specific sneaker
- `POST /api/sneakers` - Create sneaker (requires API key)
- `PUT /api/sneakers/{id}` - Update sneaker (requires API key)
- `DELETE /api/sneakers/{id}` - Delete sneaker (requires API key)

#### Health Check
- `GET /health` - Server health status

### Using API with cURL

```bash
# Get all brands (no auth needed)
curl http://localhost:8000/api/brands

# Create a brand (requires API key)
curl -X POST http://localhost:8000/api/brands \
  -H "api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Nike\"}"

# Create a sneaker (requires API key)
curl -X POST http://localhost:8000/api/sneakers \
  -H "api-key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Air Jordan 1\",
    \"brand_id\": 1,
    \"price\": 150.00,
    \"release_year\": 1985,
    \"colorway\": \"Black/Red\"
  }"
```

## Project Structure

```
project-finale444/
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend
├── database.py          # SQLite database setup
├── models.py            # Pydantic models
├── security.py          # API key verification
├── generate_key.py      # Generate API key
├── requirements.txt     # Python dependencies
├── .env                 # API key (created by generate_key.py)
├── sneakers.db          # SQLite database (auto-created)
└── README.md            # This file
```

## Database Schema

### brands table
```sql
id          INTEGER PRIMARY KEY
name        TEXT UNIQUE NOT NULL
```

### sneakers table
```sql
id            INTEGER PRIMARY KEY
name          TEXT NOT NULL
brand_id      INTEGER (FOREIGN KEY)
product_link  TEXT
categories    TEXT
price         REAL
release_year  INTEGER
colorway      TEXT
```

## Troubleshooting

### "Port already in use" error
- Change the port: `uvicorn main:app --reload --port 8001`
- Or kill the process using port 8000

### API key not working
- Make sure `.env` file exists and has `API_KEY=your-key`
- Run `python generate_key.py` again to generate a new key
- Check that Streamlit is reading the correct API key from `.env`

### Database issues
- Delete `sneakers.db` and restart the backend to reset the database
- The database will be automatically recreated with fresh tables

### Streamlit can't connect to API
- Ensure FastAPI backend is running on `http://localhost:8000`
- Check that no firewall is blocking localhost connections

## Next Steps

1. Add more fields to the sneaker model (size, quantity, images, etc.)
2. Implement user authentication
3. Add filtering and search functionality
4. Deploy to production (Vercel, Heroku, etc.)
5. Add database migrations
6. Implement image uploads for sneakers

## Requirements

- Python 3.8+
- FastAPI 0.111.1
- Uvicorn 0.22.0
- Streamlit 1.25.0
- Pydantic 2.8.2
- SQLite3 (built-in)

## License

MIT License - Feel free to use this project for learning purposes!
