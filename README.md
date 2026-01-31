# 🎵 Humming Recognition System

A web-based application that recognizes songs from hummed melodies using advanced audio signal processing and machine learning techniques. Built as a university-level Digital Signal Processing (DSP) project.

![Project Banner](https://img.shields.io/badge/DSP-Project-blue) ![Python](https://img.shields.io/badge/Python-3.12-green) ![Flask](https://img.shields.io/badge/Flask-3.0-red) ![React](https://img.shields.io/badge/React-18-blue)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [Contributors](#contributors)
- [License](#license)

---

## 🎯 Overview

The Humming Recognition System allows users to hum a melody into their microphone, and the system identifies the song by comparing the hummed audio against a preprocessed song database. Unlike commercial solutions like Shazam, this system focuses on **melody recognition from humming** rather than audio fingerprinting.

### Key Highlights

- ✅ Real-time audio recording from browser
- ✅ Advanced feature extraction (MFCC, Chroma, Pitch)
- ✅ Dynamic Time Warping (DTW) for similarity matching
- ✅ Web-based interface with beautiful UI
- ✅ No external APIs - fully self-contained system
- ✅ University project suitable for DSP coursework

---

## ✨ Features

### Core Features

1. **Audio Recording**
   - Browser-based microphone recording
   - Supports 5-15 second humming clips
   - Real-time recording timer

2. **Feature Extraction**
   - **MFCC** (Mel-Frequency Cepstral Coefficients)
   - **Chroma** features for pitch class representation
   - **Pitch contour** (F0) tracking
   - Spectral centroid analysis

3. **Similarity Matching**
   - Dynamic Time Warping (DTW) algorithm
   - Multi-feature weighted comparison
   - Top 5 ranked results
   - Confidence scores for each match

4. **Song Database**
   - Offline feature preprocessing
   - Efficient .npy feature storage
   - SQLite database for metadata
   - Support for MP3, WAV, OGG formats

5. **User Interface**
   - Beautiful gradient design
   - Real-time server status
   - Visual similarity bars
   - Detailed score breakdown

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Audio      │  │   Results    │  │  Similarity  │     │
│  │  Recorder    │  │   Display    │  │    Scores    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                          │                                  │
│                    Axios (HTTP)                             │
└──────────────────────────┼──────────────────────────────────┘
                           │
                    REST API (JSON)
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    BACKEND (Flask)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              API Routes Layer                          │ │
│  │  /upload-humming  │  /songs  │  /health               │ │
│  └────────────────────────────────────────────────────────┘ │
│                           │                                 │
│  ┌────────────────────────▼───────────────────────┐        │
│  │         Audio Processing Pipeline              │        │
│  │  Upload → Format Conversion → Noise Reduction  │        │
│  │      ↓             ↓              ↓             │        │
│  │  Feature Extraction (MFCC, Chroma, Pitch)      │        │
│  └────────────────────────────────────────────────┘        │
│                           │                                 │
│  ┌────────────────────────▼───────────────────────┐        │
│  │          Similarity Computation                │        │
│  │   DTW Algorithm  │  Weighted Scoring           │        │
│  │   (50% Pitch, 30% MFCC, 20% Chroma)           │        │
│  └────────────────────────────────────────────────┘        │
│                           │                                 │
│  ┌────────────────────────▼───────────────────────┐        │
│  │       Database Layer (SQLAlchemy)              │        │
│  │   Songs Metadata  │  Feature Files (.npy)      │        │
│  └────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technologies Used

### Backend

- **Python 3.12** - Core programming language
- **Flask** - Web framework
- **librosa** - Audio analysis and feature extraction
- **numpy** - Numerical computing
- **scipy** - Scientific computing and signal processing
- **fastdtw** - Dynamic Time Warping implementation
- **SQLAlchemy** - Database ORM
- **pydub** - Audio format conversion
- **soundfile** - Audio I/O
- **FFmpeg** - Audio codec support

### Frontend

- **React 18** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **HTML5 MediaRecorder API** - Audio recording

### Database

- **SQLite** - Lightweight relational database
- **NumPy binary format (.npy)** - Feature storage

---

## 📦 Installation

### Prerequisites

- **Python 3.12+**
- **Node.js 18+** and npm
- **FFmpeg** (for audio format conversion)
- **Git**

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/humming-recognition.git
cd humming-recognition
```

### Step 2: Install FFmpeg

#### Windows:

1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to System PATH

#### macOS:

```bash
brew install ffmpeg
```

#### Linux:

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

### Step 3: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install flask flask-cors librosa numpy scipy scikit-learn sqlalchemy fastdtw soundfile audioread pydub

# Initialize database
python setup.py

# Verify setup
python verify_setup.py
```

### Step 4: Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Install axios
npm install axios
```

### Step 5: Add Songs to Database

```bash
cd ../backend
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Add a song (example)
python add_song.py "path/to/song.mp3" "Song Title" "Artist Name"

# Or generate test songs
python generate_test_song.py

# List songs
python list_songs.py
```

---

## 🚀 Usage

### Start the Backend Server

```bash
cd backend
.\venv\Scripts\Activate  # Windows
# source venv/bin/activate  # macOS/Linux

python run.py
```

Backend will run on: `http://localhost:5000`

### Start the Frontend Development Server

Open a **new terminal**:

```bash
cd frontend
npm run dev
```

Frontend will run on: `http://localhost:5173`

### Using the Application

1. Open browser and navigate to `http://localhost:5173`
2. Check that "Server: online" is displayed
3. Click **"Start Recording"**
4. Hum a melody for 5-10 seconds
5. Click **"Stop Recording"**
6. Wait for results (typically 2-5 seconds)
7. View the best match and top 5 similar songs

---

## 🔬 How It Works

### 1. Feature Extraction Pipeline

```python
Audio Input (WebM/WAV)
    ↓
Format Conversion (16kHz, Mono)
    ↓
Noise Reduction (High-pass filter @ 100Hz)
    ↓
Normalization
    ↓
Feature Extraction:
    ├─ MFCC (13 coefficients + deltas)
    ├─ Chroma (12 pitch classes)
    └─ Pitch Contour (F0 via PYIN algorithm)
    ↓
Feature Vector Storage
```

### 2. Similarity Calculation

**Dynamic Time Warping (DTW)** is used to compare sequences of different lengths:

```python
# Weighted similarity formula
Total_Similarity = 0.5 × Pitch_Score
                 + 0.3 × MFCC_Score
                 + 0.2 × Chroma_Score

# Individual scores calculated via DTW
DTW_Distance = fastdtw(sequence1, sequence2)
Similarity = 100 × (1 - normalized_distance)
```

**Why these weights?**

- **Pitch (50%)**: Most important for melody recognition
- **MFCC (30%)**: Captures timbral characteristics
- **Chroma (20%)**: Provides key/chord information

### 3. Database Schema

```sql
CREATE TABLE songs (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    duration FLOAT,
    feature_path TEXT  -- Path to .npy file
);
```

Feature files stored as NumPy arrays:

```python
{
    'mfcc': ndarray(26, time_steps),
    'chroma': ndarray(12, time_steps),
    'pitch': ndarray(time_steps),
    'voiced_probs': ndarray(time_steps),
    'spectral_centroid': ndarray(1, time_steps)
}
```

---

## 📁 Project Structure

```
humming-recognition/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app initialization
│   │   ├── config.py            # Configuration settings
│   │   └── routes.py            # API endpoints
│   ├── models/
│   │   └── database.py          # Database models
│   ├── utils/
│   │   ├── audio_processor.py   # Audio loading & preprocessing
│   │   ├── feature_extractor.py # Feature extraction
│   │   └── similarity.py        # DTW & similarity matching
│   ├── database/
│   │   └── songs.db             # SQLite database
│   ├── song_features/           # Stored .npy feature files
│   ├── uploads/                 # Temporary upload directory
│   ├── run.py                   # Server entry point
│   ├── add_song.py              # Script to add songs
│   ├── list_songs.py            # List database contents
│   ├── setup.py                 # Project setup script
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioRecorder.jsx    # Recording component
│   │   │   └── ResultDisplay.jsx    # Results UI
│   │   ├── services/
│   │   │   └── api.js               # API client
│   │   ├── App.jsx                  # Main app component
│   │   ├── App.css                  # Styling
│   │   └── main.jsx                 # Entry point
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 📡 API Documentation

### Base URL

```
http://localhost:5000/api
```

### Endpoints

#### 1. Health Check

```http
GET /health
```

**Response:**

```json
{
  "status": "healthy",
  "message": "API is running"
}
```

---

#### 2. Get All Songs

```http
GET /songs
```

**Response:**

```json
{
  "songs": [
    {
      "id": 1,
      "title": "Song Title",
      "artist": "Artist Name",
      "duration": 180.5
    }
  ],
  "count": 1
}
```

---

#### 3. Upload Humming

```http
POST /upload-humming
Content-Type: multipart/form-data
```

**Request:**

- `audio`: Audio file (WAV, WebM, MP3, OGG)

**Response:**

```json
{
  "success": true,
  "best_match": {
    "song_id": 1,
    "title": "Song Title",
    "artist": "Artist Name",
    "similarity": 78.5,
    "pitch_score": 82.3,
    "mfcc_score": 75.2,
    "chroma_score": 68.9
  },
  "top_matches": [
    {
      "song_id": 1,
      "title": "Song Title",
      "artist": "Artist Name",
      "similarity": 78.5,
      "pitch_score": 82.3,
      "mfcc_score": 75.2,
      "chroma_score": 68.9
    }
  ]
}
```

---

#### 4. Get Song Details

```http
GET /match-results/{song_id}
```

**Response:**

```json
{
  "id": 1,
  "title": "Song Title",
  "artist": "Artist Name",
  "duration": 180.5
}
```

---

## 🐛 Troubleshooting

### Issue: "FFmpeg not found"

**Solution:**

1. Verify FFmpeg installation: `ffmpeg -version`
2. Ensure FFmpeg is in system PATH
3. Restart terminal after PATH changes
4. Check `backend/app/__init__.py` for manual FFmpeg path configuration

---

### Issue: "MFCC and Chroma scores are 0%"

**Solution:**

1. Update `backend/utils/similarity.py` with the corrected DTW normalization
2. Restart backend server
3. Clear Python cache: `Remove-Item -Recurse utils\__pycache__`

---

### Issue: "No songs in database"

**Solution:**

```bash
cd backend
python list_songs.py  # Check current songs
python add_song.py "path/to/song.mp3" "Title" "Artist"
```

---

### Issue: "Audio conversion failed"

**Solution:**

1. Install missing codecs: `pip install soundfile audioread pydub`
2. Verify FFmpeg is working: `ffmpeg -version`
3. Check backend logs for detailed error

---

### Issue: "Server: offline" in frontend

**Solution:**

1. Verify backend is running on port 5000
2. Check CORS configuration in `backend/app/__init__.py`
3. Test API directly: `curl http://localhost:5000/api/health`

---

## 🚀 Future Improvements

### Accuracy Enhancements

- [ ] Implement key normalization (transpose to common key)
- [ ] Add tempo-invariant matching
- [ ] Use Siamese Neural Networks for better matching
- [ ] Integrate vocal separation for better melody extraction

### Features

- [ ] User accounts and history
- [ ] Real-time waveform visualization
- [ ] Confidence threshold filtering
- [ ] Support for longer recordings (up to 30 seconds)
- [ ] Mobile app (React Native)

### Performance

- [ ] GPU acceleration for feature extraction
- [ ] Caching of song features in memory
- [ ] Parallel processing for multiple song comparisons
- [ ] PostgreSQL for production database

### UI/UX

- [ ] Dark mode toggle
- [ ] Audio playback of matched songs
- [ ] Share results on social media
- [ ] Tutorial/onboarding flow

---

## 👥 Contributors

- **Your Name** - _Project Lead & Developer_ - [GitHub](https://github.com/yourusername)
- **Course:** Digital Signal Processing (DSP)
- **Institution:** [Your University Name]
- **Year:** 2025/2026

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **librosa** team for excellent audio processing tools
- **FastDTW** for efficient DTW implementation
- **Flask** and **React** communities
- Course instructors and teaching assistants
- Open-source DSP community

---

## 📚 References

1. Müller, M. (2015). _Fundamentals of Music Processing_. Springer.
2. McFee, B., et al. (2015). librosa: Audio and Music Signal Analysis in Python.
3. Salvador, S., & Chan, P. (2007). FastDTW: Toward Accurate Dynamic Time Warping in Linear Time and Space.
4. Wang, A. (2003). An Industrial-Strength Audio Search Algorithm. _ISMIR_.

---

## 📞 Contact

For questions, issues, or contributions:

- **Email:** your.email@university.edu
- **GitHub Issues:** [Create an issue](https://github.com/yourusername/humming-recognition/issues)
- **Project Link:** [https://github.com/yourusername/humming-recognition](https://github.com/yourusername/humming-recognition)

---

**Made with ❤️ for DSP Course Project**

_Last Updated: January 2026_
