from utils.feature_extractor import FeatureExtractor
from utils.similarity import SimilarityMatcher

def test_self_similarity():
    """
    Compare a song's features with itself
    Should get ~100% similarity
    """
    extractor = FeatureExtractor(sr=16000)
    matcher = SimilarityMatcher()
    
    songs = [
        ('Senorita', 'song_features/song_senorita.npy'),
        ('Lake of Fire', 'song_features/song_lake_of_fire.npy'),
        ('Hope', 'song_features/song_hope.npy'),
        ('Living Life', 'song_features/song_living_life_in_the_night.npy')
    ]
    
    print("="*60)
    print("Testing self-similarity (should be ~100% for each)")
    print("="*60)
    
    for name, path in songs:
        features = extractor.load_features(path)
        
        # Compare with itself
        total_score, individual_scores = matcher.combined_similarity(features, features)
        
        print(f"\n{name}:")
        print(f"  Total: {total_score:.2f}%")
        print(f"  Pitch: {individual_scores['pitch']:.2f}%")
        print(f"  MFCC: {individual_scores['mfcc']:.2f}%")
        print(f"  Chroma: {individual_scores['chroma']:.2f}%")
        
        if total_score < 95:
            print(f"  ⚠️ WARNING: Self-similarity is too low!")

if __name__ == "__main__":
    test_self_similarity()