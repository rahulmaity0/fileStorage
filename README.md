# File Storage API (FastAPI)

A FastAPI service for uploading, listing, downloading and deleting files, with JWT authentication and automatic thumbnails for images. `index.html` is a small browser front end for the API.

## Features

- Register and log in (bcrypt password hashing), receiving a JWT
- Every `/files` route requires a bearer token, and users only ever see their own files
- Uploads up to 10 MB, stored under a generated UUID file name
- Thumbnails created with Pillow for image uploads
- SQLAlchemy models with SQLite by default; any SQLAlchemy database URL works

## Tech stack

Python, FastAPI, SQLAlchemy, Pydantic Settings, python-jose, passlib/bcrypt, Pillow, Uvicorn

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Get a JWT (form fields `username`, `password`) |
| GET | `/auth/me` | Current user |
| POST | `/files/upload` | Upload a file |
| GET | `/files/` | List your files |
| GET | `/files/{file_id}` | File metadata |
| GET | `/files/download/{file_id}` | Download a file |
| DELETE | `/files/{file_id}` | Delete a file |

Interactive API docs are served at `/docs`.

## Running locally

```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # then set SECRET_KEY
uvicorn app.main:app --reload
```

The `Procfile` runs the same app on platforms such as Heroku or Render.
