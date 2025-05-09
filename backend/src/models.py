from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    artist = Column(String, index=True)
    album = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    file_path = Column(String, nullable=True)  # Path to the music file
    is_dummy = Column(Integer, default=0)  # 0 for real songs, 1 for dummy songs
    link = Column(String, nullable=True)  # For dummy songs with external links
    file_hash = Column(String, nullable=True)  # Hash of the file for deduplication
    duration = Column(Float, nullable=True)  # Duration in seconds 