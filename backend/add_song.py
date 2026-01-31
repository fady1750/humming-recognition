import os
import sys
import librosa
from utils.feature_extractor import FeatureExtractor
from models.database import add_song

def process_and_add_song(audio_path, title, artist):
    """
    Process an audio file and add it to the database
    """
    try:
        print(f"Processing: {title} by {artist}")
        
        # Extract features
        extractor = FeatureExtractor(sr=16000)
        features = extractor.extract_features(audio_path)
        
        # Get duration
        y, sr = librosa.load(audio_path, sr=16000)
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Save features
        feature_filename = f"song_{title.replace(' ', '_').lower()}.npy"
        feature_path = os.path.join('song_features', feature_filename)
        extractor.save_features(features, feature_path)
        
        # Add to database
        song_id = add_song(
            title=title,
            artist=artist,
            duration=duration,
            feature_path=feature_path
        )
        
        print(f"✅ Added song ID {song_id}: {title}")
        return song_id
        
    except Exception as e:
        print(f"❌ Error processing {title}: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 4:
        print("Usage: python add_song.py <audio_file> <title> <artist>")
        print("Example: python add_song.py imagine.wav 'Imagine' 'John Lennon'")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    song_title = sys.argv[2]
    song_artist = sys.argv[3]
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        sys.exit(1)
    
    process_and_add_song(audio_file, song_title, song_artist)