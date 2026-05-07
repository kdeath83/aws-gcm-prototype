import React from 'react';

export function WasteTab({ data }) {
  const waste = data?.waste || { score: 0, metrics: {}, indicators: [], status: 'NO_DATA' };
  const gap = data?.capabilityGap || { capability: 0, productivity: 0, gap: 0 };
  
  return (
    <div className="principle-tab">
      <h2>📊 Structural Waste Detection</h2>
      <p className="description">Measuring the gap between model capability and system productivity</p>
      
      <div className="waste-score-card">
        <div className="waste-score-value">{waste.score.toFixed(1)}%</div>
        <div className="waste-score-label">Waste Score</div>
        <div className={`status-badge ${waste.status.toLowerCase()}`}>{waste.status}</div>
      </div>
      
      <div className="gap-analysis">
        <h3>⚡ Capability vs Productivity Gap</h3>
        <div className="gap-bar">
          <div className="gap-segment capability" style={{ width: `${gap.capability}%` }}>
            Capability: {gap.capability}%
          </div>
          <div className="gap-segment productivity" style={{ width: `${gap.productivity}%` }}>
            Productivity: {gap.productivity}%
          </div>
          <div className="gap-segment lost" style={{ width: `${gap.gap}%` }}>
            Lost: {gap.gap}%
          </div>
        </div>
      </div>
      
      <div className="waste-metrics">
        <h3>💰 Cost & Efficiency Metrics</h3>
        <div className="metric-row">
          <span>Latency Waste:</span>
          <span>{waste.metrics.latencyWaste?.toFixed(1)}%</span>
        </div>
        <div className="metric-row">
          <span>Cost per Output:</span>
          <span>${waste.metrics.costPerOutput?.toFixed(4)}</span>
        </div>
        <div className="metric-row">
          <span>Tokens per Change:</span>
          <span>{waste.metrics.tokensPerChange?.toFixed(0)}</span>
        </div>
        <div className="metric-row">
          <span>Retry Waste:</span>
          <span>{waste.metrics.retryWaste?.toFixed(1)}%</span>
        </div>
      </div>
      
      <div className="indicators-section">
        <h3>🚨 Waste Indicators ({waste.indicators.length})</h3>
        {waste.indicators.map((ind, i) => (
          <div key={i} className={`indicator ${ind.severity}`}>
            <strong>{ind.type}:</strong> {ind.description}
            <br /><small>{ind.metric}</small>
          </div>
        ))}
      </div>
    </div>
  );
}