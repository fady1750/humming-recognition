import sys
import os
from models.database import get_session, Song

def delete_song(song_id):
    """Delete a song from database and remove its feature file"""
    session = get_session()
    
    try:
        # Find the song
        song = session.query(Song).filter_by(id=song_id).first()
        
        if not song:
            print(f"❌ Song ID {song_id} not found")
            return False
        
        print(f"Found song: {song.title} by {song.artist}")
        
        # Delete feature file
        if song.feature_path and os.path.exists(song.feature_path):
            os.remove(song.feature_path)
            print(f"✅ Deleted feature file: {song.feature_path}")
        
        # Delete from database
        session.delete(song)
        session.commit()
        
        print(f"✅ Deleted song ID {song_id} from database")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_song.py <song_id>")
        print("\nAvailable songs:")
        from models.database import get_all_songs
        for song in get_all_songs():
            print(f"  ID {song.id}: {song.title} by {song.artist}")
        sys.exit(1)
    
    song_id = int(sys.argv[1])
    delete_song(song_id)