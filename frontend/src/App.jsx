import { useState, useEffect } from 'react';
import AudioRecorder from './components/AudioRecorder';
import ResultDisplay from './components/ResultDisplay';
import { uploadHumming, getSongs, healthCheck } from './services/api';
import './App.css';

function App() {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [songCount, setSongCount] = useState(0);
    const [serverStatus, setServerStatus] = useState('checking...');

    useEffect(() => {
        // Check server health
        healthCheck()
            .then(() => setServerStatus('online'))
            .catch(() => setServerStatus('offline'));
        
        // Get song count
        getSongs()
            .then(data => setSongCount(data.count))
            .catch(() => setSongCount(0));
    }, []);

    const handleRecordingComplete = async (audioBlob) => {
        setLoading(true);
        setError(null);
        setResults(null);

        try {
            const data = await uploadHumming(audioBlob);
            setResults(data);
        } catch (err) {
            setError(err.toString());
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app">
            <header>
                <h1>🎵 Humming Recognition System</h1>
                <p>Hum a melody and find the song!</p>
                <div className="status-bar">
                    <span className={`status ${serverStatus === 'online' ? 'online' : 'offline'}`}>
                        Server: {serverStatus}
                    </span>
                    <span className="song-count">Database: {songCount} songs</span>
                </div>
            </header>

            <main>
                <AudioRecorder onRecordingComplete={handleRecordingComplete} />

                {loading && (
                    <div className="loading">
                        <div className="spinner"></div>
                        <p>Analyzing your humming...</p>
                    </div>
                )}

                {error && (
                    <div className="error">
                        <p>❌ Error: {error}</p>
                    </div>
                )}

                <ResultDisplay results={results} />
            </main>
        </div>
    );
}

export default App;