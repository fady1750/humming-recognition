from flask import Blueprint, request, jsonify
import os
import librosa
import soundfile as sf
from werkzeug.utils import secure_filename
from utils.feature_extractor import FeatureExtractor
from utils.similarity import SimilarityMatcher
from models.database import get_all_songs, get_song_by_id
import numpy as np

api = Blueprint('api', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'API is running'}), 200

@api.route('/songs', methods=['GET'])
def get_songs():
    """Get all songs in database"""
    try:
        songs = get_all_songs()
        songs_list = [
            {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'duration': song.duration
            }
            for song in songs
        ]
        return jsonify({'songs': songs_list, 'count': len(songs_list)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/upload-humming', methods=['POST'])
def upload_humming():
    """
    Main endpoint: Upload humming audio and find matches
    """
    import traceback
    
    try:
        print("\n" + "="*60)
        print("🎤 NEW HUMMING UPLOAD REQUEST")
        print("="*60)
        
        # Check if file is present
        if 'audio' not in request.files:
            print("❌ No audio file in request")
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            print("❌ Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"📁 Original filename: {file.filename}")
        print(f"📁 Content type: {file.content_type}")
        
        # Save uploaded file with original extension
        filename = secure_filename(file.filename)
        if not filename:
            filename = "recording.webm"  # Default for browser recordings
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        file_size = os.path.getsize(filepath)
        print(f"✅ File saved: {filepath} ({file_size} bytes)")
        
        # Always convert to WAV for processing
        wav_path = os.path.join(UPLOAD_FOLDER, "processed_audio.wav")
        
        print(f"🔄 Converting to WAV...")
        
        try:
            # Method 1: Try pydub with FFmpeg (best for webm/ogg/mp3)
            from pydub import AudioSegment
            
            print("   Trying pydub conversion...")
            audio = AudioSegment.from_file(filepath)
            audio = audio.set_frame_rate(16000).set_channels(1)
            audio.export(wav_path, format='wav')
            print(f"   ✅ Converted with pydub")
            
        except Exception as e1:
            print(f"   ⚠️ Pydub failed: {e1}")
            
            try:
                # Method 2: Try librosa (fallback)
                print("   Trying librosa conversion...")
                y, sr = librosa.load(filepath, sr=16000, mono=True)
                sf.write(wav_path, y, sr)
                print(f"   ✅ Converted with librosa")
                
            except Exception as e2:
                print(f"   ❌ Librosa also failed: {e2}")
                print(f"\n{'='*60}")
                print("❌ AUDIO CONVERSION FAILED")
                print("="*60)
                print("FFmpeg might not be properly configured.")
                print("Error details:")
                print(f"  Pydub error: {e1}")
                print(f"  Librosa error: {e2}")
                print("="*60 + "\n")
                
                # Clean up
                try:
                    os.remove(filepath)
                except:
                    pass
                
                return jsonify({
                    'error': 'Audio conversion failed. Please check server logs.'
                }), 500
        
        # Clean up original file
        try:
            os.remove(filepath)
        except:
            pass
        
        filepath = wav_path
        
        # Extract features from humming
        print(f"🎵 Extracting features...")
        extractor = FeatureExtractor(sr=16000)
        
        try:
            humming_features = extractor.extract_features(filepath)
            print(f"✅ Features extracted successfully")
            print(f"   - MFCC shape: {humming_features['mfcc'].shape}")
            print(f"   - Chroma shape: {humming_features['chroma'].shape}")
            print(f"   - Pitch shape: {humming_features['pitch'].shape}")
        except Exception as e:
            print(f"❌ Feature extraction error: {e}")
            traceback.print_exc()
            
            # Clean up
            try:
                os.remove(filepath)
            except:
                pass
            
            return jsonify({'error': f'Feature extraction failed: {str(e)}'}), 500
        
        # Get all songs and compare
        songs = get_all_songs()
        
        if len(songs) == 0:
            print("⚠️ No songs in database")
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': 'No songs in database. Please add songs first.'}), 400
        
        print(f"📚 Comparing with {len(songs)} songs...")
        matcher = SimilarityMatcher()
        
        results = []
        
        for song in songs:
            try:
                # Load song features
                song_features = extractor.load_features(song.feature_path)
                
                # Calculate similarity
                total_score, individual_scores = matcher.combined_similarity(
                    humming_features, 
                    song_features
                )
                
                results.append({
                    'song_id': song.id,
                    'title': song.title,
                    'artist': song.artist,
                    'similarity': round(total_score, 2),
                    'pitch_score': round(individual_scores['pitch'], 2),
                    'mfcc_score': round(individual_scores['mfcc'], 2),
                    'chroma_score': round(individual_scores['chroma'], 2)
                })
                
                print(f"   - {song.title}: {total_score:.2f}%")
                
            except Exception as e:
                print(f"⚠️ Error comparing with song {song.title}: {e}")
                continue
        
        if len(results) == 0:
            print("❌ Could not compare with any songs")
            try:
                os.remove(filepath)
            except:
                pass
            return jsonify({'error': 'Could not compare with any songs'}), 500
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Get top 5
        top_matches = results[:5]
        best_match = results[0] if results else None
        
        print(f"\n🎯 BEST MATCH: {best_match['title']} by {best_match['artist']}")
        print(f"   Similarity: {best_match['similarity']}%")
        print(f"   Pitch: {best_match['pitch_score']}% | MFCC: {best_match['mfcc_score']}% | Chroma: {best_match['chroma_score']}%")
        print("="*60 + "\n")
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify({
            'success': True,
            'best_match': best_match,
            'top_matches': top_matches
        }), 200
        
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        traceback.print_exc()
        print("="*60 + "\n")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@api.route('/match-results/<int:song_id>', methods=['GET'])
def get_match_details(song_id):
    """Get detailed information about a matched song"""
    try:
        song = get_song_by_id(song_id)
        if not song:
            return jsonify({'error': 'Song not found'}), 404
        
        return jsonify({
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'duration': song.duration
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500