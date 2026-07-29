import React from 'react';
import { Sliders, MapPin, Shield, Zap } from 'lucide-react';

export default function PredictorCard({
  metadata,
  matchState,
  onChange,
  onSwapTeams
}) {
  const { teams = [], venues = [] } = metadata || {};

  const handleInputChange = (field, value) => {
    onChange({ ...matchState, [field]: value });
  };

  return (
    <div className="glass-card" style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <Sliders size={20} color="var(--text-accent)" /> LIVE MATCH SITUATION INPUTS
        </h3>
        <button
          onClick={onSwapTeams}
          className="btn-secondary"
          style={{ fontSize: '0.8rem', padding: '0.4rem 0.8rem' }}
        >
          Swap Teams 🔄
        </button>
      </div>

      {/* Team Selection */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '0.5rem' }}>
            Batting Team (2nd Innings Chaser)
          </label>
          <select
            className="glass-input"
            value={matchState.batting_team}
            onChange={(e) => handleInputChange('batting_team', e.target.value)}
          >
            {teams.map((t) => (
              <option key={t.name} value={t.name} style={{ background: '#121a2c', color: '#fff' }}>
                {t.name} ({t.short_name})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '0.5rem' }}>
            Bowling Team (Defending)
          </label>
          <select
            className="glass-input"
            value={matchState.bowling_team}
            onChange={(e) => handleInputChange('bowling_team', e.target.value)}
          >
            {teams.map((t) => (
              <option key={t.name} value={t.name} style={{ background: '#121a2c', color: '#fff' }}>
                {t.name} ({t.short_name})
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Venue Selection */}
      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, marginBottom: '0.5rem' }}>
          <MapPin size={14} style={{ display: 'inline', marginRight: '4px' }} /> Match Stadium / Venue
        </label>
        <select
          className="glass-input"
          value={matchState.venue}
          onChange={(e) => handleInputChange('venue', e.target.value)}
        >
          {venues.map((v) => (
            <option key={v.name} value={v.name} style={{ background: '#121a2c', color: '#fff' }}>
              {v.name}
            </option>
          ))}
        </select>
      </div>

      {/* Match Parameters Sliders & Numbers */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        {/* Target Runs */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>1st Innings Target</span>
            <span style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-accent)' }}>{matchState.target_runs} Runs</span>
          </div>
          <input
            type="range"
            min="60"
            max="260"
            value={matchState.target_runs}
            onChange={(e) => handleInputChange('target_runs', parseInt(e.target.value))}
          />
        </div>

        {/* Current Score */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Current Score</span>
            <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#fff' }}>{matchState.current_score} Runs</span>
          </div>
          <input
            type="range"
            min="0"
            max={matchState.target_runs}
            value={matchState.current_score}
            onChange={(e) => handleInputChange('current_score', parseInt(e.target.value))}
          />
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
        {/* Overs Completed */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Overs Completed</span>
            <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#fff' }}>{matchState.overs_completed} Overs</span>
          </div>
          <input
            type="range"
            min="0.1"
            max="19.5"
            step="0.1"
            value={matchState.overs_completed}
            onChange={(e) => handleInputChange('overs_completed', parseFloat(e.target.value))}
          />
        </div>

        {/* Wickets Fallen */}
        <div style={{ background: 'rgba(255,255,255,0.02)', padding: '1rem', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Wickets Fallen</span>
            <span style={{ fontSize: '1.1rem', fontWeight: 800, color: matchState.wickets_fallen >= 7 ? '#ff2a4b' : '#fff' }}>
              {matchState.wickets_fallen} / 10
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="9"
            value={matchState.wickets_fallen}
            onChange={(e) => handleInputChange('wickets_fallen', parseInt(e.target.value))}
          />
        </div>
      </div>
    </div>
  );
}
