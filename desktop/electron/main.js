const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development' || !app.isPackaged;

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 700,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    backgroundColor: '#1a1a1a',
    title: 'CleanoutPro - Job Management',
    icon: path.join(__dirname, '../assets/icon.png')
  });

  // Load React app
  if (isDev) {
    mainWindow.loadURL('http://localhost:3000');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../build/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Handle window events
  mainWindow.on('ready-to-show', () => {
    mainWindow.show();
    mainWindow.focus();
  });
}

// App lifecycle
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// IPC handlers for backend communication
ipcMain.handle('get-jobs', async () => {
  // This will be handled by the renderer process via fetch
  return { success: true };
});

ipcMain.handle('get-app-version', () => {
  return app.getVersion();
});

console.log('CleanoutPro Desktop starting...');
console.log('Environment:', isDev ? 'Development' : 'Production');
