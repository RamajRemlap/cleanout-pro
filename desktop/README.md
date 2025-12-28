# CleanoutPro Desktop

**AI-Powered Cleanout Business Management with 3D Visualization**

A modern Electron + React desktop application featuring interactive 3D room visualization powered by Three.js.

## Features

- **3D Room Visualization**: Interactive 3D cubes representing rooms with color-coded workload indicators
- **Table View Fallback**: Traditional table view for when visualization isn't needed
- **Job Management**: Create, view, edit, and track cleanout jobs
- **Real-time API Integration**: Connects to your CleanoutPro backend
- **Dashboard**: Overview of business metrics and recent jobs
- **Dark Theme**: Modern, professional UI optimized for desktop use

## Tech Stack

- **Electron**: Cross-platform desktop framework
- **React**: UI framework
- **Three.js + React Three Fiber**: 3D graphics
- **@react-three/drei**: 3D helpers and components
- **Axios**: HTTP client for API calls
- **React Router**: Navigation

## Quick Start

### Installation

```bash
# Navigate to desktop directory
cd desktop

# Install dependencies
npm install
```

### Development

```bash
# Start development server (React + Electron)
npm start
```

This will:
1. Start the React development server on `http://localhost:3000`
2. Launch the Electron app window

### Building for Production

```bash
# Build React app
npm run build

# Package Electron app
npm run build:electron
```

## Configuration

### API URL

The app connects to your backend API. Configure the URL in Settings or set environment variable:

```bash
# .env file
REACT_APP_API_URL=https://your-backend-url.com
```

Default: `https://web-production-35f31.up.railway.app`

## 3D Visualization

### Controls

- **Rotate**: Left-click + drag
- **Pan**: Right-click + drag
- **Zoom**: Mouse scroll wheel

### Room Colors

Rooms are color-coded by workload:
- 🟢 **Green**: Light workload
- 🟡 **Yellow**: Moderate workload
- 🟠 **Orange**: Heavy workload
- 🔴 **Red**: Extreme workload

### Room Sizes

Cube size represents room size class:
- **Small**: 1x cube
- **Medium**: 1.5x cube
- **Large**: 2x cube
- **Extra Large**: 2.5x cube

## Project Structure

```
desktop/
├── electron/           # Electron main process
│   ├── main.js        # Entry point
│   └── preload.js     # Security bridge
├── public/            # Static assets
├── src/
│   ├── components/    # React components
│   │   ├── Dashboard.js
│   │   ├── JobsList.js
│   │   ├── RoomVisualization.js  # 3D scene
│   │   └── Settings.js
│   ├── services/      # API service
│   │   └── api.js
│   ├── App.js         # Main app component
│   ├── App.css        # Global styles
│   └── index.js       # React entry point
└── package.json
```

## API Endpoints Used

- `GET /health` - Health check
- `GET /api/jobs` - List all jobs
- `GET /api/jobs/:id` - Get job details
- `GET /api/jobs/:id/rooms` - Get rooms for a job
- `POST /api/jobs` - Create new job
- `PUT /api/jobs/:id` - Update job
- `DELETE /api/jobs/:id` - Delete job

## Troubleshooting

### App Won't Start

1. Ensure dependencies are installed: `npm install`
2. Check Node.js version: `node --version` (requires v16+)
3. Clear cache: `rm -rf node_modules && npm install`

### 3D View Not Loading

1. Check browser console for errors (View → Toggle Developer Tools)
2. Ensure WebGL is supported: Visit `chrome://gpu` in Chrome
3. Update graphics drivers

### API Connection Errors

1. Check API URL in Settings
2. Verify backend is running and accessible
3. Check CORS settings on backend

## Development Tips

### Hot Reload

Changes to React components will hot-reload automatically. For Electron changes, restart the app.

### DevTools

Press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac) to open DevTools.

### Debug 3D Scene

The 3D canvas includes OrbitControls debugging. Check console for camera position and rotation.

## Building for Distribution

### Windows

```bash
npm run build:electron
# Output: dist/CleanoutPro Setup.exe
```

### macOS

```bash
npm run build:electron
# Output: dist/CleanoutPro.dmg
```

### Linux

```bash
npm run build:electron
# Output: dist/CleanoutPro.AppImage
```

## License

MIT

## Support

For issues and questions:
- GitHub Issues: [cleanout-pro/issues](https://github.com/your-repo/cleanout-pro/issues)
- Documentation: See `CLAUDE.md` in root directory
