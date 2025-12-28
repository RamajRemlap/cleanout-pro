const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electron', {
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  getJobs: () => ipcRenderer.invoke('get-jobs'),
  // Add more IPC methods as needed
  platform: process.platform
});

console.log('Preload script loaded');
