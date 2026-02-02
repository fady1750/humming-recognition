import os
import sys
import librosa
import soundfile as sf
import numpy as np
from utils.feature_extractor import FeatureExtractor
from models.database import add_song

def find_chorus_section(y, sr, duration=30):
    """
    Find the most energetic section (likely chorus)
    Returns start and end in seconds
    """
    # Calculate energy over time
    hop_length = 512
    frame_length = 2048
    
    # RMS energy
    rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
    
    # Convert to time
    times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
    
    # Find section with highest average energy
    window_frames = int(duration * sr / hop_length)
    
    best_energy = 0
    best_start_frame = 0
    
    for i in range(len(rms) - window_frames):
        energy = np.mean(rms[i:i+window_frames])
        if energy > best_energy:
            best_energy = energy
            best_start_frame = i
    
    start_time = times[best_start_frame]
    end_time = start_time + duration
    
    return start_time, end_time

def extract_and_add_chorus(audio_path, title, artist, chorus_duration=30):
    """
    Extract chorus section and add to database
    """
    try:
        print("="*60)
        print(f"Processing: {title} by {artist}")
        print("="*60)
        
        # Load full audio
        print("📂 Loading audio...")
        y_full, sr = librosa.load(audio_path, sr=16000)
        total_duration = len(y_full) / sr
        print(f"   Total duration: {total_duration:.1f}s")
        
        # Find chorus
        print("🔍 Finding chorus section...")
        start, end = find_chorus_section(y_full, sr, chorus_duration)
        print(f"   Chorus found: {start:.1f}s to {end:.1f}s")
        
        # Extract chorus
        start_sample = int(start * sr)
        end_sample = int(end * sr)
        y_chorus = y_full[start_sample:end_sample]
        
        # Save temporary file
        temp_file = "temp_chorus.wav"
        sf.write(temp_file, y_chorus, sr)
        
        # Extract features (MELODY-FOCUSED)
        print("🎵 Extracting melody features...")
        extractor = FeatureExtractor(sr=16000)
        features = extractor.extract_features(temp_file)
        
        # Verify pitch extraction
        voiced_frames = np.sum(features['pitch'] > 0)
        total_frames = len(features['pitch'])
        print(f"   Voiced frames: {voiced_frames}/{total_frames} ({100*voiced_frames/total_frames:.1f}%)")
        
        if voiced_frames < total_frames * 0.3:
            print("   ⚠️ WARNING: Low voiced content, might be instrumental!")
        
        # Save features
        feature_filename = f"song_{title.replace(' ', '_').lower()}_chorus.npy"
        feature_path = os.path.join('song_features', feature_filename)
        extractor.save_features(features, feature_path)
        
        # Add to database
        song_id = add_song(
            title=title,
            artist=artist,
            duration=chorus_duration,
            feature_path=feature_path
        )
        
        # Clean up
        os.remove(temp_file)
        
        print(f"✅ Added song ID {song_id}: {title}")
        print("="*60)
        return song_id
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_chorus.py <audio_file> <title> <artist>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    song_title = sys.argv[2]
    song_artist = sys.argv[3] if len(sys.argv) > 3 else "Unknown"
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        sys.exit(1)
    
    extract_and_add_chorus(audio_file, song_title, song_artist)