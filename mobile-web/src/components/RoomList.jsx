import { useEffect, useState } from 'react';
import { useStore } from '../store';
import api from '../api';

export default function RoomList({ onBack, onCapture, onViewRoom }) {
  const { currentJob, rooms, setRooms, setCurrentRoom } = useStore();
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    try {
      setLoading(true);
      const data = await api.getRooms(currentJob.id);
      setRooms(data);
    } catch (error) {
      console.error('Failed to load rooms:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadRooms();
    setRefreshing(false);
  };

  const handleRoomClick = (room) => {
    setCurrentRoom(room);
    onViewRoom();
  };

  if (loading) {
    return (
      <div>
        <div className="header">
          <button onClick={onBack} style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
            ← Back
          </button>
          <h1>Job #{currentJob?.job_number}</h1>
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
        <button onClick={onBack} style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          ← Back
        </button>
        <h1>Job #{currentJob?.job_number}</h1>
        <div className="header-subtitle">
          {rooms.length} {rooms.length === 1 ? 'room' : 'rooms'}
        </div>
      </div>

      <div className="content" style={{ paddingBottom: '100px' }}>
        <button
          onClick={handleRefresh}
          className="btn btn-secondary"
          disabled={refreshing}
          style={{ marginBottom: '1rem' }}>
          {refreshing ? 'Refreshing...' : '🔄 Refresh'}
        </button>

        {rooms.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📷</div>
            <div className="empty-state-text">No rooms captured yet</div>
            <div className="empty-state-subtext">Tap the camera button to add a room</div>
          </div>
        ) : (
          rooms.map((room) => {
            const sizeLabel = {
              small: 'S',
              medium: 'M',
              large: 'L',
              extra_large: 'XL',
            }[room.final_size_class];

            const workloadLabel = {
              light: 'Light',
              moderate: 'Moderate',
              heavy: 'Heavy',
              extreme: 'Extreme',
            }[room.final_workload_class];

            const confidenceColor =
              room.ai_confidence >= 0.7
                ? '#34C759'
                : room.ai_confidence >= 0.5
                ? '#FF9500'
                : '#FF3B30';

            return (
              <div key={room.id} className="card" onClick={() => handleRoomClick(room)}>
                {room.image_url && (
                  <img
                    src={room.image_url}
                    alt={room.name}
                    style={{
                      width: '100%',
                      height: '200px',
                      objectFit: 'cover',
                      borderRadius: '8px',
                      marginBottom: '1rem',
                    }}
                  />
                )}

                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: '0.5rem',
                  }}>
                  <h3 style={{ margin: 0 }}>{room.name}</h3>
                  <span className="badge badge-primary">{sizeLabel}</span>
                </div>

                <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.5rem' }}>
                  {workloadLabel} workload
                </div>

                {room.ai_confidence !== undefined && (
                  <div
                    style={{
                      fontSize: '0.875rem',
                      marginBottom: '0.5rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem',
                    }}>
                    <span style={{ color: '#666' }}>AI Confidence:</span>
                    <span style={{ color: confidenceColor, fontWeight: '600' }}>
                      {(room.ai_confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                )}

                {room.human_size_class && (
                  <div style={{ fontSize: '0.875rem', color: '#34C759', fontWeight: '600', marginBottom: '0.5rem' }}>
                    ✓ Human verified
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
                    ${room.estimated_cost.toFixed(2)}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>

      <button
        onClick={onCapture}
        className="btn btn-primary"
        style={{
          position: 'fixed',
          bottom: '1rem',
          left: '1rem',
          right: '1rem',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.2)',
        }}>
        📷 Add Room
      </button>
    </div>
  );
}
