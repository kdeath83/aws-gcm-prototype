import React from 'react';

export function CoherenceTab({ data }) {
  const coherence = data?.coherence || { score: 0, violations: [], status: 'NO_DATA' };
  
  const getScoreColor = (score) => {
    if (score >= 80) return '#22c55e';
    if (score >= 50) return '#eab308';
    return '#ef4444';
  };

  return (
    <div className="principle-tab">
      <h2>🔀 Runtime Control Coherence</h2>
      <p className="description">Detecting conflicting control loops between schedulers, policy layers, and circuit breakers</p>
      
      <div className="score-card">
        <div className="score-value" style={{ color: getScoreColor(coherence.score) }}>
          {coherence.score.toFixed(1)}%
        </div>
        <div className="score-label">Coherence Score</div>
        <div className={`status-badge ${coherence.status.toLowerCase()}`}>
          {coherence.status}
        </div>
      </div>
      
      <div className="violations-section">
        <h3>Control Violations ({coherence.violations.length})</h3>
        {coherence.violations.length === 0 ? (
          <p className="no-issues">✓ No coherence violations detected</p>
        ) : (
          <ul className="violations-list">
            {coherence.violations.map((v, i) => (
              <li key={i} className={`violation ${v.severity}`}>
                <span className="violation-type">{v.type}</span>
                <span className="violation-desc">{v.description}</span>
                <span className="violation-time">{v.timestamp}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}