import sys
from utils.feature_extractor import FeatureExtractor
from utils.similarity import SimilarityMatcher
from models.database import get_all_songs

def test_audio_file(audio_path):
    """
    Test matching with a direct audio file (not recorded from speakers)
    """
    print("="*60)
    print(f"Testing audio file: {audio_path}")
    print("="*60)
    
    # Extract features
    extractor = FeatureExtractor(sr=16000)
    test_features = extractor.extract_features(audio_path)
    
    # Get all songs
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
        print(f"   Pitch: {result['pitch']:.2f}% | MFCC: {result['mfcc']:.2f}% | Chroma: {result['chroma']:.2f}%")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_with_file.py <audio_file.mp3>")
        print("Example: python test_with_file.py 'D:\\Music\\living_life.mp3'")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    test_audio_file(audio_file)