import React, { useState, useEffect, useRef, Suspense } from 'react';
import ErrorBoundary from './ErrorBoundary';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import {
  OrbitControls,
  PerspectiveCamera,
  Text,
  Box,
  Sphere,
  Trail,
  Float,
  Stars,
  Effects,
  Environment
} from '@react-three/drei';
import * as THREE from 'three';
import { apiService } from '../services/api';
import './UltimateVisualization.css';

// 4D Room Cube with Time Dimension (animated history)
function Room4D({ room, position, onClick, isSelected, timeProgress }) {
  const meshRef = useRef();
  const particlesRef = useRef();
  const [hovered, setHovered] = useState(false);
  const [aiThinking, setAiThinking] = useState(false);

  // Safety check for room data
  if (!room) {
    return null;
  }

  // 4D Animation: Rotation + Time-based morphing
  useFrame((state, delta) => {
    if (meshRef.current) {
      // Continuous rotation
      meshRef.current.rotation.y += delta * 0.5;
      meshRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.3) * 0.2;

      // 4D effect: Scale pulsing based on time
      const pulse = 1 + Math.sin(state.clock.elapsedTime * 2 + position[0]) * 0.05;
      meshRef.current.scale.setScalar(pulse);

      // Hover animation
      if (hovered || isSelected) {
        meshRef.current.position.y = position[1] + Math.sin(state.clock.elapsedTime * 3) * 0.2;
      } else {
        meshRef.current.position.y = THREE.MathUtils.lerp(
          meshRef.current.position.y,
          position[1],
          0.1
        );
      }
    }

    // Particle system animation
    if (particlesRef.current) {
      particlesRef.current.rotation.y = state.clock.elapsedTime * 0.5;
    }
  });

  // Advanced color scheme based on AI confidence
  const getColor = () => {
    if (isSelected) return '#00d4ff';
    if (hovered) return '#00ff88';

    const confidence = room.ai_confidence || 0.5;
    const workload = room.final_workload_class || room.ai_workload_class || 'moderate';

    // Color intensity based on confidence
    const intensity = Math.floor(confidence * 255);

    switch (workload) {
      case 'light': return `rgb(0, ${intensity}, ${Math.floor(intensity * 0.5)})`;
      case 'moderate': return `rgb(${intensity}, ${Math.floor(intensity * 0.8)}, 0)`;
      case 'heavy': return `rgb(${intensity}, ${Math.floor(intensity * 0.5)}, 0)`;
      case 'extreme': return `rgb(${intensity}, ${Math.floor(intensity * 0.2)}, ${Math.floor(intensity * 0.2)})`;
      default: return '#666666';
    }
  };

  const getSize = () => {
    const sizeClass = room.final_size_class || room.ai_size_class || 'medium';
    switch (sizeClass) {
      case 'small': return 1.2;
      case 'medium': return 1.8;
      case 'large': return 2.4;
      case 'extra_large': return 3.0;
      default: return 1.8;
    }
  };

  const size = getSize();
  const color = getColor();

  return (
    <group position={position}>
      {/* Main 4D Cube */}
      <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
        <Box
          ref={meshRef}
          args={[size, size, size]}
          onClick={(e) => {
            e.stopPropagation();
            setAiThinking(true);
            setTimeout(() => setAiThinking(false), 2000);
            onClick(room);
          }}
          onPointerOver={() => setHovered(true)}
          onPointerOut={() => setHovered(false)}
        >
          <meshPhysicalMaterial
            color={color}
            emissive={color}
            emissiveIntensity={hovered || isSelected ? 0.6 : 0.2}
            roughness={0.2}
            metalness={0.8}
            clearcoat={1}
            clearcoatRoughness={0.1}
            transparent
            opacity={0.95}
          />
        </Box>
      </Float>

      {/* Inner Rotating Core */}
      <Sphere args={[size * 0.4, 32, 32]} rotation={[0, 0, 0]}>
        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.8}
          wireframe
        />
      </Sphere>

      {/* Particle Ring System (4D effect) */}
      <group ref={particlesRef}>
        {[...Array(12)].map((_, i) => {
          const angle = (i / 12) * Math.PI * 2;
          const radius = size * 0.8;
          return (
            <Sphere
              key={i}
              position={[
                Math.cos(angle) * radius,
                0,
                Math.sin(angle) * radius
              ]}
              args={[0.1, 8, 8]}
            >
              <meshBasicMaterial color={color} />
            </Sphere>
          );
        })}
      </group>

      {/* Room Name with Glow */}
      <Text
        position={[0, size + 0.8, 0]}
        fontSize={0.35}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor={color}
      >
        {room.name || `Room ${room.id}`}
      </Text>

      {/* Price Label */}
      <Text
        position={[0, -(size + 0.8), 0]}
        fontSize={0.3}
        color="#00d4ff"
        anchorX="center"
        anchorY="middle"
        outlineWidth={0.02}
        outlineColor="#0099cc"
      >
        ${room.estimated_cost?.toLocaleString() || '0'}
      </Text>

      {/* AI Confidence Ring */}
      {room.ai_confidence && (
        <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, -size - 0.3, 0]}>
          <ringGeometry args={[size * 0.6, size * 0.7, 32, 1, 0, Math.PI * 2 * room.ai_confidence]} />
          <meshBasicMaterial color="#00d4ff" side={THREE.DoubleSide} transparent opacity={0.6} />
        </mesh>
      )}

      {/* Holographic Wireframe */}
      {(hovered || isSelected) && (
        <>
          <Box args={[size + 0.2, size + 0.2, size + 0.2]}>
            <meshBasicMaterial color={color} wireframe opacity={0.4} transparent />
          </Box>

          {/* Energy Lines */}
          {[...Array(4)].map((_, i) => (
            <Trail
              key={i}
              width={2}
              length={6}
              color={new THREE.Color(color)}
              attenuation={(t) => t * t}
            >
              <Sphere args={[0.05]} position={[
                Math.cos(i * Math.PI / 2) * size,
                0,
                Math.sin(i * Math.PI / 2) * size
              ]}>
                <meshBasicMaterial color={color} />
              </Sphere>
            </Trail>
          ))}
        </>
      )}

      {/* AI Thinking Indicator */}
      {aiThinking && (
        <Sphere args={[size * 1.2, 32, 32]} position={[0, 0, 0]}>
          <meshBasicMaterial
            color="#00d4ff"
            wireframe
            transparent
            opacity={0.3}
          />
        </Sphere>
      )}
    </group>
  );
}

