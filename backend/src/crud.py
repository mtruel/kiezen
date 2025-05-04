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
    db_song = db.query(models.Song).filter(models.Song.id == song_id).first()
    if db_song and db_song.file_path:
        # Delete the associated file if it exists
        if os.path.exists(db_song.file_path):
            os.remove(db_song.file_path)
    if db_song:
        db.delete(db_song)
        db.commit()
    return db_song 