const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electron', {
  ipcRenderer: {
    agentIPC(message, callback) {
      const channel = 'agent-ipc';
      ipcRenderer.once(channel, callback);
      ipcRenderer.send(channel, message);
    },
    on(channel, func) {
      ipcRenderer.on(channel, (event, ...args) => func(...args));
    },
    once(channel, func) {
      ipcRenderer.once(channel, (event, ...args) => func(...args));
    },
    pythonLoadedCallback(callback) {
      ipcRenderer.on('python-ready', callback)
    }
  },
});
