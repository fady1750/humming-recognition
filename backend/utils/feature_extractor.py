import librosa
import numpy as np
from utils.audio_processor import load_audio, reduce_noise, normalize_audio

class FeatureExtractor:
    def __init__(self, sr=16000, n_mfcc=13, n_chroma=12):
        self.sr = sr
        self.n_mfcc = n_mfcc
        self.n_chroma = n_chroma
    
    def extract_features(self, audio_path):
        """
        Extract MFCC, Chroma, and Pitch features from audio
        Returns a dictionary with all features
        """
        # Load and preprocess audio
        y, sr = load_audio(audio_path, sr=self.sr)
        y = reduce_noise(y, sr)
        y = normalize_audio(y)
        
        features = {}
        
        # 1. MFCC (Mel-frequency cepstral coefficients)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=self.n_mfcc)
        mfcc_delta = librosa.feature.delta(mfcc)
        features['mfcc'] = np.concatenate([mfcc, mfcc_delta], axis=0)
        
        # 2. Chroma features
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=self.n_chroma)
        features['chroma'] = chroma
        
        # 3. Pitch contour (F0 - fundamental frequency)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, 
            fmin=librosa.note_to_hz('C2'),
            fmax=librosa.note_to_hz('C7'),
            sr=sr
        )
        # Replace NaN with 0 and normalize
        f0 = np.nan_to_num(f0)
        features['pitch'] = f0
        features['voiced_probs'] = voiced_probs
        
        # 4. Spectral features (bonus)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        features['spectral_centroid'] = spectral_centroid
        
        return features
    
    def save_features(self, features, output_path):
        """Save features to .npy file"""
        np.save(output_path, features, allow_pickle=True)
    
    def load_features(self, feature_path):
        """Load features from .npy file"""
        return np.load(feature_path, allow_pickle=True).item()