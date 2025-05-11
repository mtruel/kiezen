# Kiezen Backend

This is the backend service for the Kiezen DJ application, built with FastAPI.

## Features

- RESTful API for managing songs
- SQLite database for data persistence
- File storage for music files
- CORS support for frontend integration

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies using UV:
```bash
uv pip install -r requirements.txt
```

3. Create a `.env` file with the following variables:
```
DATABASE_URL=sqlite:///./kiezen.db
MUSIC_FILES_DIR=music_files
DEBUG=True
```

4. Create the music files directory:
```bash
mkdir music_files
```

## Running the Application

You can start the development server in two ways:

1. Using FastAPI CLI (recommended):
```bash
uv run fastapi dev ./src/main.py
```

2. Using Uvicorn directly:
```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Songs
- `GET /api/songs/` - List all songs
- `POST /api/songs/` - Create a new song
- `GET /api/songs/{song_id}` - Get a specific song
- `PUT /api/songs/{song_id}` - Update a song
- `DELETE /api/songs/{song_id}` - Delete a song
