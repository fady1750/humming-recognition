const ResultDisplay = ({ results }) => {
    if (!results) return null;

    const { best_match, top_matches } = results;

    return (
        <div className="results-container">
            <div className="best-match">
                <h2>🎯 Best Match</h2>
                <div className="match-card highlight">
                    <h3>{best_match.title}</h3>
                    <p className="artist">{best_match.artist}</p>
                    <div className="similarity-bar">
                        <div 
                            className="similarity-fill"
                            style={{ width: `${best_match.similarity}%` }}
                        ></div>
                    </div>
                    <p className="similarity-score">{best_match.similarity}% Match</p>
                    <div className="score-breakdown">
                        <span>Melody: {best_match.pitch_score}%</span>
                        <span>Pitch: {best_match.pitch_score}%</span>
                    </div>
                </div>
            </div>

            <div className="top-matches">
                <h3>Top 5 Matches</h3>
                {top_matches.map((match, index) => (
                    <div key={match.song_id} className="match-card">
                        <div className="rank">#{index + 1}</div>
                        <div className="match-info">
                            <h4>{match.title}</h4>
                            <p>{match.artist}</p>
                        </div>
                        <div className="match-score">{match.similarity}%</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ResultDisplay;