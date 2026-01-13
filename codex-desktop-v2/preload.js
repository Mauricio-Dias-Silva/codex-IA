const { contextBridge, ipcRenderer } = require('electron');

// Since nodeIntegration is true, we don't strictly need contextBridge, but it's good practice.
// However, main.js has contextIsolation: false, so we can just attach to window if we want, 
// or let the react app import 'electron'.
// But `nodeIntegration: true` + `contextIsolation: false` means `window.require` works.
// The error "Unable to load preload" implies main.js wants it.

// Let's just expose IPC if contextIsolation was on, or just log.
console.log("Preload loaded");

// Expose ipcRenderer and paths to window for compatibility with our App.jsx
window.ipcRenderer = ipcRenderer;
window.electronPaths = {
    resourcesPath: process.resourcesPath
};
