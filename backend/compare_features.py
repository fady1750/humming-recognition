from utils.feature_extractor import FeatureExtractor
from utils.similarity import SimilarityMatcher
import numpy as np

def compare_same_song():
    """
    Extract features from Living Life song twice and compare
    Should get very high similarity (90%+)
    """
    extractor = FeatureExtractor(sr=16000)
    
    # Load the stored features
    stored_features = extractor.load_features('song_features/song_living_life_in_the_night.npy')
    
    print("="*60)
    print("Stored features for 'Living Life in the Night':")
    print("="*60)
    print(f"MFCC shape: {stored_features['mfcc'].shape}")
    print(f"Chroma shape: {stored_features['chroma'].shape}")
    print(f"Pitch shape: {stored_features['pitch'].shape}")
    print(f"Pitch non-zero: {np.count_nonzero(stored_features['pitch'])}/{len(stored_features['pitch'])}")
    print(f"Pitch mean: {np.mean(stored_features['pitch'][stored_features['pitch'] > 0]):.2f} Hz")
    print()
    
    # Check for abnormalities
    if np.all(stored_features['mfcc'] == 0):
        print("⚠️ WARNING: MFCC is all zeros!")
    if np.all(stored_features['chroma'] == 0):
        print("⚠️ WARNING: Chroma is all zeros!")
    if np.all(stored_features['pitch'] == 0):
        print("⚠️ WARNING: Pitch is all zeros!")
    
    # Compare with other songs
    print("\n" + "="*60)
    print("Comparing pitch ranges:")
    print("="*60)
    
    songs = [
        ('Senorita', 'song_features/song_senorita.npy'),
        ('Lake of Fire', 'song_features/song_lake_of_fire.npy'),
        ('Hope', 'song_features/song_hope.npy'),
        ('Living Life', 'song_features/song_living_life_in_the_night.npy')
    ]
    
    for name, path in songs:
        features = extractor.load_features(path)
        pitch = features['pitch']
        voiced_pitch = pitch[pitch > 0]
        
        if len(voiced_pitch) > 0:
            print(f"{name:20} - Pitch: {np.min(voiced_pitch):6.1f}Hz to {np.max(voiced_pitch):6.1f}Hz (mean: {np.mean(voiced_pitch):6.1f}Hz)")
        else:
            print(f"{name:20} - No voiced frames!")

if __name__ == "__main__":
    compare_same_song()