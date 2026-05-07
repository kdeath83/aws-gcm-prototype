import React, { useState, useEffect } from 'react';
import { CoherenceTab } from './components/CoherenceTab';
import { ToolCallTab } from './components/ToolCallTab';
import { WasteTab } from './components/WasteTab';
import { AuditTab } from './components/AuditTab';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('coherence');
  const [executionData, setExecutionData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Fix 2: Get WebSocket URL from environment or fetch from API
    const wsUrl = process.env.REACT_APP_WEBSOCKET_URL || 
                  window.GCM_CONFIG?.websocketUrl ||
                  'wss://placeholder.execute-api.region.amazonaws.com/production';
    
    if (wsUrl.includes('placeholder')) {
      console.warn('WebSocket URL not configured - dashboard will run in demo mode');
      setIsConnected(false);
      return;
    }
    
    const ws = new WebSocket(wsUrl);
    
    ws.onopen = () => {
      console.log('GCM Dashboard connected');
      setIsConnected(true);
    };
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setExecutionData(data);
      } catch (e) {
        console.error('Failed to parse WebSocket message:', e);
      }
    };
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };
    ws.onclose = () => {
      console.log('GCM Dashboard disconnected');
      setIsConnected(false);
    };
    
    return () => ws.close();
  }, []);

  const renderTab = () => {
    switch(activeTab) {
      case 'coherence': return <CoherenceTab data={executionData} />;
      case 'tools': return <ToolCallTab data={executionData} />;
      case 'waste': return <WasteTab data={executionData} />;
      case 'audit': return <AuditTab data={executionData} />;
      default: return <CoherenceTab data={executionData} />;
    }
  };

  return (
    <div className="App">
      <header>
        <h1>🔍 Governable Capability Monitor (GCM)</h1>
        <div className={`status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '● Live' : '○ Offline'}
        </div>
      </header>
      
      <nav className="tabs">
        {['coherence', 'tools', 'waste', 'audit'].map(tab => (
          <button 
            key={tab}
            className={activeTab === tab ? 'active' : ''}
            onClick={() => setActiveTab(tab)}
          >
            {tab === 'coherence' && '1. Coherence'}
            {tab === 'tools' && '2. Tool-Calls'}
            {tab === 'waste' && '3. Waste'}
            {tab === 'audit' && '4. Reconstruction'}
          </button>
        ))}
      </nav>
      
      <main>{renderTab()}</main>
      
      <footer>
        <p>GCM Prototype — AWS Native AI Governance</p>
      </footer>
    </div>
  );
}

export default App;