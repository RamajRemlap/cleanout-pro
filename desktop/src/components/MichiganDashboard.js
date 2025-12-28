import React, { useState, useEffect } from 'react';
import './MichiganDashboard.css';

const MichiganDashboard = () => {
  const [stats, setStats] = useState({
    totalLeads: 0,
    leadsContacted: 0,
    quotesSent: 0,
    conversionRate: 0,
    averageJobValue: 0,
    systemStatus: 'offline'
  });
  
  const [leads, setLeads] = useState([]);
  const [campaignRunning, setCampaignRunning] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState('all');
  const [urgencyThreshold, setUrgencyThreshold] = useState(0.4);

  useEffect(() => {
    loadMichiganData();
    const interval = setInterval(loadMichiganData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const loadMichiganData = async () => {
    try {
      // Load analytics
      const analyticsResponse = await fetch('/api/michigan/analytics');
      if (analyticsResponse.ok) {
        const analytics = await analyticsResponse.json();
        setStats({
          totalLeads: analytics.total_leads,
          leadsContacted: analytics.leads_contacted,
          quotesSent: analytics.quotes_sent,
          conversionRate: analytics.conversion_rate,
          averageJobValue: analytics.average_job_value,
          systemStatus: 'online'
        });
      }

      // Load leads
      const leadsResponse = await fetch('/api/michigan/leads');
      if (leadsResponse.ok) {
        const leadsData = await leadsResponse.json();
        setLeads(leadsData.slice(0, 20)); // Show top 20 leads
      }
    } catch (error) {
      console.error('Error loading Michigan data:', error);
      setStats(prev => ({ ...prev, systemStatus: 'error' }));
    }
  };

  const startCampaign = async (campaignType) => {
    setCampaignRunning(true);
    try {
      const response = await fetch('/api/michigan/campaigns/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          campaign_type: campaignType,
          location_filter: selectedLocation !== 'all' ? selectedLocation : null,
          urgency_threshold: urgencyThreshold
        })
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Campaign started:', result);
        // Refresh data after campaign starts
        setTimeout(loadMichiganData, 5000);
      }
    } catch (error) {
      console.error('Error starting campaign:', error);
    } finally {
      setCampaignRunning(false);
    }
  };

  const startSystem = async () => {
    try {
      const response = await fetch('/api/michigan/start', { method: 'POST' });
      if (response.ok) {
        loadMichiganData();
      }
    } catch (error) {
      console.error('Error starting system:', error);
    }
  };

  const stopSystem = async () => {
    try {
      const response = await fetch('/api/michigan/stop', { method: 'POST' });
      if (response.ok) {
        loadMichiganData();
      }
    } catch (error) {
      console.error('Error stopping system:', error);
    }
  };

  const getUrgencyColor = (score) => {
    if (score >= 0.7) return '#ff4444'; // High - Red
    if (score >= 0.4) return '#ff8800'; // Medium - Orange
    return '#44aa44'; // Low - Green
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  };

  const formatPercentage = (value) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="michigan-dashboard">
      <div className="dashboard-header">
        <h1>🚀 Michigan Autonomous Client Acquisition</h1>
        <div className="status-bar">
          <span className={`status-indicator ${stats.systemStatus}`}>
            {stats.systemStatus === 'online' ? '🟢 Online' : 
             stats.systemStatus === 'error' ? '🔴 Error' : '🟡 Offline'}
          </span>
          <span className="last-update">
            Last updated: {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* Key Performance Metrics */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{stats.totalLeads}</div>
          <div className="metric-label">Total Leads</div>
          <div className="metric-source">Michigan Area</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{stats.leadsContacted}</div>
          <div className="metric-label">Leads Contacted</div>
          <div className="metric-source">Email/SMS</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{stats.quotesSent}</div>
          <div className="metric-label">Quotes Sent</div>
          <div className="metric-source">Automated</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{formatPercentage(stats.conversionRate)}</div>
          <div className="metric-label">Conversion Rate</div>
          <div className="metric-source">Contact to Quote</div>
        </div>
        
        <div className="metric-card">
          <div className="metric-value">{formatCurrency(stats.averageJobValue)}</div>
          <div className="metric-label">Average Job Value</div>
          <div className="metric-source">Michigan Pricing</div>
        </div>
      </div>

      {/* Control Panel */}
      <div className="control-panel">
        <h2>🎛️ Autonomous Control</h2>
        
        <div className="control-section">
          <div className="control-group">
            <label>Location Filter:</label>
            <select value={selectedLocation} onChange={(e) => setSelectedLocation(e.target.value)}>
              <option value="all">All Michigan Cities</option>
              <option value="detroit">Detroit</option>
              <option value="ann_arbor">Ann Arbor</option>
              <option value="royal_oak">Royal Oak</option>
              <option value="bloomfield_hills">Bloomfield Hills</option>
            </select>
          </div>
          
          <div className="control-group">
            <label>Urgency Threshold: {formatPercentage(urgencyThreshold)}</label>
            <input
              type="range"
              min="0.1"
              max="0.9"
              step="0.1"
              value={urgencyThreshold}
              onChange={(e) => setUrgencyThreshold(parseFloat(e.target.value))}
            />
          </div>
        </div>

        <div className="campaign-buttons">
          <button
            className="campaign-btn lead-gen"
            onClick={() => startCampaign('lead_generation')}
            disabled={campaignRunning}
          >
            📊 Generate Leads
          </button>
          
          <button
            className="campaign-btn outreach"
            onClick={() => startCampaign('outreach')}
            disabled={campaignRunning || !stats.systemStatus}
          >
            📧 Start Outreach
          </button>
          
          <button
            className="campaign-btn quoting"
            onClick={() => startCampaign('quoting')}
            disabled={campaignRunning || !stats.systemStatus}
          >
            💰 Send Quotes
          </button>
          
          <button
            className="campaign-btn full-cycle"
            onClick={() => startCampaign('full_cycle')}
            disabled={campaignRunning || !stats.systemStatus}
          >
            🚀 Full Autonomous Cycle
          </button>
        </div>

        <div className="system-controls">
          <button className="system-btn start" onClick={startSystem}>
            ▶️ Start System
          </button>
          <button className="system-btn stop" onClick={stopSystem}>
            ⏹️ Stop System
          </button>
        </div>
      </div>

      {/* Recent Leads */}
      <div className="leads-section">
        <h2>🎯 Recent Michigan Leads</h2>
        
        <div className="leads-table">
          <div className="table-header">
            <div>Source</div>
            <div>Title</div>
            <div>Location</div>
            <div>Urgency</div>
            <div>Value</div>
            <div>Status</div>
          </div>
          
          {leads.map((lead, index) => (
            <div key={lead.id} className="table-row">
              <div className="source-badge">{lead.source}</div>
              <div className="lead-title">{lead.title}</div>
              <div className="location">{lead.location}</div>
              <div className="urgency">
                <div 
                  className="urgency-score"
                  style={{ 
                    backgroundColor: getUrgencyColor(lead.urgency_score) 
                  }}
                >
                  {formatPercentage(lead.urgency_score)}
                </div>
              </div>
              <div className="value">{formatCurrency(lead.estimated_value)}</div>
              <div className="status">
                {lead.contacted ? '📧 Contacted' : '⏳ Pending'}
                {lead.quoted && ' 💰 Quoted'}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Michigan-Specific Insights */}
      <div className="insights-section">
        <h2>🧠 Michigan Market Insights</h2>
        
        <div className="insights-grid">
          <div className="insight-card">
            <h3>🏙️ Top Markets</h3>
            <ul>
              <li><strong>Detroit:</strong> Highest volume, eviction cleanouts</li>
              <li><strong>Ann Arbor:</strong> Student housing, faculty moves</li>
              <li><strong>Royal Oak:</strong> Renovation debris, urban renewals</li>
              <li><strong>Bloomfield Hills:</strong> Premium estate cleanouts</li>
            </ul>
          </div>
          
          <div className="insight-card">
            <h3>📈 Peak Times</h3>
            <ul>
              <li><strong>Monday-Wednesday:</strong> Moving inquiries</li>
              <li><strong>End of month:</strong> Eviction cleanouts</li>
              <li><strong>Summer:</strong> Student housing turnover</li>
              <li><strong>Weekends:</strong> Estate sale prep</li>
            </ul>
          </div>
          
          <div className="insight-card">
            <h3>💰 Michigan Discounts</h3>
            <ul>
              <li><strong>Student:</strong> 15% discount</li>
              <li><strong>Military:</strong> 20% discount</li>
              <li><strong>Senior:</strong> 10% discount</li>
              <li><strong>Michigan Resident:</strong> 5% automatic</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MichiganDashboard;