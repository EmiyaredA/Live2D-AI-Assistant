/**
 * Phase 2 desktop pet shell.
 * Loads the frontend chat/embed UI in a transparent always-on-top window.
 * See Open-LLM-VTuber-Web window-manager.ts for full pet mode behavior.
 */
const { app, BrowserWindow, screen } = require('electron')
const path = require('path')

const DEV_URL = process.env.ASSISTANT_FRONTEND_URL || 'http://localhost:5173/embed/?token=REPLACE_TOKEN'
const IS_DEV = process.argv.includes('--dev')

function createPetWindow() {
  const displays = screen.getAllDisplays()
  const bounds = displays.reduce(
    (acc, d) => ({
      x: Math.min(acc.x, d.bounds.x),
      y: Math.min(acc.y, d.bounds.y),
      width: Math.max(acc.width, d.bounds.x + d.bounds.width) - Math.min(acc.x, d.bounds.x),
      height: Math.max(acc.height, d.bounds.y + d.bounds.height) - Math.min(acc.y, d.bounds.y),
    }),
    { x: 0, y: 0, width: 0, height: 0 },
  )

  const win = new BrowserWindow({
    x: bounds.x,
    y: bounds.y,
    width: Math.min(420, bounds.width),
    height: Math.min(640, bounds.height),
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    hasShadow: false,
    resizable: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  })

  win.setBackgroundColor('#00000000')
  win.setAlwaysOnTop(true, 'screen-saver')
  win.loadURL(DEV_URL)

  if (IS_DEV) {
    win.webContents.openDevTools({ mode: 'detach' })
  }
}

app.whenReady().then(createPetWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
