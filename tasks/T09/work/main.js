const { app, BrowserWindow, ipcMain, dialog } = require('electron')
const fs = require('fs-extra')
const path = require('path')

let mainWindow = null
let openedFileHandle = null

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 1200, height: 800,
    webPreferences: { preload: path.join(__dirname, 'preload.js'), contextIsolation: true, nodeIntegration: false }
  })
  mainWindow.loadFile(path.join(__dirname, 'renderer/index.html'))
}

ipcMain.handle('doc:new', async () => {
  openedFileHandle = null
  return true
})

ipcMain.handle('doc:open', async () => {
  const res = await dialog.showOpenDialog(mainWindow, { filters: [{ name: 'doc', extensions: ['txt', 'md'] }] })
  if (res.canceled) return null
  const filePath = res.filePaths[0]
  const fd = await fs.open(filePath, 'r+')
  openedFileHandle = fd
  const content = await fs.readFile(filePath, 'utf-8')
  return { content, filePath }
})

ipcMain.handle('doc:save', async (_, content) => {
  if (!openedFileHandle) return false
  await fs.writeFile(openedFileHandle, content, 'utf-8')
  return true
})

ipcMain.handle('doc:saveas', async (_, content) => {
  const res = await dialog.showSaveDialog(mainWindow)
  if (res.canceled) return false
  const fd = await fs.open(res.filePath, 'w+')
  openedFileHandle = fd
  await fs.writeFile(fd, content, 'utf-8')
  return true
})

ipcMain.handle('export:pdf', async (_, htmlContent) => {
  const pdfData = await mainWindow.webContents.printToPDF({})
  const savePath = await dialog.showSaveDialog(mainWindow, { filters: [{ name: 'PDF', extensions: ['pdf'] }] })
  if (savePath.canceled) return false
  await fs.writeFile(savePath.filePath, pdfData)
  return true
})

ipcMain.handle('print', async () => {
  mainWindow.webContents.print()
  return true
})

app.whenReady().then(createWindow)

app.on('window-all-closed', () => { app.quit() })
