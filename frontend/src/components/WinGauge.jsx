import React from 'react';
import { Flame, ShieldAlert, TrendingUp, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function WinGauge({ result, battingTeamInfo, bowlingTeamInfo }) {
  if (!result) return null;

  const {
    batting_team,
    bowling_team,
    chasing_team_win_prob,
    defending_team_win_prob,
    runs_left,
    balls_left,
    wickets_remaining,
    crr,
    rrr,
    phase
  } = result;

  const battingColor = battingTeamInfo?.primary_color || '#00f0ff';
  const bowlingColor = bowlingTeamInfo?.primary_color || '#ff2a4b';

  // Pressure Index Calculation
  let pressureLevel = 'Balanced';
  let pressureColor = '#00f0ff';

  if (rrr > 14 || (rrr > 10 && wickets_remaining <= 3)) {
    pressureLevel = 'EXTREME PRESSURE';
    pressureColor = '#ff2a4b';
  } else if (rrr > 10 || wickets_remaining <= 4) {
    pressureLevel = 'HIGH PRESSURE';
    pressureColor = '#ffaa00';
  } else if (chasing_team_win_prob >= 75) {
    pressureLevel = 'CHASING TEAM IN CONTROL';
    pressureColor = '#00ff88';
  }

  return (
    <div className="glass-card" style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
          LIVE WIN PROBABILITY
        </h3>
        <span style={{
          fontSize: '0.8rem',
          fontWeight: 700,
          padding: '4px 12px',
          borderRadius: '12px',
          background: `${pressureColor}22`,
          color: pressureColor,
          border: `1px solid ${pressureColor}44`,
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px'
        }}>
          <Flame size={14} /> {pressureLevel}
        </span>
      </div>

      {/* Main Broadcast Probability Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '1.5rem', alignItems: 'center', marginBottom: '2rem' }}>
        {/* Chasing Team (Batting) */}
        <div style={{
          background: `linear-gradient(135deg, ${battingColor}22 0%, rgba(10,15,28,0.8) 100%)`,
          border: `1px solid ${battingColor}55`,
          borderRadius: '16px',
          padding: '1.5rem',
          textAlign: 'center',
          boxShadow: chasing_team_win_prob > 50 ? `0 0 30px ${battingColor}33` : 'none'
        }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
            CHASING (2ND INNINGS)
          </span>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#fff', marginBottom: '0.5rem' }}>
            {batting_team}
          </h2>
          <div style={{ fontSize: '3.2rem', fontWeight: 900, color: battingColor, fontFamily: 'var(--font-mono)' }}>
            {chasing_team_win_prob}%
          </div>
        </div>

        <div style={{ textAlign: 'center', fontWeight: 800, fontSize: '1.2rem', color: 'var(--text-muted)' }}>
          VS
        </div>

        {/* Defending Team (Bowling) */}
        <div style={{
          background: `linear-gradient(135deg, ${bowlingColor}22 0%, rgba(10,15,28,0.8) 100%)`,
          border: `1px solid ${bowlingColor}55`,
          borderRadius: '16px',
          padding: '1.5rem',
          textAlign: 'center',
          boxShadow: defending_team_win_prob > 50 ? `0 0 30px ${bowlingColor}33` : 'none'
        }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '4px' }}>
            DEFENDING
          </span>
          <h2 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#fff', marginBottom: '0.5rem' }}>
            {bowling_team}
          </h2>
          <div style={{ fontSize: '3.2rem', fontWeight: 900, color: bowlingColor, fontFamily: 'var(--font-mono)' }}>
            {defending_team_win_prob}%
          </div>
        </div>
      </div>

      {/* Animated Broadcast Win Probability Split Bar */}
      <div style={{ marginBottom: '2rem' }}>
        <div style={{
          height: '24px',
          borderRadius: '12px',
          overflow: 'hidden',
          display: 'flex',
          background: '#111',
          border: '1px solid rgba(255,255,255,0.1)',
          boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.5)'
        }}>
          <div style={{
            width: `${chasing_team_win_prob}%`,
            background: `linear-gradient(90deg, ${battingColor}, #00f0ff)`,
            transition: 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-end',
            paddingRight: '10px',
            color: '#000',
            fontWeight: 800,
            fontSize: '0.8rem'
          }}>
            {chasing_team_win_prob > 15 && `${chasing_team_win_prob}%`}
          </div>
          <div style={{
            width: `${defending_team_win_prob}%`,
            background: `linear-gradient(90deg, #ff2a4b, ${bowlingColor})`,
            transition: 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'flex-start',
            paddingLeft: '10px',
            color: '#fff',
            fontWeight: 800,
            fontSize: '0.8rem'
          }}>
            {defending_team_win_prob > 15 && `${defending_team_win_prob}%`}
          </div>
        </div>
      </div>

      {/* Match Context Key Metrics Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', textAlign: 'center', border: '1px solid rgba(255,255,255,0.05)' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>RUNS NEEDED</span>
          <span style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff', fontFamily: 'var(--font-mono)' }}>
            {runs_left} <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>from {balls_left}b</span>
          </span>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', textAlign: 'center', border: '1px solid rgba(255,255,255,0.05)' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>WICKETS IN HAND</span>
          <span style={{ fontSize: '1.6rem', fontWeight: 800, color: wickets_remaining > 5 ? '#00ff88' : '#ff2a4b', fontFamily: 'var(--font-mono)' }}>
            {wickets_remaining}
          </span>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', textAlign: 'center', border: '1px solid rgba(255,255,255,0.05)' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>CURRENT RATE (CRR)</span>
          <span style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff', fontFamily: 'var(--font-mono)' }}>
            {crr}
          </span>
        </div>

        <div style={{ background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', textAlign: 'center', border: '1px solid rgba(255,255,255,0.05)' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block' }}>REQUIRED RATE (RRR)</span>
          <span style={{ fontSize: '1.6rem', fontWeight: 800, color: rrr > crr ? '#ffaa00' : '#00f0ff', fontFamily: 'var(--font-mono)' }}>
            {rrr}
          </span>
        </div>
      </div>
    </div>
  );
}
