from models.database import get_all_songs

def list_all_songs():
    """List all songs in the database"""
    songs = get_all_songs()
    
    if not songs:
        print("❌ No songs in database yet!")
        print("\nAdd songs using:")
        print("  python add_song.py <audio_file> <title> <artist>")
        return
    
    print("=" * 60)
    print(f"📚 Songs in Database ({len(songs)} total)")
    print("=" * 60)
    print()
    
    for song in songs:
        print(f"ID: {song.id}")
        print(f"Title: {song.title}")
        print(f"Artist: {song.artist}")
        print(f"Duration: {song.duration:.2f} seconds")
        print(f"Features: {song.feature_path}")
        print("-" * 60)

if __name__ == "__main__":
    list_all_songs()