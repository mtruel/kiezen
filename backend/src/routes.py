from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
import asyncio
from . import crud, models, schemas, utils
from .database import get_db

router = APIRouter()

async def process_file(file: UploadFile, db: Session):
    try:
        # Create the music files directory if it doesn't exist
        music_dir = "music_files"
        os.makedirs(music_dir, exist_ok=True)
        
        # Create a safe filename
        file_location = os.path.join(music_dir, file.filename)
        
        # Save the file temporarily
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        # Validate the file type
        is_valid, error_message = utils.validate_music_file(file_location)
        if not is_valid:
            # Clean up the invalid file
            os.remove(file_location)
            return {
                "filename": file.filename,
                "error": "INVALID_FILE_TYPE",
                "message": error_message
            }
        
        # Check for duplicates
        is_duplicate, existing_song = utils.find_duplicates(db, file_location)
        if is_duplicate:
            # Clean up the duplicate file
            os.remove(file_location)
            return {
                "filename": file.filename,
                "error": "DUPLICATE_FILE",
                "message": "This file already exists in your library",
                "existing_song": {
                    "id": existing_song.id,
                    "title": existing_song.title,
                    "artist": existing_song.artist
                }
            }
        
        # Read audio tags
        tags = utils.read_audio_tags(file_location)
        
        # Calculate file hash
        file_hash = utils.calculate_file_hash(file_location)
        
        # Create a song entry in the database
        song_data = schemas.SongCreate(
            title=tags.get("title", os.path.splitext(file.filename)[0]),  # Use tags or filename as title
            artist=tags.get("artist", "Unknown"),  # Use tags or default value
            album=tags.get("album"),  # Optional
            genre=tags.get("genre"),  # Optional
            year=int(tags.get("year", "0")) if tags.get("year") and tags.get("year").isdigit() else None,  # Optional, only convert if it's a valid number
            file_path=file.filename,  # Store only the filename
            is_dummy=0,  # Set to 0 for uploaded files
            file_hash=file_hash,  # Add the file hash
            duration=tags.get("duration"),
        )
        
        uploaded_song = crud.create_song(db=db, song=song_data)
        return {"song": uploaded_song}
        
    except Exception as e:
        # Clean up the file if it was created
        if os.path.exists(file_location):
            os.remove(file_location)
        return {
            "filename": file.filename,
            "error": "UPLOAD_FAILED",
            "message": f"Failed to upload file: {str(e)}"
        }

# File upload route
@router.post("/upload/")
async def upload_file(files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    uploaded_songs = []
    errors = []
    
    # Process files concurrently
    tasks = [process_file(file, db) for file in files]
    results = await asyncio.gather(*tasks)
    
    for result in results:
        if "error" in result:
            errors.append(result)
        else:
            uploaded_songs.append(result["song"])
    
    return {
        "uploaded_songs": uploaded_songs,
        "errors": errors
    }

# Song routes
@router.post("/songs/", response_model=schemas.Song)
def create_song(song: schemas.SongCreate, db: Session = Depends(get_db)):
    return crud.create_song(db=db, song=song)

@router.get("/songs/", response_model=List[schemas.Song])
def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs

@router.get("/songs/{song_id}", response_model=schemas.Song)
def read_song(song_id: int, db: Session = Depends(get_db)):
    db_song = crud.get_song(db, song_id=song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song

@router.put("/songs/{song_id}", response_model=schemas.Song)
def update_song(song_id: int, song: schemas.SongCreate, db: Session = Depends(get_db)):
    db_song = crud.update_song(db, song_id=song_id, song=song)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return db_song

@router.delete("/songs/{song_id}")
def delete_song(song_id: str, db: Session = Depends(get_db)):
    try:
        song_id_int = int(song_id)
        db_song = crud.delete_song(db, song_id=song_id_int)
        if db_song is None:
            raise HTTPException(status_code=404, detail="Song not found")
        return {"message": "Song deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid song ID format") 