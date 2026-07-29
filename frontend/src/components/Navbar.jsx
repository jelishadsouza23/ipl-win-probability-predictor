import React from 'react';
import { Activity, Tv, Cpu, Award } from 'lucide-react';

export default function Navbar({ activeMode, setActiveMode }) {
  return (
    <header style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '1.2rem 2rem',
      borderBottom: '1px solid var(--border-color)',
      background: 'rgba(10, 14, 23, 0.8)',
      backdropFilter: 'blur(12px)',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div style={{
          width: '42px',
          height: '42px',
          borderRadius: '12px',
          background: 'var(--gradient-neon)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 15px rgba(0, 240, 255, 0.4)'
        }}>
          <Cpu size={24} color="#fff" />
        </div>
        <div>
          <h1 style={{ fontSize: '1.4rem', fontWeight: 800, letterSpacing: '-0.5px', margin: 0 }}>
            IPL <span className="gradient-text">WIN MATRIX</span>
          </h1>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>
            AI Live Match Probability Predictor
          </p>
        </div>
      </div>

      <nav style={{ display: 'flex', gap: '0.5rem', background: 'rgba(255,255,255,0.05)', padding: '4px', borderRadius: '12px' }}>
        <button
          onClick={() => setActiveMode('live')}
          className={activeMode === 'live' ? 'btn-primary' : 'btn-secondary'}
          style={{ padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
        >
          <Activity size={16} /> Live Predictor
        </button>
        <button
          onClick={() => setActiveMode('simulator')}
          className={activeMode === 'simulator' ? 'btn-primary' : 'btn-secondary'}
          style={{ padding: '0.6rem 1.2rem', fontSize: '0.9rem' }}
        >
          <Tv size={16} /> Replay Simulator
        </button>
      </nav>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          borderRadius: '20px',
          background: 'rgba(0, 240, 255, 0.1)',
          border: '1px solid rgba(0, 240, 255, 0.3)',
          color: 'var(--text-accent)',
          fontSize: '0.8rem',
          fontWeight: 600
        }}>
          <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#00f0ff', boxShadow: '0 0 8px #00f0ff' }}></span>
          XGBoost Calibrated Model
        </span>
      </div>
    </header>
  );
}
