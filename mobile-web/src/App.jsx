import { useState, useEffect } from 'react';
import JobList from './components/JobList';
import RoomList from './components/RoomList';
import Camera from './components/Camera';
import RoomDetail from './components/RoomDetail';
import { useStore } from './store';

function App() {
  const [view, setView] = useState('jobs'); // 'jobs', 'rooms', 'camera', 'detail'
  const { currentJob, setApiUrl } = useStore();

  useEffect(() => {
    // Configure API URL from environment or prompt
    const savedApiUrl = localStorage.getItem('api_url');
    if (savedApiUrl) {
      setApiUrl(savedApiUrl);
    } else {
      // Prompt for API URL on first launch
      const url = prompt(
        'Enter your backend API URL:\n\n' +
        'Local: http://localhost:8000\n' +
        'Railway: https://your-app.railway.app\n' +
        'Render: https://your-app.onrender.com'
      );
      if (url) {
        setApiUrl(url);
        localStorage.setItem('api_url', url);
      }
    }
  }, [setApiUrl]);

  const renderView = () => {
    switch (view) {
      case 'jobs':
        return <JobList onSelectJob={() => setView('rooms')} />;
      case 'rooms':
        return (
          <RoomList
            onBack={() => setView('jobs')}
            onCapture={() => setView('camera')}
            onViewRoom={() => setView('detail')}
          />
        );
      case 'camera':
        return (
          <Camera
            onCapture={() => setView('rooms')}
            onCancel={() => setView('rooms')}
          />
        );
      case 'detail':
        return <RoomDetail onBack={() => setView('rooms')} />;
      default:
        return <JobList onSelectJob={() => setView('rooms')} />;
    }
  };

  return <div className="app">{renderView()}</div>;
}

export default App;
