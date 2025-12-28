import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './JobsList.css';

function JobsList({ viewMode }) {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all', 'scheduled', 'in_progress', 'completed'

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      setLoading(true);
      setError(null);

      const jobsData = await apiService.getJobs();
      setJobs(jobsData);
      setLoading(false);
    } catch (err) {
      console.error('Failed to load jobs:', err);
      // Show demo data on error
      setJobs(createDemoJobs());
      setError('Could not connect to API. Showing demo data.');
      setLoading(false);
    }
  };

  const createDemoJobs = () => {
    return [
      {
        id: 1,
        customer_id: 1,
        address: '123 Main St, Springfield',
        scheduled_date: '2024-01-15',
        status: 'scheduled',
        base_estimate: 1500,
        ai_estimate: 1650,
        final_price: 1650,
        created_at: '2024-01-10T10:00:00Z'
      },
      {
        id: 2,
        customer_id: 2,
        address: '456 Oak Ave, Portland',
        scheduled_date: '2024-01-12',
        status: 'in_progress',
        base_estimate: 2200,
        ai_estimate: 2450,
        final_price: 2450,
        created_at: '2024-01-08T14:30:00Z'
      },
      {
        id: 3,
        customer_id: 3,
        address: '789 Pine Rd, Seattle',
        scheduled_date: '2024-01-05',
        status: 'completed',
        base_estimate: 1800,
        ai_estimate: 1950,
        final_price: 1950,
        created_at: '2024-01-02T09:15:00Z'
      }
    ];
  };

  const filteredJobs = jobs.filter(job => {
    if (filter === 'all') return true;
    return job.status === filter;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'scheduled': return '#ffcc00';
      case 'in_progress': return '#00d4ff';
      case 'completed': return '#00ff88';
      case 'cancelled': return '#ff4444';
      default: return '#666666';
    }
  };

  if (loading) {
    return (
      <div className="jobs-list-page">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading jobs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="jobs-list-page">
      <div className="page-header">
        <h2>Jobs</h2>
        <p>Manage all your cleanout jobs</p>
      </div>

      {error && (
        <div className="error">
          <strong>Note:</strong> {error}
        </div>
      )}

      {/* Filters */}
      <div className="filters">
        <button
          className={filter === 'all' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('all')}
        >
          All ({jobs.length})
        </button>
        <button
          className={filter === 'scheduled' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('scheduled')}
        >
          Scheduled ({jobs.filter(j => j.status === 'scheduled').length})
        </button>
        <button
          className={filter === 'in_progress' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('in_progress')}
        >
          In Progress ({jobs.filter(j => j.status === 'in_progress').length})
        </button>
        <button
          className={filter === 'completed' ? 'filter-btn active' : 'filter-btn'}
          onClick={() => setFilter('completed')}
        >
          Completed ({jobs.filter(j => j.status === 'completed').length})
        </button>

        <button className="btn btn-primary" style={{marginLeft: 'auto'}}>
          + New Job
        </button>
      </div>

      {/* View Mode: Table or 3D */}
      {viewMode === 'table' ? (
        <div className="table-view">
          <table className="jobs-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Address</th>
                <th>Scheduled Date</th>
                <th>Status</th>
                <th>Estimate</th>
                <th>Final Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredJobs.length === 0 ? (
                <tr>
                  <td colSpan="7" className="empty-table">
                    No jobs found with status: {filter}
                  </td>
                </tr>
              ) : (
                filteredJobs.map((job) => (
                  <tr key={job.id}>
                    <td>#{job.id}</td>
                    <td>{job.address || 'N/A'}</td>
                    <td>{job.scheduled_date ? new Date(job.scheduled_date).toLocaleDateString() : 'Not scheduled'}</td>
                    <td>
                      <span className={`status-badge ${job.status}`} style={{background: getStatusColor(job.status)}}>
                        {job.status}
                      </span>
                    </td>
                    <td>${job.ai_estimate?.toLocaleString() || job.base_estimate?.toLocaleString() || '0'}</td>
                    <td className="price">${job.final_price?.toLocaleString() || '0'}</td>
                    <td>
                      <button className="action-btn">View</button>
                      <button className="action-btn">Edit</button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="card-view">
          {filteredJobs.length === 0 ? (
            <div className="empty-state">
              <p>No jobs found with status: {filter}</p>
            </div>
          ) : (
            <div className="jobs-grid">
              {filteredJobs.map((job) => (
                <div key={job.id} className="job-card">
                  <div className="job-card-header">
                    <span className="job-id">#{job.id}</span>
                    <span className={`status-badge ${job.status}`} style={{background: getStatusColor(job.status)}}>
                      {job.status}
                    </span>
                  </div>

                  <div className="job-card-body">
                    <h3>{job.address || 'Unnamed Job'}</h3>

                    <div className="job-info-grid">
                      <div className="info-item">
                        <label>Scheduled:</label>
                        <span>{job.scheduled_date ? new Date(job.scheduled_date).toLocaleDateString() : 'Not set'}</span>
                      </div>
                      <div className="info-item">
                        <label>Estimate:</label>
                        <span>${job.ai_estimate?.toLocaleString() || job.base_estimate?.toLocaleString() || '0'}</span>
                      </div>
                      <div className="info-item">
                        <label>Final Price:</label>
                        <span className="final-price">${job.final_price?.toLocaleString() || '0'}</span>
                      </div>
                    </div>
                  </div>

                  <div className="job-card-footer">
                    <button className="btn btn-secondary">View Details</button>
                    <button className="btn btn-primary">Edit Job</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Summary */}
      <div className="jobs-summary">
        <p>Showing <strong>{filteredJobs.length}</strong> of <strong>{jobs.length}</strong> jobs</p>
        <p>Total Value: <strong>${jobs.reduce((sum, j) => sum + (j.final_price || 0), 0).toLocaleString()}</strong></p>
      </div>
    </div>
  );
}

export default JobsList;