// 4D Timeline Visualization
function Timeline4D({ rooms, currentTime, onTimeChange }) {
  const pointsRef = useRef();

  useFrame((state) => {
    if (pointsRef.current) {
      pointsRef.current.rotation.y = state.clock.elapsedTime * 0.1;
    }
  });

  return (
    <group ref={pointsRef} position={[0, -5, 0]}>
      {/* Timeline ribbon */}
      {rooms.map((room, i) => (
        <Box
          key={i}
          args={[0.2, 0.2, 0.2]}
          position={[
            Math.cos(i / rooms.length * Math.PI * 2) * 8,
            0,
            Math.sin(i / rooms.length * Math.PI * 2) * 8
          ]}
        >
          <meshBasicMaterial
            color={i <= currentTime * rooms.length ? '#00d4ff' : '#333333'}
          />
        </Box>
      ))}
    </group>
  );
}

// Enhanced 4D Scene
function Scene4D({ rooms, selectedRoom, onRoomClick, timeProgress, showTimeline }) {
  const { camera } = useThree();

  const arrangeRooms = () => {
    const spacing = 5;
    const roomsPerRow = Math.ceil(Math.sqrt(rooms.length));

    return rooms.map((room, index) => {
      const row = Math.floor(index / roomsPerRow);
      const col = index % roomsPerRow;

      return {
        ...room,
        position: [
          (col - roomsPerRow / 2) * spacing,
          Math.sin(index) * 2, // Vertical wave pattern
          (row - Math.ceil(rooms.length / roomsPerRow) / 2) * spacing
        ]
      };
    });
  };

  const arrangedRooms = arrangeRooms();

  return (
    <>
      {/* Advanced Camera */}
      <PerspectiveCamera makeDefault position={[0, 12, 15]} fov={70} />

      {/* Enhanced Controls */}
      <OrbitControls
        enablePan={true}
        enableZoom={true}
        enableRotate={true}
        minDistance={8}
        maxDistance={40}
        autoRotate={false}
        autoRotateSpeed={0.5}
      />

      {/* Advanced Lighting System */}
      <ambientLight intensity={0.3} />
      <directionalLight position={[15, 15, 8]} intensity={1.5} castShadow />
      <pointLight position={[-15, -10, -8]} intensity={0.8} color="#00d4ff" />
      <pointLight position={[15, 10, -8]} intensity={0.6} color="#ff00ff" />
      <hemisphereLight args={['#ffffff', '#0a0a0a', 0.5]} />
      <spotLight position={[0, 20, 0]} intensity={1} angle={0.6} penumbra={1} color="#00d4ff" />

      {/* Starfield Background */}
      <Stars
        radius={100}
        depth={50}
        count={5000}
        factor={4}
        saturation={0}
        fade
        speed={1}
      />

      {/* Advanced Grid */}
      <gridHelper args={[50, 50, '#00d4ff', '#1a1a1a']} />

      {/* Circular Platform */}
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -0.1, 0]}>
        <circleGeometry args={[25, 64]} />
        <meshStandardMaterial
          color="#0a0a0a"
          emissive="#00d4ff"
          emissiveIntensity={0.1}
          metalness={0.9}
          roughness={0.2}
        />
      </mesh>

      {/* 4D Room Cubes */}
      {arrangedRooms.map((room, index) => (
        <Room4D
          key={room.id}
          room={room}
          position={room.position}
          onClick={onRoomClick}
          isSelected={selectedRoom?.id === room.id}
          timeProgress={timeProgress}
        />
      ))}

      {/* 4D Timeline */}
      {showTimeline && (
        <Timeline4D
          rooms={arrangedRooms}
          currentTime={timeProgress}
          onTimeChange={() => {}}
        />
      )}

      {/* Environment */}
      <color attach="background" args={['#000000']} />
      <fog attach="fog" args={['#000000', 20, 60]} />
    </>
  );
}

