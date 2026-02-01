import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean, cosine

class SimilarityMatcher:
    def __init__(self):
        pass
    
    def normalize_pitch_to_key(self, pitch):
        """
        Normalize pitch contour to be key-invariant
        Converts to relative pitch (semitones from median)
        """
        # Remove unvoiced frames
        voiced_pitch = pitch[pitch > 0]
        
        if len(voiced_pitch) < 10:
            return pitch
        
        # Use median as reference (more robust than mean)
        reference = np.median(voiced_pitch)
        
        if reference == 0:
            return pitch
        
        # Convert to semitones relative to reference
        pitch_normalized = np.zeros_like(pitch)
        pitch_normalized[pitch > 0] = 12 * np.log2(pitch[pitch > 0] / reference)
        
        return pitch_normalized
    
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
        Key-invariant comparison using relative pitch
        """
        # Normalize to be key-invariant
        p1_norm = self.normalize_pitch_to_key(pitch1)
        p2_norm = self.normalize_pitch_to_key(pitch2)
        
        # Remove zeros (unvoiced regions)
        p1 = p1_norm[p1_norm != 0]
        p2 = p2_norm[p2_norm != 0]
        
        if len(p1) < 10 or len(p2) < 10:
            print(f"    ⚠️ Insufficient voiced frames: p1={len(p1)}, p2={len(p2)}")
            return 0.0
        
        # Normalize to [0, 1] range
        p1_min, p1_max = np.min(p1), np.max(p1)
        p2_min, p2_max = np.min(p2), np.max(p2)
        
        if (p1_max - p1_min) > 1e-8:
            p1 = (p1 - p1_min) / (p1_max - p1_min)
        else:
            p1 = np.zeros_like(p1)
            
        if (p2_max - p2_min) > 1e-8:
            p2 = (p2 - p2_min) / (p2_max - p2_min)
        else:
            p2 = np.zeros_like(p2)
        
        # DTW distance
        distance, _ = fastdtw(p1.reshape(-1, 1), p2.reshape(-1, 1), dist=euclidean)
        
        # Convert distance to similarity score (0-100)
        avg_length = (len(p1) + len(p2)) / 2
        normalized_distance = distance / avg_length
        
        # Convert to similarity
        similarity = max(0, 100 * (1 - min(normalized_distance / 1.2, 1)))
        
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
                step = max(1, mfcc1.shape[1] // max_length)
                mfcc1 = mfcc1[:, ::step]
            if mfcc2.shape[1] > max_length:
                step = max(1, mfcc2.shape[1] // max_length)
                mfcc2 = mfcc2[:, ::step]

            # Calculate DTW distance
            distance = self.dtw_distance(mfcc1, mfcc2)

            # Normalize by number of features and average length
            avg_length = (mfcc1.shape[1] + mfcc2.shape[1]) / 2
            num_features = mfcc1.shape[0]

            normalized_distance = distance / (avg_length * num_features)

            # Convert to similarity score (0-100)
            # Empirically calibrated thresholds:
            # Best match (same song): 6.0-6.5 → 80-100%
            # Good match: 6.5-7.0 → 50-80%
            # Weak match: 7.0-7.5 → 20-50%
            # Poor match: 7.5+ → 0-20%

            if normalized_distance <= 6.0:
                similarity = 100
            elif normalized_distance <= 6.5:
                # Scale 100% to 80%
                similarity = 100 - (normalized_distance - 6.0) * 40
            elif normalized_distance <= 7.0:
                # Scale 80% to 50%
                similarity = 80 - (normalized_distance - 6.5) * 60
            elif normalized_distance <= 7.5:
                # Scale 50% to 20%
                similarity = 50 - (normalized_distance - 7.0) * 60
            elif normalized_distance <= 8.0:
                # Scale 20% to 0%
                similarity = 20 - (normalized_distance - 7.5) * 40
            else:
                similarity = 0

            similarity = max(0, min(100, similarity))

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
                step = max(1, chroma1.shape[1] // max_length)
                chroma1 = chroma1[:, ::step]
            if chroma2.shape[1] > max_length:
                step = max(1, chroma2.shape[1] // max_length)
                chroma2 = chroma2[:, ::step]
            
            # Calculate DTW distance
            distance = self.dtw_distance(chroma1, chroma2)
            
            # Normalize
            avg_length = (chroma1.shape[1] + chroma2.shape[1]) / 2
            num_features = chroma1.shape[0]
            
            normalized_distance = distance / (avg_length * num_features)
            
            # Convert to similarity
            similarity = max(0, 100 * (1 - min(normalized_distance / 3, 1)))
            
            return similarity
            
        except Exception as e:
            print(f"    ⚠️ Chroma similarity error: {e}")
            return 0.0
    
    def melody_contour_similarity(self, pitch1, pitch2):
        """
        Compare melody contour direction (up, down, same)
        """
        # Get voiced regions
        p1 = pitch1[pitch1 > 0]
        p2 = pitch2[pitch2 > 0]
        
        if len(p1) < 3 or len(p2) < 3:
            return 0.0
        
        # Calculate pitch differences (contour)
        contour1 = np.diff(p1)
        contour2 = np.diff(p2)
        
        # Normalize
        if np.std(contour1) > 0:
            contour1 = contour1 / np.std(contour1)
        if np.std(contour2) > 0:
            contour2 = contour2 / np.std(contour2)
        
        # DTW on contours
        try:
            distance, _ = fastdtw(
                contour1.reshape(-1, 1), 
                contour2.reshape(-1, 1),
                dist=euclidean
            )
            
            avg_length = (len(contour1) + len(contour2)) / 2
            normalized_distance = distance / avg_length
            
            similarity = max(0, 100 * (1 - min(normalized_distance / 2, 1)))
            return similarity
        except:
            return 0.0
    
    def combined_similarity(self, features1, features2, weights=None):
        """
        Combine multiple similarity metrics with weights
        """
        if weights is None:
            weights = {
                'pitch': 0.60,      # Increased pitch weight
                'contour': 0.30,    # Melody shape
                'mfcc': 0.07,       # Reduced MFCC weight
                'chroma': 0.03      # Harmony
            }
        
        scores = {}
        
        # Calculate individual scores with error handling
        print(f"\n    [SIMILARITY] Computing scores...")
        
        try:
            scores['pitch'] = self.pitch_similarity(
                features1['pitch'], 
                features2['pitch']
            )
            print(f"    [SIMILARITY] Pitch: {scores['pitch']:.2f}%")
        except Exception as e:
            print(f"    ⚠️ Pitch similarity error: {e}")
            scores['pitch'] = 0.0
        
        try:
            scores['contour'] = self.melody_contour_similarity(
                features1['pitch'],
                features2['pitch']
            )
            print(f"    [SIMILARITY] Contour: {scores['contour']:.2f}%")
        except Exception as e:
            print(f"    ⚠️ Contour similarity error: {e}")
            scores['contour'] = 0.0
        
        print(f"\n    [SIMILARITY] Starting MFCC comparison...")
        try:
            scores['mfcc'] = self.mfcc_similarity(
                features1['mfcc'], 
                features2['mfcc']
            )
            print(f"    [SIMILARITY] MFCC: {scores['mfcc']:.2f}%")
        except Exception as e:
            print(f"    ⚠️ MFCC similarity error: {e}")
            import traceback
            traceback.print_exc()
            scores['mfcc'] = 0.0
        
        try:
            scores['chroma'] = self.chroma_similarity(
                features1['chroma'], 
                features2['chroma']
            )
            print(f"    [SIMILARITY] Chroma: {scores['chroma']:.2f}%")
        except Exception as e:
            print(f"    ⚠️ Chroma similarity error: {e}")
            scores['chroma'] = 0.0
        
        # Weighted average
        total_score = sum(scores[key] * weights[key] for key in weights)
        
        print(f"    [SIMILARITY] Total Score: {total_score:.2f}%\n")
        
        # Return only the scores that are displayed
        display_scores = {
            'pitch': scores['pitch'],
            'mfcc': scores['mfcc'],
            'chroma': scores['chroma']
        }
        
        return total_score, display_scores