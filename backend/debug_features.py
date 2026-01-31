from utils.feature_extractor import FeatureExtractor
import numpy as np

def debug_song_features(song_feature_path):
    """Debug: Check if song features are valid"""
    extractor = FeatureExtractor(sr=16000)
    
    try:
        features = extractor.load_features(song_feature_path)
        
        print("="*60)
        print(f"📊 Analyzing features from: {song_feature_path}")
        print("="*60)
        
        for key, value in features.items():
            if isinstance(value, np.ndarray):
                print(f"\n{key}:")
                print(f"  Shape: {value.shape}")
                print(f"  Min: {np.min(value):.4f}")
                print(f"  Max: {np.max(value):.4f}")
                print(f"  Mean: {np.mean(value):.4f}")
                print(f"  Non-zero values: {np.count_nonzero(value)}/{value.size}")
                
                # Check for problems
                if np.all(value == 0):
                    print(f"  ⚠️ WARNING: All values are zero!")
                if np.any(np.isnan(value)):
                    print(f"  ⚠️ WARNING: Contains NaN values!")
                if np.any(np.isinf(value)):
                    print(f"  ⚠️ WARNING: Contains infinite values!")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error loading features: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import sys
    from models.database import get_all_songs
    
    songs = get_all_songs()
    
    if len(songs) == 0:
        print("❌ No songs in database!")
    else:
        print(f"Found {len(songs)} songs in database\n")
        
        for song in songs:
            print(f"\n{'='*60}")
            print(f"Song: {song.title} by {song.artist}")
            print(f"{'='*60}")
            debug_song_features(song.feature_path)