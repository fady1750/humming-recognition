from utils.feature_extractor import FeatureExtractor
from utils.similarity import SimilarityMatcher
from models.database import get_all_songs

def test_stored_sections():
    """
    Test each stored chorus section against all songs
    This verifies the stored data is distinct
    """
    extractor = FeatureExtractor(sr=16000)
    matcher = SimilarityMatcher()
    songs = get_all_songs()
    
    for test_song in songs:
        print("\n" + "="*60)
        print(f"Testing: {test_song.title}")
        print("="*60)
        
        test_features = extractor.load_features(test_song.feature_path)
        
        results = []
        for song in songs:
            song_features = extractor.load_features(song.feature_path)
            score, _ = matcher.combined_similarity(test_features, song_features)
            results.append((song.title, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        
        for i, (title, score) in enumerate(results[:3], 1):
            marker = "✅" if title == test_song.title else "❌"
            print(f"  #{i}: {title} - {score:.1f}% {marker}")

if __name__ == "__main__":
    test_stored_sections()