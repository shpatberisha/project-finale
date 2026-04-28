# Sneaker Management System

A full-stack sneaker and brand management app with a FastAPI backend and a Streamlit frontend, persisted in SQLite.

## Stack

- **Backend:** FastAPI + Uvicorn (Python)
- **Frontend:** Streamlit (Python)
- **Database:** SQLite (`DSA/sneakers.db`, auto-created)
- **Auth:** API key passed in the `api-key` header (read from `DSA/.env`)

## Project Layout

```
DSA/
├── main.py              # FastAPI entrypoint (mounts routers)
├── app.py               # Streamlit UI (talks to backend at http://localhost:8000)
├── database.py          # SQLite init + FastAPI get_db dependency
├── models/              # Pydantic models (Brand, Sneaker)
├── routers/             # FastAPI routers (brands, sneakers)
├── auth/                # API key generation + verification
├── .streamlit/config.toml  # Streamlit server config (port 5000, headless)
├── .env                 # API key (auto-generated on setup)
└── requirements.txt
```

## Replit Environment Setup

Two workflows are configured:

- **Backend API** — `cd DSA && python -m uvicorn main:app --host 127.0.0.1 --port 8000`
  - Listens on `localhost:8000` (internal only).
- **Start application** — Streamlit on `0.0.0.0:5000` (webview)
  - Streamlit config disables CORS/XSRF and websocket compression so the page works through Replit's iframe proxy.

The Streamlit frontend calls the backend via `http://localhost:8000/api/...`.

## API Key

The `DSA/.env` file is created at setup time with a random key. To regenerate:

```bash
cd DSA && python auth/generate_key.py
```

Send the key in the `api-key` header for any POST/PUT/DELETE request.

## Deployment

Configured as a **VM** deployment that runs both the FastAPI backend (localhost:8000) and the Streamlit frontend (0.0.0.0:5000) in the same process group. VM is required because Streamlit holds an open websocket per session.

## Recent Changes

- 2026-04-28: Initial Replit import setup.
  - Installed Python deps (FastAPI, Uvicorn, Streamlit, Pydantic, requests, python-dotenv).
  - Generated API key into `DSA/.env`.
  - Added `DSA/.streamlit/config.toml` with proxy-friendly settings.
  - Fixed `database.py`: removed the `@contextmanager` decorator from `get_db` so FastAPI's `Depends` can use it as a generator (was causing 500 on every API call).
  - Configured Backend API + Start application workflows and VM deployment.
