from sqlalchemy.orm import Session
from . import models, schemas
import os

def get_song(db: Session, song_id: int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).order_by(models.Song.id.desc()).offset(skip).limit(limit).all()

def create_song(db: Session, song: schemas.SongCreate):
    db_song = models.Song(**song.model_dump())
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song

def update_song(db: Session, song_id: int, song: schemas.SongCreate):
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song:
        for key, value in song.model_dump().items():
            setattr(db_song, key, value)
        db.commit()
        db.refresh(db_song)
    return db_song

def delete_song(db: Session, song_id: int):
    try:
        db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
        if not db_song:
            return None

        # Store the file path before deleting the record
        file_path = db_song.file_path

        # First delete the database record
        db.delete(db_song)
        db.commit()

        # Then try to delete the file if it exists
        if file_path:
            try:
                # Construct the full path by joining with music_files directory
                full_path = os.path.join("music_files", file_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
                else:
                    print(f"Warning: File not found at path {full_path}")
            except OSError as e:
                # Log the error but don't fail the deletion since the DB record is already gone
                print(f"Warning: Failed to delete file {full_path}: {str(e)}")
        
        return db_song
    except Exception as e:
        db.rollback()
        print(f"Error deleting song: {str(e)}")
        raise 