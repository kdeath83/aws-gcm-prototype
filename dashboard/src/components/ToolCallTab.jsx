import React from 'react';

export function ToolCallTab({ data }) {
  const graph = data?.toolGraph || { depth: 0, nodes: [], cycles: [], deadEnds: [], status: 'NO_DATA' };
  
  return (
    <div className="principle-tab">
      <h2>🕸️ Tool-Call Graph Monitor</h2>
      <p className="description">Visualizing tool invocation graphs and detecting expansion without progress</p>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{graph.depth}</div>
          <div className="metric-label">Graph Depth</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{graph.nodes?.length || 0}</div>
          <div className="metric-label">Total Nodes</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{graph.cycles?.length || 0}</div>
          <div className="metric-label">Cycles Detected</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">{graph.deadEnds?.length || 0}</div>
          <div className="metric-label">Dead Ends</div>
        </div>
      </div>
      
      <div className="alert-section">
        {graph.expansionWithoutProgress && (
          <div className="alert critical">
            ⚠️ Critical: Tool graph expanding without state change
          </div>
        )}
        {(graph.cycles?.length > 0) && (
          <div className="alert warning">
            ⚠️ Warning: Cyclic tool invocation detected
          </div>
        )}
      </div>
      
      <div className="graph-viz">
        <h3>Tool Invocation Chain</h3>
        {graph.nodes?.map((node, i) => (
          <div key={i} className={`graph-node ${node.stateChange ? 'productive' : 'wasted'}`}>
            <span className="node-index">{i + 1}</span>
            <span className="node-tool">{node.tool}</span>
            <span className="node-result">{node.result}</span>
            {node.stateChange && <span className="badge productive">✓ State Change</span>}
          </div>
        ))}
      </div>
    </div>
  );
}