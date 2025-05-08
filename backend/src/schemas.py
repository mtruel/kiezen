from pydantic import BaseModel, ConfigDict
from typing import Optional

class SongBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    is_dummy: int = 0  # 0 for real songs, 1 for dummy songs
    link: Optional[str] = None
    file_path: Optional[str] = None
    file_hash: Optional[str] = None  # Hash of the file for deduplication

class SongCreate(SongBase):
    pass

class Song(SongBase):
    id: int
    model_config = ConfigDict(from_attributes=True) 