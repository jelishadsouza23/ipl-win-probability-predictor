import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, FastForward, Tv, Trophy } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ReferenceLine } from 'recharts';
import { fetchSampleMatches, simulateMatchReplay } from '../api';

export default function ReplaySimulator({ teams = [] }) {
  const [sampleMatches, setSampleMatches] = useState([]);
  const [selectedMatchId, setSelectedMatchId] = useState('match_2023_final');
  const [simulationData, setSimulationData] = useState(null);
  const [currentBallIndex, setCurrentBallIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(500); // ms per ball

  useEffect(() => {
    fetchSampleMatches().then(setSampleMatches).catch(console.error);
  }, []);

  useEffect(() => {
    if (selectedMatchId) {
      setIsPlaying(false);
      setCurrentBallIndex(0);
      simulateMatchReplay(selectedMatchId).then(data => {
        setSimulationData(data);
      }).catch(console.error);
    }
  }, [selectedMatchId]);

  // Animation Loop
  useEffect(() => {
    let timer;
    if (isPlaying && simulationData) {
      timer = setInterval(() => {
        setCurrentBallIndex((prev) => {
          if (prev >= simulationData.ball_by_ball.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, playbackSpeed);
    }
    return () => clearInterval(timer);
  }, [isPlaying, simulationData, playbackSpeed]);

  if (!simulationData) return <div style={{ color: 'var(--text-muted)', padding: '2rem' }}>Loading match replay simulation...</div>;

  const currentBall = simulationData.ball_by_ball[currentBallIndex] || simulationData.ball_by_ball[0];
  const chartData = simulationData.ball_by_ball.slice(0, currentBallIndex + 1);

  const battingTeamInfo = teams.find(t => t.name === simulationData.batting_team);
  const bowlingTeamInfo = teams.find(t => t.name === simulationData.bowling_team);
  const battingColor = battingTeamInfo?.primary_color || '#00f0ff';
  const bowlingColor = bowlingTeamInfo?.primary_color || '#ff2a4b';

  return (
    <div className="glass-card" style={{ padding: '2rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h3 style={{ fontSize: '1.3rem', fontWeight: 800, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Tv color="var(--text-accent)" size={24} /> OVER-BY-OVER BROADCAST REPLAY SIMULATOR
          </h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Watch the live win probability curve fluctuate ball-by-ball in classic IPL thrillers
          </p>
        </div>

        {/* Match Selector Dropdown */}
        <select
          className="glass-input"
          style={{ width: 'auto', minWidth: '280px' }}
          value={selectedMatchId}
          onChange={(e) => setSelectedMatchId(e.target.value)}
        >
          {sampleMatches.map((m) => (
            <option key={m.id} value={m.id} style={{ background: '#121a2c', color: '#fff' }}>
              {m.title}
            </option>
          ))}
        </select>
      </div>

      {/* Simulator Scoreboard Header */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(0,240,255,0.08) 0%, rgba(112,0,255,0.08) 100%)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '16px',
        padding: '1.5rem',
        marginBottom: '2rem',
        display: 'grid',
        gridTemplateColumns: '1fr auto 1fr',
        alignItems: 'center',
        gap: '1rem'
      }}>
        {/* Batting Team Live State */}
        <div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>CHASING</span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>{simulationData.batting_team}</h2>
          <div style={{ fontSize: '2rem', fontWeight: 900, color: battingColor, fontFamily: 'var(--font-mono)' }}>
            {currentBall.total_score} / {currentBall.wickets}
            <span style={{ fontSize: '1rem', color: 'var(--text-muted)', marginLeft: '8px' }}>
              ({currentBall.overs_completed} ov)
            </span>
          </div>
        </div>

        {/* Live Probability Dial */}
        <div style={{ textAlign: 'center', padding: '0 1.5rem', borderLeft: '1px solid rgba(255,255,255,0.1)', borderRight: '1px solid rgba(255,255,255,0.1)' }}>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
            WIN PROBABILITY
          </span>
          <div style={{ fontSize: '2.5rem', fontWeight: 900, color: 'var(--text-accent)', fontFamily: 'var(--font-mono)' }}>
            {currentBall.chasing_win_prob}%
          </div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Target: {simulationData.target_runs} runs
          </span>
        </div>

        {/* Defending Team State */}
        <div style={{ textAlign: 'right' }}>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>DEFENDING</span>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>{simulationData.bowling_team}</h2>
          <div style={{ fontSize: '2rem', fontWeight: 900, color: bowlingColor, fontFamily: 'var(--font-mono)' }}>
            {currentBall.defending_win_prob}%
            <span style={{ fontSize: '1rem', color: 'var(--text-muted)', marginLeft: '8px' }}>
              Win Prob
            </span>
          </div>
        </div>
      </div>

      {/* Interactive Play Controls Bar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
        <button
          onClick={() => setIsPlaying(!isPlaying)}
          className="btn-primary"
          style={{ padding: '0.75rem 1.5rem' }}
        >
          {isPlaying ? <Pause size={18} /> : <Play size={18} />}
          {isPlaying ? 'Pause Replay' : 'Play Replay'}
        </button>

        <button
          onClick={() => { setIsPlaying(false); setCurrentBallIndex(0); }}
          className="btn-secondary"
        >
          <RotateCcw size={16} /> Reset
        </button>

        <div style={{ flex: 1, padding: '0 1rem' }}>
          <input
            type="range"
            min="0"
            max={simulationData.ball_by_ball.length - 1}
            value={currentBallIndex}
            onChange={(e) => { setIsPlaying(false); setCurrentBallIndex(parseInt(e.target.value)); }}
          />
        </div>

        <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.9rem', color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>
          Ball {currentBallIndex + 1} / {simulationData.ball_by_ball.length}
        </span>
      </div>

      {/* Live Recharts Win Probability Trajectory Curve */}
      <div style={{ height: '320px', width: '100%', marginBottom: '1.5rem' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="overs_completed" stroke="var(--text-muted)" unit=" ov" />
            <YAxis domain={[0, 100]} stroke="var(--text-muted)" unit="%" />
            <Tooltip
              contentStyle={{ background: '#121a2c', borderColor: 'rgba(255,255,255,0.1)', borderRadius: '8px' }}
              labelFormatter={(val) => `Over ${val}`}
              formatter={(value) => [`${value}%`, 'Chasing Win Prob']}
            />
            <ReferenceLine y={50} stroke="rgba(255,255,255,0.2)" strokeDasharray="3 3" label={{ value: '50/50 Even', fill: 'var(--text-muted)', fontSize: 12 }} />
            <Line
              type="monotone"
              dataKey="chasing_win_prob"
              stroke="var(--text-accent)"
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 6, fill: '#00f0ff' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Ball Event Feed */}
      <div style={{
        background: 'rgba(0,0,0,0.4)',
        borderRadius: '12px',
        padding: '1rem 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        border: '1px solid rgba(255,255,255,0.05)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            background: currentBall.event_type === 'W' ? '#ff2a4b' : (currentBall.runs_ball >= 4 ? '#00ff88' : 'rgba(255,255,255,0.1)'),
            color: currentBall.event_type === 'W' || currentBall.runs_ball >= 4 ? '#000' : '#fff',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 800
          }}>
            {currentBall.event_type}
          </span>
          <div>
            <span style={{ fontSize: '0.9rem', fontWeight: 700 }}>
              Over {currentBall.overs_completed}: {currentBall.event_type === 'W' ? 'WICKET FALLEN!' : `${currentBall.runs_ball} Run(s) Scored`}
            </span>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'block' }}>
              Need {currentBall.runs_left} runs off {currentBall.balls_left} balls (RRR: {currentBall.rrr})
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