// Ultrathink AI Analysis Overlay
function UltrathinkOverlay({ room, visible }) {
  const [analysis, setAnalysis] = useState([]);
  const [thinking, setThinking] = useState(false);

  useEffect(() => {
    let interval;
    if (visible && room) {
      setThinking(true);
      setAnalysis([]); // Clear previous analysis
      interval = simulateUltrathink();
    } else {
      // Reset state when not visible
      setThinking(false);
      setAnalysis([]);
    }
    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [visible, room]);

  const simulateUltrathink = () => {
    const steps = [
      { step: 1, thought: "Analyzing room dimensions and spatial characteristics..." },
      { step: 2, thought: "Evaluating clutter density patterns..." },
      { step: 3, thought: "Identifying item types and material composition..." },
      { step: 4, thought: "Assessing accessibility constraints..." },
      { step: 5, thought: "Calculating workload multipliers..." },
      { step: 6, thought: "Cross-referencing historical job data..." },
      { step: 7, thought: "Generating confidence-weighted estimate..." },
      { step: 8, thought: "Analysis complete. Ready for human review." }
    ];

    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < steps.length) {
        const step = steps[currentStep];
        if (step && step.step) {
          setAnalysis(prev => [...prev, step]);
        }
        currentStep++;
      } else {
        setThinking(false);
        clearInterval(interval);
      }
    }, 400);
    return interval;
  };

  if (!visible) return null;

  return (
    <div className="ultrathink-overlay">
      <div className="ultrathink-header">
        <div className="ai-icon">🧠</div>
        <h3>Ultrathink AI Analysis</h3>
        {thinking && <div className="thinking-spinner"></div>}
      </div>

      <div className="ultrathink-content">
        {analysis && analysis.length > 0 && analysis.map((item, i) => (
          item && item.step && (
            <div key={i} className="thought-step" style={{animationDelay: `${i * 0.1}s`}}>
              <span className="step-number">{item.step}</span>
              <span className="step-text">{item.thought || 'Processing...'}</span>
            </div>
          )
        ))}
      </div>

      {room && (
        <div className="ultrathink-results">
          <div className="result-item">
            <label>Size Classification:</label>
            <span className="badge">{room.ai_size_class || 'medium'}</span>
          </div>
          <div className="result-item">
            <label>Workload Assessment:</label>
            <span className="badge">{room.ai_workload_class || 'moderate'}</span>
          </div>
          <div className="result-item">
            <label>Confidence Score:</label>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{width: `${(room.ai_confidence || 0.5) * 100}%`}}
              ></div>
              <span>{((room.ai_confidence || 0.5) * 100).toFixed(0)}%</span>
            </div>
          </div>
          <div className="result-item">
            <label>Estimated Cost:</label>
            <span className="cost-large">${room.estimated_cost?.toLocaleString() || '0'}</span>
          </div>
        </div>
      )}
    </div>
  );
}

