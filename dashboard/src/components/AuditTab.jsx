import React, { useState } from 'react';

export function AuditTab({ data }) {
  const [replayMode, setReplayMode] = useState(false);
  const audit = data?.audit || { timeline: [], decisions: [], interventions: [] };
  
  return (
    <div className="principle-tab">
      <h2>📼 Execution Reconstructor</h2>
      <p className="description">Full audit trail with replay capability for multi-step planning</p>
      
      <div className="audit-summary">
        <div className="summary-card">
          <div className="summary-value">{audit.timeline?.length || 0}</div>
          <div className="summary-label">Total Events</div>
        </div>
        <div className="summary-card">
          <div className="summary-value">{audit.decisions?.length || 0}</div>
          <div className="summary-label">Decision Points</div>
        </div>
        <div className="summary-card">
          <div className="summary-value">{audit.interventions?.length || 0}</div>
          <div className="summary-label">Interventions</div>
        </div>
      </div>
      
      <div className="replay-controls">
        <button 
          className={`replay-btn ${replayMode ? 'active' : ''}`}
          onClick={() => setReplayMode(!replayMode)}
        >
          {replayMode ? '⏹ Stop Replay' : '▶️ Replay Execution'}
        </button>
        <button className="export-btn">
          📥 Export Audit Report
        </button>
      </div>
      
      {replayMode && (
        <div className="replay-viewer">
          <div className="timeline-slider">
            <input type="range" min="0" max={audit.timeline?.length || 0} />
          </div>
          <div className="replay-status">Replaying execution...</div>
        </div>
      )}
      
      <div className="timeline-section">
        <h3>📋 Execution Timeline</h3>
        <div className="timeline">
          {audit.timeline?.map((event, i) => (
            <div key={i} className={`timeline-item ${event.type}`}>
              <span className="time">{event.timestamp?.split('T')[1]?.slice(0, 8)}</span>
              <span className="type-badge">{event.type}</span>
              <span className="description">{event.description}</span>
            </div>
          ))}
        </div>
      </div>
      
      <div className="decisions-section">
        <h3>🎯 Decision Points</h3>
        {audit.decisions?.map((dec, i) => (
          <div key={i} className="decision-card">
            <div className="decision-type">{dec.decisionType}</div>
            <div className="rationale">{dec.rationale}</div>
            <div className="state-change">
              <span className="before">{JSON.stringify(dec.inputState)}</span>
              <span className="arrow">→</span>
              <span className="after">{JSON.stringify(dec.outputState)}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}