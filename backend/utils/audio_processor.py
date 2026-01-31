import librosa
import numpy as np
from scipy import signal

def load_audio(file_path, sr=16000):
    """Load audio file and convert to mono"""
    try:
        y, sr = librosa.load(file_path, sr=sr, mono=True)
        return y, sr
    except Exception as e:
        raise Exception(f"Error loading audio: {str(e)}")

def reduce_noise(y, sr):
    """Basic noise reduction using spectral gating"""
    # Simple noise reduction: high-pass filter
    sos = signal.butter(10, 100, 'hp', fs=sr, output='sos')
    filtered = signal.sosfilt(sos, y)
    return filtered

def normalize_audio(y):
    """Normalize audio to [-1, 1]"""
    if np.max(np.abs(y)) > 0:
        return y / np.max(np.abs(y))
    return y