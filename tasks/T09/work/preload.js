const { contextBridge, ipcRenderer } = require('electron')
contextBridge.exposeInMainWorld('editorApi', {
  newDoc: () => ipcRenderer.invoke('doc:new'),
  openDoc: () => ipcRenderer.invoke('doc:open'),
  saveDoc: (content) => ipcRenderer.invoke('doc:save', content),
  saveAsDoc: (content) => ipcRenderer.invoke('doc:saveas', content),
  exportPdf: (html) => ipcRenderer.invoke('export:pdf', html),
  print: () => ipcRenderer.invoke('print')
})
