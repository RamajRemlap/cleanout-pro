import React, { useState } from 'react';
import './Settings.css';

function Settings() {
  const [apiUrl, setApiUrl] = useState('https://web-production-35f31.up.railway.app');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    // Save to localStorage or config file
    localStorage.setItem('api_url', apiUrl);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="settings-page">
      <div className="page-header">
        <h2>Settings</h2>
        <p>Configure your CleanoutPro desktop app</p>
      </div>

      {saved && (
        <div className="success">
          Settings saved successfully!
        </div>
      )}

      {/* API Configuration */}
      <div className="card">
        <h3>API Configuration</h3>

        <div className="setting-item">
          <label>Backend API URL</label>
          <input
            type="text"
            value={apiUrl}
            onChange={(e) => setApiUrl(e.target.value)}
            placeholder="https://your-api-url.com"
            className="input"
          />
          <p className="hint">The URL of your CleanoutPro backend API</p>
        </div>

        <button className="btn btn-primary" onClick={handleSave}>
          💾 Save Settings
        </button>
      </div>

      {/* Display Settings */}
      <div className="card">
        <h3>Display Settings</h3>

        <div className="setting-item">
          <label>Default View Mode</label>
          <select className="input">
            <option value="3d">3D Visualization</option>
            <option value="table">Table View</option>
          </select>
          <p className="hint">Choose the default view mode when viewing jobs</p>
        </div>

        <div className="setting-item">
          <label>Theme</label>
          <select className="input">
            <option value="dark">Dark (Default)</option>
            <option value="light">Light</option>
          </select>
          <p className="hint">Choose your preferred color theme</p>
        </div>
      </div>

      {/* About */}
      <div className="card">
        <h3>About CleanoutPro Desktop</h3>

        <div className="about-info">
          <div className="about-item">
            <strong>Version:</strong>
            <span>1.0.0</span>
          </div>
          <div className="about-item">
            <strong>Platform:</strong>
            <span>{window.navigator.platform}</span>
          </div>
          <div className="about-item">
            <strong>Build:</strong>
            <span>Production</span>
          </div>
        </div>

        <div className="about-description">
          <p>
            CleanoutPro Desktop is an AI-powered cleanout/junk removal business management
            system with 3D visualization capabilities.
          </p>
        </div>

        <div className="about-links">
          <a href="#" className="link">Documentation</a>
          <a href="#" className="link">GitHub Repository</a>
          <a href="#" className="link">Report Issue</a>
        </div>
      </div>
    </div>
  );
}

export default Settings;
