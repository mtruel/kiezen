from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
from . import models, routes
from .database import engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kiezen Backend", version="1.0.0")

# Configure CORS
allowed_origins = [
    os.getenv("FRONTEND_DEV_URL", "http://localhost:5173"),  # Vite default dev server
    os.getenv("FRONTEND_PROD_URL", "http://localhost:3000"),  # Production URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create music files directory if it doesn't exist
MUSIC_FILES_DIR = "music_files"
os.makedirs(MUSIC_FILES_DIR, exist_ok=True)

# Mount the music files directory
app.mount("/music/music_files", StaticFiles(directory=MUSIC_FILES_DIR), name="music")

# Include routes
app.include_router(routes.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Kiezen Backend API"}

def run_dev():
    """Run the development server with hot reloading"""
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

def run_prod():
    """Run the production server"""
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000) 