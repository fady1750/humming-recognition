import numpy as np
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

class SimilarityMatcher:
    def __init__(self):
        pass
    
    def pitch_to_relative(self, pitch):
        """
        Convert absolute pitch to RELATIVE intervals (Google Hum style)
        This makes it KEY-INVARIANT and TEMPO-INVARIANT
        """
        # Remove unvoiced frames
        voiced_pitch = pitch[pitch > 0]
        
        if len(voiced_pitch) < 5:
            return np.array([])
        
        # Convert to semitones (log scale)
        semitones = 12 * np.log2(voiced_pitch / 440.0)  # Relative to A4
        
        # Calculate intervals (differences between consecutive notes)
        intervals = np.diff(semitones)
        
        # Normalize by standard deviation (tempo invariance)
        if np.std(intervals) > 0:
            intervals = intervals / np.std(intervals)
        
        return intervals
    
    def melody_contour(self, pitch):
        """
        Extract melody contour (shape): UP, DOWN, SAME
        """
        intervals = self.pitch_to_relative(pitch)
        
        if len(intervals) == 0:
            return np.array([])
        
        # Quantize to: -1 (down), 0 (same), +1 (up)
        threshold = 0.2
        contour = np.zeros_like(intervals)
        contour[intervals > threshold] = 1   # UP
        contour[intervals < -threshold] = -1  # DOWN
        # contour[abs(intervals) <= threshold] = 0  # SAME (already 0)
        
        return contour
    
    def pitch_similarity(self, pitch1, pitch2):
        """
        Compare melodies using RELATIVE PITCH (Google Hum approach)
        """
        # Convert to relative intervals
        intervals1 = self.pitch_to_relative(pitch1)
        intervals2 = self.pitch_to_relative(pitch2)
        
        if len(intervals1) < 5 or len(intervals2) < 5:
            return 0.0
        
        # DTW on intervals
        try:
            distance, _ = fastdtw(
                intervals1.reshape(-1, 1),
                intervals2.reshape(-1, 1),
                dist=euclidean
            )
            
            # Normalize
            avg_length = (len(intervals1) + len(intervals2)) / 2
            normalized_distance = distance / avg_length
            
            # Convert to similarity (0-100)
            similarity = max(0, 100 * (1 - min(normalized_distance / 2.0, 1)))
            
            return similarity
        except:
            return 0.0
    
    def contour_similarity(self, pitch1, pitch2):
        """
        Compare melody SHAPE (up/down/same pattern)
        """
        contour1 = self.melody_contour(pitch1)
        contour2 = self.melody_contour(pitch2)
        
        if len(contour1) < 5 or len(contour2) < 5:
            return 0.0
        
        try:
            distance, _ = fastdtw(
                contour1.reshape(-1, 1),
                contour2.reshape(-1, 1),
                dist=euclidean
            )
            
            avg_length = (len(contour1) + len(contour2)) / 2
            normalized_distance = distance / avg_length
            
            similarity = max(0, 100 * (1 - min(normalized_distance / 1.5, 1)))
            
            return similarity
        except:
            return 0.0
    
    def combined_similarity(self, features1, features2, weights=None):
        """
        MELODY-ONLY MATCHING (Google Hum approach)
        Only uses PITCH - ignores MFCC/Chroma
        """
        if weights is None:
            weights = {
                'pitch': 0.80,     # Relative pitch intervals
                'contour': 0.20,   # Melody shape
            }
        
        scores = {}
        
        # Calculate pitch similarity (relative)
        try:
            scores['pitch'] = self.pitch_similarity(
                features1['pitch'],
                features2['pitch']
            )
        except Exception as e:
            print(f"    ⚠️ Pitch error: {e}")
            scores['pitch'] = 0.0
        
        # Calculate contour similarity (shape)
        try:
            scores['contour'] = self.contour_similarity(
                features1['pitch'],
                features2['pitch']
            )
        except Exception as e:
            print(f"    ⚠️ Contour error: {e}")
            scores['contour'] = 0.0
        
        print(f"    Pitch (intervals): {scores['pitch']:.1f}% | Contour (shape): {scores['contour']:.1f}%")
        
        # Weighted average
        total_score = (
            scores['pitch'] * weights['pitch'] +
            scores['contour'] * weights['contour']
        )
        
        # Return dummy MFCC/Chroma for display compatibility
        display_scores = {
            'pitch': scores['pitch'],
            'mfcc': 0.0,  # Not used anymore
            'chroma': 0.0  # Not used anymore
        }
        
        return total_score, display_scores