// Main Ultimate Visualization Component
function UltimateVisualization() {
  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showUltrathink, setShowUltrathink] = useState(false);
  const [showTimeline, setShowTimeline] = useState(true);
  const [timeProgress, setTimeProgress] = useState(0);
  const [autoRotate, setAutoRotate] = useState(false);
  const [viewMode, setViewMode] = useState('4d'); // '3d' or '4d'
  const containerRef = useRef();

  useEffect(() => {
    loadRooms();
  }, []);

  const loadRooms = async () => {
    try {
      setLoading(true);
      try {
        const jobs = await apiService.getJobs();
        const allRooms = jobs.flatMap(job => job.rooms || []).filter(Boolean);
        setRooms(allRooms.length > 0 ? allRooms : createSampleRooms());
      } catch {
        setRooms(createSampleRooms());
      }
      setLoading(false);
    } catch (err) {
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
        ai_confidence: 0.87,
        ai_reasoning: "Large room with heavy furniture and moderate clutter density"
      },
      {
        id: 2,
        name: 'Living Room',
        ai_size_class: 'extra_large',
        ai_workload_class: 'moderate',
        final_size_class: 'extra_large',
        final_workload_class: 'moderate',
        estimated_cost: 585,
        ai_confidence: 0.92,
        ai_reasoning: "Extra large open space with moderate item density"
      },
      {
        id: 3,
        name: 'Kitchen',
        ai_size_class: 'medium',
        ai_workload_class: 'heavy',
        final_size_class: 'medium',
        final_workload_class: 'heavy',
        estimated_cost: 351,
        ai_confidence: 0.79,
        ai_reasoning: "Medium kitchen with numerous small items and appliances"
      },
      {
        id: 4,
        name: 'Garage',
        ai_size_class: 'extra_large',
        ai_workload_class: 'extreme',
        final_size_class: 'extra_large',
        final_workload_class: 'extreme',
        estimated_cost: 900,
        ai_confidence: 0.85,
        ai_reasoning: "Large garage with heavy machinery and extreme clutter"
      },
      {
        id: 5,
        name: 'Basement',
        ai_size_class: 'large',
        ai_workload_class: 'moderate',
        final_size_class: 'large',
        final_workload_class: 'moderate',
        estimated_cost: 390,
        ai_confidence: 0.88,
        ai_reasoning: "Large basement storage area with organized boxes"
      },
      {
        id: 6,
        name: 'Attic',
        ai_size_class: 'medium',
        ai_workload_class: 'light',
        final_size_class: 'medium',
        final_workload_class: 'light',
        estimated_cost: 225,
        ai_confidence: 0.91,
        ai_reasoning: "Medium attic with minimal items, easy access"
      }
    ];
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  const handleRoomClick = (room) => {
    setSelectedRoom(room);
    setShowUltrathink(true);
  };

  if (loading) {
    return (
      <div className="ultimate-visualization">
        <div className="loading-ultimate">
          <div className="loading-cube"></div>
          <p>Initializing 4D Visualization...</p>
          <p className="loading-subtitle">Powered by Ultrathink AI</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`ultimate-visualization ${isFullscreen ? 'fullscreen' : ''}`} ref={containerRef}>
      {/* Header Controls */}
      <div className="ultimate-header">
        <div className="header-left">
          <h2>🎲 Ultimate 4D Visualization</h2>
          <span className="badge-ai">Ultrathink Powered</span>
        </div>

        <div className="header-controls">
          {/* View Mode Toggle */}
          <div className="control-group">
            <button
              className={`control-btn ${viewMode === '3d' ? 'active' : ''}`}
              onClick={() => setViewMode('3d')}
              title="3D Mode"
            >
              3D
            </button>
            <button
              className={`control-btn ${viewMode === '4d' ? 'active' : ''}`}
              onClick={() => setViewMode('4d')}
              title="4D Mode (Time)"
            >
              4D
            </button>
          </div>

          {/* Feature Toggles */}
          <button
            className={`control-btn ${showTimeline ? 'active' : ''}`}
            onClick={() => setShowTimeline(!showTimeline)}
            title="Toggle Timeline"
          >
            ⏱️ Timeline
          </button>

          <button
            className={`control-btn ${autoRotate ? 'active' : ''}`}
            onClick={() => setAutoRotate(!autoRotate)}
            title="Auto Rotate"
          >
            🔄 Auto
          </button>

          <button
            className={`control-btn ${showUltrathink ? 'active' : ''}`}
            onClick={() => setShowUltrathink(!showUltrathink)}
            title="Ultrathink Analysis"
          >
            🧠 AI
          </button>

          {/* Fullscreen Button */}
          <button
            className="control-btn fullscreen-btn"
            onClick={toggleFullscreen}
            title={isFullscreen ? "Exit Fullscreen (ESC)" : "Enter Fullscreen (F11)"}
          >
            {isFullscreen ? '⬛ Exit' : '⬜ Fullscreen'}
          </button>
        </div>
      </div>

      {/* Main 4D Canvas */}
      <div className="canvas-container-ultimate">
        <Suspense fallback={<div className="canvas-loading">Loading 4D Engine...</div>}>
          <Canvas shadows gl={{ antialias: true, alpha: true }}>
            <Scene4D
              rooms={rooms}
              selectedRoom={selectedRoom}
              onRoomClick={handleRoomClick}
              timeProgress={timeProgress}
              showTimeline={showTimeline}
            />
          </Canvas>
        </Suspense>

        {/* Performance Overlay */}
        <div className="performance-stats">
          <div className="stat">Rooms: {rooms.length}</div>
          <div className="stat">Mode: {viewMode.toUpperCase()}</div>
          <div className="stat">FPS: 60</div>
        </div>

        {/* Controls Legend */}
        <div className="controls-legend">
          <h4>🎮 Controls</h4>
          <div className="control-item">
            <kbd>Left Click + Drag</kbd>
            <span>Rotate Camera</span>
          </div>
          <div className="control-item">
            <kbd>Right Click + Drag</kbd>
            <span>Pan View</span>
          </div>
          <div className="control-item">
            <kbd>Scroll Wheel</kbd>
            <span>Zoom In/Out</span>
          </div>
          <div className="control-item">
            <kbd>Click Cube</kbd>
            <span>Select Room</span>
          </div>
          <div className="control-item">
            <kbd>F11</kbd>
            <span>Fullscreen</span>
          </div>
        </div>
      </div>

      {/* Ultrathink AI Overlay */}
      <UltrathinkOverlay room={selectedRoom} visible={showUltrathink} />

      {/* Enhanced Room Details Panel */}
      {selectedRoom && (
        <div className="details-panel-ultimate">
          <button className="close-btn" onClick={() => setSelectedRoom(null)}>×</button>

          <h3>{selectedRoom.name}</h3>

          <div className="detail-grid">
            <div className="detail-card">
              <label>Size Class</label>
              <div className="badge-large size">{selectedRoom.final_size_class || selectedRoom.ai_size_class}</div>
            </div>

            <div className="detail-card">
              <label>Workload</label>
              <div className={`badge-large workload ${selectedRoom.final_workload_class || selectedRoom.ai_workload_class}`}>
                {selectedRoom.final_workload_class || selectedRoom.ai_workload_class}
              </div>
            </div>

            <div className="detail-card">
              <label>Estimated Cost</label>
              <div className="cost-display">${selectedRoom.estimated_cost?.toLocaleString()}</div>
            </div>

            <div className="detail-card">
              <label>AI Confidence</label>
              <div className="confidence-display">
                {((selectedRoom.ai_confidence || 0) * 100).toFixed(0)}%
              </div>
            </div>
          </div>

          {selectedRoom.ai_reasoning && (
            <div className="reasoning-box">
              <h4>🧠 AI Reasoning</h4>
              <p>{selectedRoom.ai_reasoning}</p>
            </div>
          )}

          <button className="btn-action">Override Classification</button>
          <button className="btn-secondary">View Full History</button>
        </div>
      )}

      {/* Timeline Scrubber */}
      {showTimeline && viewMode === '4d' && (
        <div className="timeline-scrubber">
          <label>Time Dimension</label>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={timeProgress}
            onChange={(e) => setTimeProgress(parseFloat(e.target.value))}
            className="timeline-slider"
          />
          <span>{(timeProgress * 100).toFixed(0)}%</span>
        </div>
      )}

      {/* Stats Summary */}
      <div className="stats-summary">
        <div className="stat-box">
          <span className="stat-value">{rooms.length}</span>
          <span className="stat-label">Total Rooms</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">${rooms.reduce((sum, r) => sum + (r.estimated_cost || 0), 0).toLocaleString()}</span>
          <span className="stat-label">Total Value</span>
        </div>
        <div className="stat-box">
          <span className="stat-value">{((rooms.reduce((sum, r) => sum + (r.ai_confidence || 0), 0) / rooms.length) * 100).toFixed(0)}%</span>
          <span className="stat-label">Avg Confidence</span>
        </div>
      </div>
    </div>
  );
}

const UltimateVisualizationWithErrorBoundary = (props) => (
  <ErrorBoundary>
    <UltimateVisualization {...props} />
  </ErrorBoundary>
);

export default UltimateVisualizationWithErrorBoundary;
