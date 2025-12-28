import { useRef, useState, useEffect } from 'react';
import { useStore } from '../store';
import api from '../api';

export default function Camera({ onCapture, onCancel }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [captured, setCaptured] = useState(null);
  const [roomName, setRoomName] = useState('');
  const [uploading, setUploading] = useState(false);
  const { currentJob, rooms, addRoom } = useStore();

  useEffect(() => {
    startCamera();
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment', // Use back camera
          width: { ideal: 1920 },
          height: { ideal: 1080 },
        },
        audio: false,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setStream(mediaStream);
    } catch (error) {
      console.error('Camera error:', error);
      alert(
        'Camera access denied. Please allow camera permissions in your browser settings.'
      );
      onCancel();
    }
  };

  const handleCapture = () => {
    if (!videoRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    // Convert to blob
    canvas.toBlob((blob) => {
      setCaptured(blob);

      // Stop camera
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    }, 'image/jpeg', 0.9);
  };

  const handleRetake = () => {
    setCaptured(null);
    setRoomName('');
    startCamera();
  };

  const handleUpload = async () => {
    if (!roomName.trim() || !captured) {
      alert('Please enter a room name');
      return;
    }

    setUploading(true);

    try {
      const roomNumber = rooms.length + 1;
      const room = await api.uploadRoom(
        currentJob.id,
        roomName,
        roomNumber,
        captured
      );

      addRoom(room);

      alert(
        `✓ Room "${roomName}" uploaded!\n\n` +
        `Size: ${room.final_size_class}\n` +
        `Workload: ${room.final_workload_class}\n` +
        `Estimate: $${room.estimated_cost.toFixed(2)}\n` +
        `AI Confidence: ${((room.ai_confidence || 0) * 100).toFixed(0)}%`
      );

      onCapture();
    } catch (error) {
      console.error('Upload failed:', error);
      alert('Upload failed: ' + (error.response?.data?.detail || error.message));
    } finally {
      setUploading(false);
    }
  };

  if (captured) {
    return (
      <div className="camera-container">
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <img
            src={URL.createObjectURL(captured)}
            alt="Captured"
            style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
          />
        </div>

        <div
          style={{
            background: 'white',
            padding: '1.5rem',
            borderTopLeftRadius: '24px',
            borderTopRightRadius: '24px',
          }}>
          <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: '600' }}>
            Room Name
          </label>
          <input
            type="text"
            className="input"
            placeholder="e.g., Master Bedroom, Garage"
            value={roomName}
            onChange={(e) => setRoomName(e.target.value)}
            autoFocus
            style={{ marginBottom: '1rem' }}
          />

          <div style={{ fontSize: '0.875rem', color: '#666', marginBottom: '1rem' }}>
            Room #{rooms.length + 1} - AI will analyze the photo
          </div>

          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={handleRetake}
              className="btn btn-secondary"
              disabled={uploading}
              style={{ flex: 1 }}>
              Retake
            </button>
            <button
              onClick={handleUpload}
              className="btn btn-primary"
              disabled={uploading}
              style={{ flex: 2 }}>
              {uploading ? (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
                  <div className="spinner" style={{ width: '20px', height: '20px', borderWidth: '2px' }}></div>
                  Analyzing...
                </div>
              ) : (
                'Upload & Analyze'
              )}
            </button>
          </div>
        </div>

        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>
    );
  }

  return (
    <div className="camera-container">
      <video ref={videoRef} className="camera-video" autoPlay playsInline muted />

      {/* Guide overlay */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          pointerEvents: 'none',
        }}>
        <div
          style={{
            width: '80%',
            maxWidth: '400px',
            height: '60%',
            border: '2px solid rgba(255, 255, 255, 0.5)',
            borderRadius: '12px',
          }}
        />
        <div
          style={{
            marginTop: '1rem',
            background: 'rgba(0, 0, 0, 0.6)',
            color: 'white',
            padding: '0.5rem 1rem',
            borderRadius: '8px',
            fontSize: '1rem',
            fontWeight: '600',
          }}>
          Frame the room to capture all clutter
        </div>
      </div>

      {/* Controls */}
      <div className="camera-controls">
        <button
          onClick={onCancel}
          style={{
            color: 'white',
            fontSize: '1rem',
            padding: '0.75rem',
            fontWeight: '600',
          }}>
          Cancel
        </button>

        <button onClick={handleCapture} className="camera-btn">
          <div className="camera-btn-inner" />
        </button>

        <div style={{ width: '70px' }} />
      </div>

      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}
