import os
import sys
import librosa
import soundfile as sf
import numpy as np
from utils.feature_extractor import FeatureExtractor
from models.database import add_song

def extract_chorus_manual(audio_path, title, artist, start_sec, end_sec):
    """
    Extract SPECIFIC section of song
    """
    try:
        print("="*60)
        print(f"Processing: {title} by {artist}")
        print(f"Section: {start_sec}s to {end_sec}s")
        print("="*60)
        
        # Load audio
        y_full, sr = librosa.load(audio_path, sr=16000)
        
        # Extract section
        start_sample = int(start_sec * sr)
        end_sample = int(end_sec * sr)
        y_section = y_full[start_sample:end_sample]
        
        duration = (end_sec - start_sec)
        print(f"Extracted: {duration}s")
        
        # Save temporary file
        temp_file = "temp_section.wav"
        sf.write(temp_file, y_section, sr)
        
        # Extract features
        print("🎵 Extracting features...")
        extractor = FeatureExtractor(sr=16000)
        features = extractor.extract_features(temp_file)
        
        # Check pitch
        voiced_frames = np.sum(features['pitch'] > 0)
        total_frames = len(features['pitch'])
        print(f"Voiced: {voiced_frames}/{total_frames} ({100*voiced_frames/total_frames:.1f}%)")
        
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
        
        os.remove(temp_file)
        
        print(f"✅ Added song ID {song_id}")
        print("="*60)
        return song_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python add_song_manual_chorus.py <file> <title> <artist> <start> <end>")
        print("Example: python add_song_manual_chorus.py song.mp3 'Title' 'Artist' 60 90")
        sys.exit(1)
    
    extract_chorus_manual(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        float(sys.argv[4]),
        float(sys.argv[5])
    )