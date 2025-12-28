import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './Dashboard.css';

function Dashboard({ viewMode }) {
  const [stats, setStats] = useState({
    totalJobs: 0,
    activeJobs: 0,
    completedJobs: 0,
    totalRevenue: 0,
  });
  const [recentJobs, setRecentJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Check API health
      try {
        const health = await apiService.healthCheck();
        setApiStatus(health.status === 'healthy' ? 'online' : 'degraded');
      } catch (err) {
        setApiStatus('offline');
      }

      // Load jobs data
      try {
        const jobs = await apiService.getJobs();

        // Calculate stats
        const active = jobs.filter(j => j.status === 'in_progress' || j.status === 'scheduled');
        const completed = jobs.filter(j => j.status === 'completed');
        const revenue = completed.reduce((sum, j) => sum + (j.final_price || 0), 0);

        setStats({
          totalJobs: jobs.length,
          activeJobs: active.length,
          completedJobs: completed.length,
          totalRevenue: revenue,
        });

        setRecentJobs(jobs.slice(0, 5));
      } catch (err) {
        // If jobs API fails, show demo data
        console.warn('Jobs API unavailable, showing demo data');
        setRecentJobs([]);
      }

      setLoading(false);
    } catch (err) {
      console.error('Dashboard error:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h2>Dashboard</h2>
        <p>Overview of your cleanout business</p>
      </div>

      {/* API Status Banner */}
      <div className={`api-status ${apiStatus}`}>
        <span className="status-dot"></span>
        <span>
          API Status: {apiStatus === 'online' ? '✓ Connected' : apiStatus === 'offline' ? '✗ Offline' : '⟳ Checking...'}
        </span>
        <span className="api-url">https://web-production-35f31.up.railway.app</span>
      </div>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <h3>{stats.totalJobs}</h3>
            <p>Total Jobs</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🚀</div>
          <div className="stat-content">
            <h3>{stats.activeJobs}</h3>
            <p>Active Jobs</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>{stats.completedJobs}</h3>
            <p>Completed</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💰</div>
          <div className="stat-content">
            <h3>${stats.totalRevenue.toLocaleString()}</h3>
            <p>Total Revenue</p>
          </div>
        </div>
      </div>

      {/* Recent Jobs */}
      <div className="card">
        <div className="card-header">
          <h3>Recent Jobs</h3>
          <button className="btn btn-secondary" onClick={loadDashboardData}>
            ⟳ Refresh
          </button>
        </div>

        {recentJobs.length === 0 ? (
          <div className="empty-state">
            <p>No jobs found. Create your first job to get started!</p>
            <button className="btn btn-primary">+ New Job</button>
          </div>
        ) : (
          <div className="jobs-list">
            {recentJobs.map((job) => (
              <div key={job.id} className="job-item">
                <div className="job-info">
                  <h4>{job.address || 'Unnamed Job'}</h4>
                  <p>Status: <span className={`status ${job.status}`}>{job.status}</span></p>
                </div>
                <div className="job-price">
                  ${job.final_price?.toLocaleString() || job.ai_estimate?.toLocaleString() || '0'}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* View Mode Indicator */}
      <div className="view-mode-info">
        <p>Current view mode: <strong>{viewMode === '3d' ? '3D Visualization' : 'Table View'}</strong></p>
        <p className="hint">Switch between 3D and Table view using the toggle in the sidebar</p>
      </div>
    </div>
  );
}

export default Dashboard;
