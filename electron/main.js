const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      // --- IMPORTANT ---
      // Security Best Practices:
      // 1. Set contextIsolation to true.
      // 2. Do not set nodeIntegration to true.
      // 3. Use a preload script to expose limited functionality to the renderer.
      contextIsolation: true,
      nodeIntegration: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Load the React app
  win.loadURL('http://localhost:3000');

  // Open the DevTools.
  win.webContents.openDevTools();
}

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
