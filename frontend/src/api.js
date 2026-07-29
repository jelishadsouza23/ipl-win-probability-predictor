const API_BASE = '/api';

export async function fetchMetadata() {
  const res = await fetch(`${API_BASE}/metadata`);
  if (!res.ok) throw new Error('Failed to fetch metadata');
  return res.json();
}

export async function predictWinProbability(matchState) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(matchState),
  });

  if (!res.ok) {
    const errorData = await res.json();
    throw new Error(errorData.detail || 'Prediction failed');
  }

  return res.json();
}

export async function fetchSampleMatches() {
  const res = await fetch(`${API_BASE}/sample-matches`);
  if (!res.ok) throw new Error('Failed to fetch sample matches');
  return res.json();
}

export async function simulateMatchReplay(matchId) {
  const res = await fetch(`${API_BASE}/simulate-match/${matchId}`);
  if (!res.ok) throw new Error('Failed to simulate match replay');
  return res.json();
}
