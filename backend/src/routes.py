from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas, database
import os
import shutil

router = APIRouter()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# File upload route
@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Create the music files directory if it doesn't exist
    music_dir = "music_files"
    os.makedirs(music_dir, exist_ok=True)
    
    # Create a safe filename
    file_location = os.path.join(music_dir, file.filename)
    
    # Save the file
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # Create a song entry in the database
    song_data = schemas.SongCreate(
        title=os.path.splitext(file.filename)[0],  # Use filename as title
        artist="Unknown",  # Default value
        file_path=file_location,
        is_dummy=0  # Set to 0 for uploaded files
    )
    
    return crud.create_song(db=db, song=song_data)

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
def delete_song(song_id: int, db: Session = Depends(get_db)):
    db_song = crud.delete_song(db, song_id=song_id)
    if db_song is None:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"message": "Song deleted successfully"} 