import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import PredictorCard from './components/PredictorCard';
import WinGauge from './components/WinGauge';
import ReplaySimulator from './components/ReplaySimulator';
import { fetchMetadata, predictWinProbability } from './api';

export default function App() {
  const [activeMode, setActiveMode] = useState('live'); // 'live' | 'simulator'
  const [metadata, setMetadata] = useState({ teams: [], venues: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Default Match State
  const [matchState, setMatchState] = useState({
    batting_team: 'Chennai Super Kings',
    bowling_team: 'Mumbai Indians',
    venue: 'Wankhede Stadium, Mumbai',
    current_score: 124,
    wickets_fallen: 3,
    overs_completed: 13.4,
    target_runs: 175,
    toss_winner: 'Chennai Super Kings',
    toss_decision: 'field'
  });

  const [predictionResult, setPredictionResult] = useState(null);

  // Fetch Metadata on Load
  useEffect(() => {
    fetchMetadata()
      .then((data) => {
        setMetadata(data);
        if (data.teams.length >= 2) {
          setMatchState(prev => ({
            ...prev,
            batting_team: data.teams[0].name,
            bowling_team: data.teams[1].name,
            venue: data.default_venue || prev.venue
          }));
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError('Could not connect to FastAPI Backend server.');
        setLoading(false);
      });
  }, []);

  // Real-Time Auto Predict whenever matchState updates
  useEffect(() => {
    if (activeMode === 'live' && matchState.batting_team && matchState.bowling_team) {
      // Small debounce for real-time reactivity
      const timeout = setTimeout(() => {
        predictWinProbability(matchState)
          .then((res) => {
            setPredictionResult(res);
            setError(null);
          })
          .catch((err) => {
            setError(err.message);
          });
      }, 100);

      return () => clearTimeout(timeout);
    }
  }, [matchState, activeMode]);

  const handleSwapTeams = () => {
    setMatchState(prev => ({
      ...prev,
      batting_team: prev.bowling_team,
      bowling_team: prev.batting_team
    }));
  };

  const battingTeamInfo = metadata.teams.find(t => t.name === matchState.batting_team);
  const bowlingTeamInfo = metadata.teams.find(t => t.name === matchState.bowling_team);

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar activeMode={activeMode} setActiveMode={setActiveMode} />

      <main style={{ flex: 1, padding: '2rem', maxWidth: '1400px', margin: '0 auto', width: '100%' }}>
        {error && (
          <div style={{
            background: 'rgba(255, 42, 75, 0.15)',
            border: '1px solid rgba(255, 42, 75, 0.4)',
            color: '#ff4b2b',
            padding: '1rem 1.5rem',
            borderRadius: '12px',
            marginBottom: '1.5rem',
            fontWeight: 600
          }}>
            ⚠️ {error}
          </div>
        )}

        {activeMode === 'live' ? (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.1fr', gap: '2rem', alignItems: 'start' }}>
            <PredictorCard
              metadata={metadata}
              matchState={matchState}
              onChange={setMatchState}
              onSwapTeams={handleSwapTeams}
            />

            <WinGauge
              result={predictionResult}
              battingTeamInfo={battingTeamInfo}
              bowlingTeamInfo={bowlingTeamInfo}
            />
          </div>
        ) : (
          <ReplaySimulator teams={metadata.teams} />
        )}
      </main>

      <footer style={{
        textAlign: 'center',
        padding: '1.5rem',
        borderTop: '1px solid var(--border-color)',
        fontSize: '0.85rem',
        color: 'var(--text-muted)'
      }}>
        IPL Win Probability Predictor ML System • Built with FastAPI, XGBoost, Scikit-Learn & React
      </footer>
    </div>
  );
}
