console.log('[Preload] Preload script loaded successfully.');

const { contextBridge, ipcRenderer } = require('electron');

// Expose a limited set of APIs to the renderer process (your React app)
// This is the secure way to allow communication between front-end and back-end.
contextBridge.exposeInMainWorld('electronAPI', {
  // Example function: renderer can call this to send a message to the main process
  sendMessage: (message) => ipcRenderer.send('message-from-renderer', message),

  // Example listener: renderer can use this to listen for messages from the main process
  onMessage: (callback) => ipcRenderer.on('message-from-main', (event, ...args) => callback(...args)),
});

window.addEventListener('DOMContentLoaded', () => {
  console.log('[Preload] DOM content has been fully loaded.');
});
