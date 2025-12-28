import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import JobsList from './components/JobsList';
import RoomVisualization from './components/RoomVisualization';
import UltimateVisualization from './components/UltimateVisualization';
import Settings from './components/Settings';
import './App.css';

function App() {
  const [viewMode, setViewMode] = useState('4d'); // '3d', '4d', or 'table'

  return (
    <Router>
      <div className="app">
        {/* Sidebar Navigation */}
        <aside className="sidebar">
          <div className="logo">
            <h1>CleanoutPro</h1>
            <p>Desktop</p>
          </div>

          <nav className="nav">
            <NavLink to="/" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              <span className="icon">📊</span>
              Dashboard
            </NavLink>
            <NavLink to="/jobs" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              <span className="icon">📋</span>
              Jobs
            </NavLink>
            <NavLink to="/visualize" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              <span className="icon">🎲</span>
              3D Visualization
            </NavLink>
            <NavLink to="/ultimate" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              <span className="icon">✨</span>
              Ultimate 4D
            </NavLink>
            <NavLink to="/settings" className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
              <span className="icon">⚙️</span>
              Settings
            </NavLink>
          </nav>

          {/* View Mode Toggle */}
          <div className="view-toggle">
            <button
              className={viewMode === '3d' ? 'active' : ''}
              onClick={() => setViewMode('3d')}
              title="3D View"
            >
              🎲 3D
            </button>
            <button
              className={viewMode === '4d' ? 'active' : ''}
              onClick={() => setViewMode('4d')}
              title="4D View (Ultimate)"
            >
              ✨ 4D
            </button>
            <button
              className={viewMode === 'table' ? 'active' : ''}
              onClick={() => setViewMode('table')}
              title="Table View (Fallback)"
            >
              📄 Table
            </button>
          </div>

          <div className="sidebar-footer">
            <p>v1.0.0</p>
            <p className="status-indicator">
              <span className="dot online"></span> Online
            </p>
          </div>
        </aside>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard viewMode={viewMode} />} />
            <Route path="/jobs" element={<JobsList viewMode={viewMode} />} />
            <Route path="/visualize" element={<RoomVisualization />} />
            <Route path="/ultimate" element={<UltimateVisualization />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
