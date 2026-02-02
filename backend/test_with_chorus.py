import sys
import librosa
import soundfile as sf
from utils.feature_extractor import FeatureExtractor
from utils.similarity import SimilarityMatcher
from models.database import get_all_songs

def test_chorus_section(audio_path, start_sec, end_sec):
    """
    Test a specific section of audio file
    """
    print("="*60)
    print(f"Testing: {audio_path}")
    print(f"Section: {start_sec}s to {end_sec}s")
    print("="*60)
    
    # Load and extract section
    y_full, sr = librosa.load(audio_path, sr=16000)
    start_sample = int(start_sec * sr)
    end_sample = int(end_sec * sr)
    y_section = y_full[start_sample:end_sample]
    
    # Save temp file
    temp_file = "temp_test.wav"
    sf.write(temp_file, y_section, sr)
    
    # Extract features
    extractor = FeatureExtractor(sr=16000)
    test_features = extractor.extract_features(temp_file)
    
    # Compare with all songs
    songs = get_all_songs()
    matcher = SimilarityMatcher()
    
    results = []
    
    for song in songs:
        song_features = extractor.load_features(song.feature_path)
        total_score, individual_scores = matcher.combined_similarity(
            test_features,
            song_features
        )
        
        results.append({
            'title': song.title,
            'artist': song.artist,
            'similarity': total_score,
            'pitch': individual_scores['pitch'],
            'mfcc': individual_scores['mfcc'],
            'chroma': individual_scores['chroma']
        })
    
    # Sort by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        print(f"\n#{i}: {result['title']} by {result['artist']}")
        print(f"   Total: {result['similarity']:.2f}%")
        print(f"   Pitch: {result['pitch']:.2f}%")
    
    print("\n" + "="*60)
    
    # Clean up
    import os
    os.remove(temp_file)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python test_with_chorus.py <audio_file> <start_sec> <end_sec>")
        print("\nExample: python test_with_chorus.py 'song.mp3' 50 80")
        print("\nUse the SAME timestamps you used when adding the song!")
        sys.exit(1)
    
    test_chorus_section(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))