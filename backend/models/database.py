from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class Song(Base):
    __tablename__ = 'songs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    artist = Column(String(200), nullable=False)
    duration = Column(Float)  # in seconds
    feature_path = Column(String(500))  # path to .npy file
    
    def __repr__(self):
        return f"<Song(id={self.id}, title='{self.title}', artist='{self.artist}')>"

# Create database directory if it doesn't exist
DB_DIR = 'database'
os.makedirs(DB_DIR, exist_ok=True)

# Database connection
DATABASE_PATH = os.path.join(DB_DIR, 'songs.db')
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def add_song(title, artist, duration, feature_path):
    """Add a new song to the database"""
    session = get_session()
    song = Song(
        title=title,
        artist=artist,
        duration=duration,
        feature_path=feature_path
    )
    session.add(song)
    session.commit()
    song_id = song.id
    session.close()
    return song_id

def get_all_songs():
    """Retrieve all songs from database"""
    session = get_session()
    songs = session.query(Song).all()
    session.close()
    return songs

def get_song_by_id(song_id):
    """Get a specific song by ID"""
    session = get_session()
    song = session.query(Song).filter_by(id=song_id).first()
    session.close()
    return song