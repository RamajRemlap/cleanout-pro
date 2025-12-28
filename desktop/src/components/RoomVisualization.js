import React, { useState, useEffect, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Text, Box } from '@react-three/drei';
import * as THREE from 'three';
import { apiService } from '../services/api';
import './RoomVisualization.css';

// 3D Room Cube Component
function RoomCube({ room, position, onClick, isSelected }) {
  const meshRef = useRef();
  const [hovered, setHovered] = useState(false);

  // Rotate the cube slowly
  useFrame((state, delta) => {
    if (meshRef.current && !isSelected) {
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  // Color based on workload
  const getColor = () => {
    if (isSelected) return '#00d4ff';
    if (hovered) return '#00ff88';

    const workload = room.final_workload_class || room.ai_workload_class || 'moderate';
    switch (workload) {
      case 'light': return '#00ff88';
      case 'moderate': return '#ffcc00';
      case 'heavy': return '#ff8800';
      case 'extreme': return '#ff4444';
      default: return '#666666';
    }
  };

  // Size based on room size class
  const getSize = () => {
    const sizeClass = room.final_size_class || room.ai_size_class || 'medium';
    switch (sizeClass) {
      case 'small': return 1;
      case 'medium': return 1.5;
      case 'large': return 2;
      case 'extra_large': return 2.5;
      default: return 1.5;
    }
  };

  const size = getSize();

  return (
    <group position={position}>
      {/* Main Cube */}
      <Box
        ref={meshRef}
        args={[size, size, size]}
        onClick={onClick}
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <meshStandardMaterial
          color={getColor()}
          emissive={getColor()}
          emissiveIntensity={hovered || isSelected ? 0.3 : 0.1}
          roughness={0.3}
          metalness={0.7}
        />
      </Box>

      {/* Room Name Label */}
      <Text
        position={[0, size + 0.5, 0]}
        fontSize={0.3}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
      >
        {room.name || `Room ${room.id}`}
      </Text>

      {/* Price Label */}
      <Text
        position={[0, -(size + 0.5), 0]}
        fontSize={0.25}
        color="#00d4ff"
        anchorX="center"
        anchorY="middle"
      >
        ${room.estimated_cost?.toLocaleString() || '0'}
      </Text>

      {/* Wireframe on hover */}
      {(hovered || isSelected) && (
        <Box args={[size + 0.1, size + 0.1, size + 0.1]}>
          <meshBasicMaterial color={getColor()} wireframe opacity={0.3} transparent />
        </Box>
      )}
    </group>
  );
}

// Main 3D Scene
function Scene({ rooms, selectedRoom, onRoomClick }) {
  const arrangeRooms = () => {
    const spacing = 4;
    const roomsPerRow = Math.ceil(Math.sqrt(rooms.length));

    return rooms.map((room, index) => {
      const row = Math.floor(index / roomsPerRow);
      const col = index % roomsPerRow;

      return {
        ...room,
        position: [
          (col - roomsPerRow / 2) * spacing,
          0,
          (row - Math.ceil(rooms.length / roomsPerRow) / 2) * spacing
        ]
      };
    });
  };

  const arrangedRooms = arrangeRooms();

  return (
    <>
      {/* Camera */}
      <PerspectiveCamera makeDefault position={[0, 8, 12]} fov={60} />

      {/* Controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={5}
        maxDistance={30}
      />

      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} castShadow />
      <pointLight position={[-10, -10, -5]} intensity={0.5} color="#00d4ff" />
      <hemisphereLight args={['#ffffff', '#000000', 0.3]} />

      {/* Grid Floor */}
      <gridHelper args={[40, 40, '#2a2a2a', '#1a1a1a']} />

      {/* Room Cubes */}
      {arrangedRooms.map((room) => (
        <RoomCube
          key={room.id}
          room={room}
          position={room.position}
          onClick={() => onRoomClick(room)}
          isSelected={selectedRoom?.id === room.id}
        />
      ))}

      {/* Background */}
      <color attach="background" args={['#0a0a0a']} />
      <fog attach="fog" args={['#0a0a0a', 10, 50]} />
    </>
  );
}

// Main Component
function RoomVisualization() {
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    try {
      setLoading(true);
      // For demo, create sample rooms if API fails
      try {
        const jobs = await apiService.getJobs();
        // TODO: Load actual rooms from jobs
        const allRooms = jobs.flatMap(job => job.rooms || []);

        if (allRooms.length === 0) {
          setRooms(createSampleRooms());
        } else {
          setRooms(allRooms);
        }
      } catch (err) {
        console.warn('API unavailable, showing demo rooms');
        setRooms(createSampleRooms());
      }

      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const createSampleRooms = () => {
    return [
      {
        id: 1,
        name: 'Master Bedroom',
        ai_size_class: 'large',
        ai_workload_class: 'heavy',
        final_size_class: 'large',
        final_workload_class: 'heavy',
        estimated_cost: 450,
        ai_confidence: 0.87
      },
      {
        id: 2,
        name: 'Living Room',
        ai_size_class: 'extra_large',
        ai_workload_class: 'moderate',
        final_size_class: 'extra_large',
        final_workload_class: 'moderate',
        estimated_cost: 585,
        ai_confidence: 0.92
      },
      {
        id: 3,
        name: 'Kitchen',
        ai_size_class: 'medium',
        ai_workload_class: 'heavy',
        final_size_class: 'medium',
        final_workload_class: 'heavy',
        estimated_cost: 351,
        ai_confidence: 0.79
      },
      {
        id: 4,
        name: 'Garage',
        ai_size_class: 'extra_large',
        ai_workload_class: 'extreme',
        final_size_class: 'extra_large',
        final_workload_class: 'extreme',
        estimated_cost: 900,
        ai_confidence: 0.85
      },
      {
        id: 5,
        name: 'Basement',
        ai_size_class: 'large',
        ai_workload_class: 'moderate',
        final_size_class: 'large',
        final_workload_class: 'moderate',
        estimated_cost: 390,
        ai_confidence: 0.88
      }
    ];
  };

  if (loading) {
    return (
      <div className="room-visualization">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading 3D visualization...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="room-visualization">
      <div className="page-header">
        <h2>3D Room Visualization</h2>
        <p>Interactive 3D view of all rooms in your jobs</p>
      </div>

      {error && (
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="visualization-container">
        {/* 3D Canvas */}
        <div className="canvas-container">
          <Canvas shadows>
            <Scene
              rooms={rooms}
              selectedRoom={selectedRoom}
              onRoomClick={setSelectedRoom}
            />
          </Canvas>

          {/* Controls Hint */}
          <div className="controls-hint">
            <p>🖱️ Left-click + drag to rotate</p>
            <p>⚙️ Right-click + drag to pan</p>
            <p>🔍 Scroll to zoom</p>
          </div>
        </div>

        {/* Room Details Sidebar */}
        <div className="details-sidebar">
          <h3>Room Details</h3>

          {selectedRoom ? (
            <div className="room-details">
              <div className="detail-item">
                <label>Room Name:</label>
                <span>{selectedRoom.name}</span>
              </div>

              <div className="detail-item">
                <label>Size Class:</label>
                <span className="badge size">{selectedRoom.final_size_class || selectedRoom.ai_size_class}</span>
              </div>

              <div className="detail-item">
                <label>Workload:</label>
                <span className={`badge workload ${selectedRoom.final_workload_class || selectedRoom.ai_workload_class}`}>
                  {selectedRoom.final_workload_class || selectedRoom.ai_workload_class}
                </span>
              </div>

              <div className="detail-item">
                <label>Estimated Cost:</label>
                <span className="cost">${selectedRoom.estimated_cost?.toLocaleString() || '0'}</span>
              </div>

              {selectedRoom.ai_confidence && (
                <div className="detail-item">
                  <label>AI Confidence:</label>
                  <span>{(selectedRoom.ai_confidence * 100).toFixed(0)}%</span>
                </div>
              )}

              <button className="btn btn-primary" style={{marginTop: '20px', width: '100%'}}>
                Edit Classification
              </button>
            </div>
          ) : (
            <div className="empty-selection">
              <p>Click on a room cube to view details</p>
            </div>
          )}

          {/* Legend */}
          <div className="legend">
            <h4>Workload Colors</h4>
            <div className="legend-item">
              <div className="color-box" style={{background: '#00ff88'}}></div>
              <span>Light</span>
            </div>
            <div className="legend-item">
              <div className="color-box" style={{background: '#ffcc00'}}></div>
              <span>Moderate</span>
            </div>
            <div className="legend-item">
              <div className="color-box" style={{background: '#ff8800'}}></div>
              <span>Heavy</span>
            </div>
            <div className="legend-item">
              <div className="color-box" style={{background: '#ff4444'}}></div>
              <span>Extreme</span>
            </div>
          </div>

          {/* Stats */}
          <div className="visualization-stats">
            <h4>Statistics</h4>
            <p>Total Rooms: <strong>{rooms.length}</strong></p>
            <p>Total Cost: <strong>${rooms.reduce((sum, r) => sum + (r.estimated_cost || 0), 0).toLocaleString()}</strong></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RoomVisualization;
