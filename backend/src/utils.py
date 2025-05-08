import hashlib
from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from . import models
import os

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read the file in chunks to handle large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def find_duplicates(db: Session, file_path: str) -> Tuple[bool, Optional[models.Song]]:
    """
    Check if a file is a duplicate by comparing its hash with existing files.
    Returns a tuple of (is_duplicate, existing_song).
    """
    if not os.path.exists(file_path):
        return False, None
        
    file_hash = calculate_file_hash(file_path)
    
    # Check for exact file hash match
    existing_song = db.query(models.Song).filter(
        models.Song.file_hash == file_hash
    ).first()
    
    if existing_song:
        return True, existing_song
        
    return False, None

def find_similar_songs(db: Session, title: str, artist: str) -> List[models.Song]:
    """
    Find songs with similar metadata (title and artist).
    This is a simple implementation that could be enhanced with fuzzy matching.
    """
    return db.query(models.Song).filter(
        models.Song.title.ilike(f"%{title}%"),
        models.Song.artist.ilike(f"%{artist}%")
    ).all() 