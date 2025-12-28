import { useEffect, useState } from 'react';
import { useStore } from '../store';
import api from '../api';

export default function JobList({ onSelectJob }) {
  const { jobs, setJobs, setCurrentJob, apiUrl, setApiUrl, loading, setLoading } = useStore();
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    api.setBaseURL(apiUrl);
    loadJobs();
  }, [apiUrl]);

  const loadJobs = async () => {
    try {
      setLoading(true);
      const data = await api.getJobs();
      setJobs(data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
      alert('Failed to connect to backend. Please check API URL.');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadJobs();
    setRefreshing(false);
  };

  const handleSelectJob = (job) => {
    setCurrentJob(job);
    onSelectJob();
  };

  const handleChangeApiUrl = () => {
    const url = prompt('Enter backend API URL:', apiUrl);
    if (url) {
      setApiUrl(url);
      localStorage.setItem('api_url', url);
      loadJobs();
    }
  };

  if (loading && jobs.length === 0) {
    return (
      <div>
        <div className="header">
          <h1>CleanoutPro</h1>
          <div className="header-subtitle">Loading jobs...</div>
        </div>
        <div className="loading">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="header">
        <h1>CleanoutPro</h1>
        <div className="header-subtitle">{jobs.length} active jobs</div>
        <button
          onClick={handleChangeApiUrl}
          style={{
            fontSize: '0.75rem',
            color: '#007AFF',
            marginTop: '0.5rem',
            padding: '0.25rem',
          }}>
          Change API URL
        </button>
      </div>

      <div className="content">
        <button
          onClick={handleRefresh}
          className="btn btn-secondary"
          disabled={refreshing}
          style={{ marginBottom: '1rem' }}>
          {refreshing ? 'Refreshing...' : '🔄 Refresh'}
        </button>

        {jobs.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📋</div>
            <div className="empty-state-text">No jobs found</div>
            <div className="empty-state-subtext">Pull down to refresh</div>
          </div>
        ) : (
          jobs.map((job) => (
            <div key={job.id} className="card" onClick={() => handleSelectJob(job)}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '0.5rem',
                }}>
                <h3 style={{ margin: 0 }}>#{job.job_number}</h3>
                <span
                  className={`badge badge-${
                    job.status === 'scheduled'
                      ? 'primary'
                      : job.status === 'in_progress'
                      ? 'warning'
                      : job.status === 'completed'
                      ? 'success'
                      : 'danger'
                  }`}>
                  {job.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>

              {job.customer && (
                <>
                  <div style={{ fontSize: '1rem', fontWeight: '600', marginBottom: '0.25rem' }}>
                    {job.customer.name}
                  </div>
                  {job.customer.address && (
                    <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>
                      {job.customer.address}
                    </div>
                  )}
                </>
              )}

              {job.scheduled_date && (
                <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>
                  📅 {new Date(job.scheduled_date).toLocaleDateString()}
                </div>
              )}

              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: '0.75rem',
                  paddingTop: '0.75rem',
                  borderTop: '1px solid #f0f0f0',
                }}>
                <span style={{ fontSize: '0.875rem', color: '#666' }}>Estimate:</span>
                <span style={{ fontSize: '1.25rem', fontWeight: 'bold', color: '#34C759' }}>
                  ${job.ai_estimate?.toFixed(2) || '0.00'}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
