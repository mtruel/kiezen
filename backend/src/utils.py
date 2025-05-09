import hashlib
from typing import Optional, Tuple, List, Dict, Any
from sqlalchemy.orm import Session
from . import models
import os
import magic
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.ogg import OggFileType
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.easyid3 import EasyID3

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

def validate_music_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate if a file is a valid music file using python-magic.
    Returns a tuple of (is_valid, error_message).
    """
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        allowed_types = {
            "audio/mpeg": "MP3",
            "audio/wav": "WAV",
            "audio/ogg": "OGG",
            "audio/flac": "FLAC",
            "audio/mp4": "M4A",
            "audio/aac": "AAC"
        }
        
        if file_type not in allowed_types:
            return False, f"File type {file_type} is not supported. Supported types are: {', '.join(allowed_types.values())}"
            
        return True, ""
    except Exception as e:
        return False, f"Error validating file: {str(e)}"

def read_audio_tags(file_path: str) -> Dict[str, Any]:
    """
    Read audio metadata tags from a music file.
    Returns a dictionary with the metadata.
    """
    try:
        audio = File(file_path)
        if audio is None:
            return {}
            
        tags = {}
        
        # Handle different file types
        if isinstance(audio, MP3):
            if audio.tags is not None:
                # Get title and artist
                tags["title"] = audio.tags.get("TIT2", [""])[0]
                tags["artist"] = audio.tags.get("TPE1", [""])[0]
                tags["album"] = audio.tags.get("TALB", [""])[0]
                tags["genre"] = audio.tags.get("TCON", [""])[0]
                
                # Handle year/date field carefully
                date = audio.tags.get("TDRC", [""])[0]
                if date:
                    try:
                        # If it's an ID3TimeStamp, get the year
                        if hasattr(date, 'year'):
                            tags["year"] = str(date.year)
                        # If it's a string, try to extract the year
                        elif isinstance(date, str):
                            # Try to extract year from various formats
                            import re
                            year_match = re.search(r'\d{4}', date)
                            if year_match:
                                tags["year"] = year_match.group(0)
                    except Exception as e:
                        print(f"Error parsing date: {str(e)}")
                
        elif isinstance(audio, (WAVE, OggFileType, FLAC, MP4)):
            if audio.tags is not None:
                tags["title"] = audio.tags.get("title", [""])[0]
                tags["artist"] = audio.tags.get("artist", [""])[0]
                tags["album"] = audio.tags.get("album", [""])[0]
                tags["genre"] = audio.tags.get("genre", [""])[0]
                
                # Handle date field carefully
                date = audio.tags.get("date", [""])[0]
                if date:
                    try:
                        # If it's a string, try to extract the year
                        if isinstance(date, str):
                            import re
                            year_match = re.search(r'\d{4}', date)
                            if year_match:
                                tags["year"] = year_match.group(0)
                    except Exception as e:
                        print(f"Error parsing date: {str(e)}")
                
        # Clean up empty values and strip whitespace
        return {k: v.strip() if isinstance(v, str) else v for k, v in tags.items() if v}
    except Exception as e:
        print(f"Error reading audio tags: {str(e)}")
        return {} 