import { useStore } from '../store';

export default function RoomDetail({ onBack }) {
  const { currentRoom } = useStore();

  if (!currentRoom) {
    return (
      <div>
        <div className="header">
          <button onClick={onBack} style={{ fontSize: '1.5rem' }}>
            ← Back
          </button>
          <h1>Room Details</h1>
        </div>
        <div className="content">
          <div className="empty-state">
            <div className="empty-state-text">Room not found</div>
          </div>
        </div>
      </div>
    );
  }

  const sizeLabels = {
    small: 'Small',
    medium: 'Medium',
    large: 'Large',
    extra_large: 'Extra Large',
  };

  const workloadLabels = {
    light: 'Light',
    moderate: 'Moderate',
    heavy: 'Heavy',
    extreme: 'Extreme',
  };

  return (
    <div>
      <div className="header">
        <button onClick={onBack} style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>
          ← Back
        </button>
        <h1>{currentRoom.name}</h1>
        <div className="header-subtitle">Room #{currentRoom.room_number}</div>
      </div>

      <div className="content">
        {currentRoom.image_url && (
          <img
            src={currentRoom.image_url}
            alt={currentRoom.name}
            style={{
              width: '100%',
              height: '300px',
              objectFit: 'cover',
              borderRadius: '12px',
              marginBottom: '1rem',
            }}
          />
        )}

        {/* Estimate */}
        <div
          className="card"
          style={{
            background: '#34C759',
            color: 'white',
            textAlign: 'center',
            padding: '1.5rem',
          }}>
          <div style={{ fontSize: '1rem', opacity: 0.9, marginBottom: '0.5rem' }}>
            Estimated Cost
          </div>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold' }}>
            ${currentRoom.estimated_cost.toFixed(2)}
          </div>
        </div>

        {/* Final Classification */}
        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>Final Classification</h3>
          <div style={{ display: 'flex', gap: '1rem' }}>
            <div style={{ flex: 1, background: '#f5f5f5', padding: '1rem', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.25rem' }}>
                Size
              </div>
              <div style={{ fontSize: '1.125rem', fontWeight: 'bold', color: '#007AFF' }}>
                {sizeLabels[currentRoom.final_size_class]}
              </div>
            </div>
            <div style={{ flex: 1, background: '#f5f5f5', padding: '1rem', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '0.25rem' }}>
                Workload
              </div>
              <div style={{ fontSize: '1.125rem', fontWeight: 'bold', color: '#007AFF' }}>
                {workloadLabels[currentRoom.final_workload_class]}
              </div>
            </div>
          </div>
        </div>

        {/* AI Analysis */}
        {currentRoom.ai_size_class && (
          <div className="card">
            <h3 style={{ marginBottom: '1rem' }}>AI Analysis</h3>

            <div style={{ marginBottom: '0.75rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f0f0f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Size Class:</span>
                <span style={{ fontWeight: '600' }}>{sizeLabels[currentRoom.ai_size_class]}</span>
              </div>
            </div>

            <div style={{ marginBottom: '0.75rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f0f0f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Workload Class:</span>
                <span style={{ fontWeight: '600' }}>
                  {workloadLabels[currentRoom.ai_workload_class]}
                </span>
              </div>
            </div>

            {currentRoom.ai_confidence !== undefined && (
              <div style={{ marginBottom: '0.75rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f0f0f0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#666' }}>Confidence:</span>
                  <span
                    style={{
                      fontWeight: '600',
                      color:
                        currentRoom.ai_confidence >= 0.7
                          ? '#34C759'
                          : currentRoom.ai_confidence >= 0.5
                          ? '#FF9500'
                          : '#FF3B30',
                    }}>
                    {(currentRoom.ai_confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            )}

            {currentRoom.ai_reasoning && (
              <div style={{ background: '#f5f5f5', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
                <div style={{ fontSize: '0.875rem', fontWeight: '600', color: '#666', marginBottom: '0.5rem' }}>
                  AI Reasoning:
                </div>
                <div style={{ fontSize: '0.875rem', lineHeight: '1.5' }}>
                  {currentRoom.ai_reasoning}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Human Override */}
        {currentRoom.human_size_class && (
          <div className="card">
            <h3 style={{ marginBottom: '1rem' }}>Human Verification ✓</h3>

            <div style={{ marginBottom: '0.75rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f0f0f0' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span style={{ color: '#666' }}>Adjusted Size:</span>
                <span style={{ fontWeight: '600' }}>
                  {sizeLabels[currentRoom.human_size_class]}
                </span>
              </div>
            </div>

            {currentRoom.human_workload_class && (
              <div style={{ marginBottom: '0.75rem', paddingBottom: '0.75rem', borderBottom: '1px solid #f0f0f0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: '#666' }}>Adjusted Workload:</span>
                  <span style={{ fontWeight: '600' }}>
                    {workloadLabels[currentRoom.human_workload_class]}
                  </span>
                </div>
              </div>
            )}

            {currentRoom.human_override_reason && (
              <div style={{ background: '#f5f5f5', padding: '1rem', borderRadius: '8px', marginTop: '1rem' }}>
                <div style={{ fontSize: '0.875rem', fontWeight: '600', color: '#666', marginBottom: '0.5rem' }}>
                  Reason:
                </div>
                <div style={{ fontSize: '0.875rem', lineHeight: '1.5' }}>
                  {currentRoom.human_override_reason}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Metadata */}
        <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid #e5e5e5' }}>
          <div style={{ fontSize: '0.875rem', color: '#999', marginBottom: '0.25rem' }}>
            Captured: {new Date(currentRoom.captured_at).toLocaleString()}
          </div>
          {currentRoom.processed_at && (
            <div style={{ fontSize: '0.875rem', color: '#999' }}>
              Processed: {new Date(currentRoom.processed_at).toLocaleString()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
