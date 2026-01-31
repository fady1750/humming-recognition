import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean, cosine

class SimilarityMatcher:
    def __init__(self):
        pass
    
    def dtw_distance(self, seq1, seq2):
        """
        Calculate Dynamic Time Warping distance
        Lower distance = more similar
        """
        # Ensure both sequences are 2D
        if len(seq1.shape) == 1:
            seq1 = seq1.reshape(-1, 1)
        if len(seq2.shape) == 1:
            seq2 = seq2.reshape(-1, 1)
        
        # Transpose so time is first dimension
        if seq1.shape[0] < seq1.shape[1]:
            seq1 = seq1.T
        if seq2.shape[0] < seq2.shape[1]:
            seq2 = seq2.T
        
        distance, path = fastdtw(seq1, seq2, dist=euclidean)
        return distance
    
    def pitch_similarity(self, pitch1, pitch2):
        """
        Compare pitch contours using DTW
        Focuses only on melody line
        """
        # Remove zeros (unvoiced regions)
        p1 = pitch1[pitch1 > 0]
        p2 = pitch2[pitch2 > 0]
        
        if len(p1) < 10 or len(p2) < 10:
            print(f"    ⚠️ Insufficient voiced frames: p1={len(p1)}, p2={len(p2)}")
            return 0.0
        
        # Normalize pitch to same range (key-invariant)
        p1_norm = (p1 - np.min(p1)) / (np.max(p1) - np.min(p1) + 1e-8)
        p2_norm = (p2 - np.min(p2)) / (np.max(p2) - np.min(p2) + 1e-8)
        
        # DTW distance
        distance, _ = fastdtw(p1_norm.reshape(-1, 1), p2_norm.reshape(-1, 1), dist=euclidean)
        
        # Convert distance to similarity score (0-100)
        # Normalize by the average length
        avg_length = (len(p1_norm) + len(p2_norm)) / 2
        normalized_distance = distance / avg_length
        
        # Convert to similarity (inverse relationship)
        # Distance of 0 = 100% similarity, distance of 2 = 0% similarity
        similarity = max(0, 100 * (1 - min(normalized_distance / 2, 1)))
        
        return similarity
    
    def mfcc_similarity(self, mfcc1, mfcc2):
        """Compare MFCC features using DTW"""
        try:
            # Ensure proper shape (features x time)
            if mfcc1.shape[0] > mfcc1.shape[1]:
                mfcc1 = mfcc1.T
            if mfcc2.shape[0] > mfcc2.shape[1]:
                mfcc2 = mfcc2.T
            
            # Subsample if sequences are very long (for speed)
            max_length = 500
            if mfcc1.shape[1] > max_length:
                step = mfcc1.shape[1] // max_length
                mfcc1 = mfcc1[:, ::step]
            if mfcc2.shape[1] > max_length:
                step = mfcc2.shape[1] // max_length
                mfcc2 = mfcc2[:, ::step]
            
            # Calculate DTW distance
            distance = self.dtw_distance(mfcc1, mfcc2)
            
            # Normalize by number of features and average length
            avg_length = (mfcc1.shape[1] + mfcc2.shape[1]) / 2
            num_features = mfcc1.shape[0]
            
            normalized_distance = distance / (avg_length * num_features)
            
            # Convert to similarity score (0-100)
            # Empirically, MFCC distances range from 0 to ~10
            similarity = max(0, 100 * (1 - min(normalized_distance / 10, 1)))
            
            return similarity
            
        except Exception as e:
            print(f"    ⚠️ MFCC similarity error: {e}")
            return 0.0
    
    def chroma_similarity(self, chroma1, chroma2):
        """Compare chroma features using DTW"""
        try:
            # Ensure proper shape (features x time)
            if chroma1.shape[0] > chroma1.shape[1]:
                chroma1 = chroma1.T
            if chroma2.shape[0] > chroma2.shape[1]:
                chroma2 = chroma2.T
            
            # Subsample if sequences are very long
            max_length = 500
            if chroma1.shape[1] > max_length:
                step = chroma1.shape[1] // max_length
                chroma1 = chroma1[:, ::step]
            if chroma2.shape[1] > max_length:
                step = chroma2.shape[1] // max_length
                chroma2 = chroma2[:, ::step]
            
            # Calculate DTW distance
            distance = self.dtw_distance(chroma1, chroma2)
            
            # Normalize
            avg_length = (chroma1.shape[1] + chroma2.shape[1]) / 2
            num_features = chroma1.shape[0]
            
            normalized_distance = distance / (avg_length * num_features)
            
            # Convert to similarity (chroma distances typically 0-5)
            similarity = max(0, 100 * (1 - min(normalized_distance / 5, 1)))
            
            return similarity
            
        except Exception as e:
            print(f"    ⚠️ Chroma similarity error: {e}")
            return 0.0
    
    def combined_similarity(self, features1, features2, weights=None):
        """
        Combine multiple similarity metrics with weights
        
        weights: dict with keys 'pitch', 'mfcc', 'chroma'
        """
        if weights is None:
            weights = {
                'pitch': 0.5,    # Pitch is most important for humming
                'mfcc': 0.3,
                'chroma': 0.2
            }
        
        scores = {}
        
        # Calculate individual scores with error handling
        try:
            scores['pitch'] = self.pitch_similarity(
                features1['pitch'], 
                features2['pitch']
            )
        except Exception as e:
            print(f"    ⚠️ Pitch similarity error: {e}")
            scores['pitch'] = 0.0
        
        try:
            scores['mfcc'] = self.mfcc_similarity(
                features1['mfcc'], 
                features2['mfcc']
            )
        except Exception as e:
            print(f"    ⚠️ MFCC similarity error: {e}")
            scores['mfcc'] = 0.0
        
        try:
            scores['chroma'] = self.chroma_similarity(
                features1['chroma'], 
                features2['chroma']
            )
        except Exception as e:
            print(f"    ⚠️ Chroma similarity error: {e}")
            scores['chroma'] = 0.0
        
        # Debug output
        print(f"    Individual scores: Pitch={scores['pitch']:.2f}%, MFCC={scores['mfcc']:.2f}%, Chroma={scores['chroma']:.2f}%")
        
        # Weighted average
        total_score = sum(scores[key] * weights[key] for key in weights)
        
        return total_score, scores