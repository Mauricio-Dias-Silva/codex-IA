const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs'); // Added for VS Code Settings
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 800,
        titleBarStyle: 'hidden', // macOS style / custom header
        titleBarOverlay: {
            color: '#1e293b',
            symbolColor: '#ffffff'
        },
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // For easier prototyping
            preload: path.join(__dirname, 'preload.js'),
            webSecurity: false // Allow loading resources from CDN/External sources without CORS issues
        },
        backgroundColor: '#1e293b',
        icon: path.join(__dirname, 'assets/icon.png')
    });

    // Load React App (Dev mode vs Prod)
    // Load React App
    if (app.isPackaged) {
        // PROD: Load static files
        const distPath = path.join(__dirname, 'dist', 'index.html');
        mainWindow.loadFile(distPath);
        console.log(`[PROD] Loaded static interface: ${distPath}`);
    } else {
        // DEV: Load Vite Server (Hot Reload)
        // Ensure you run 'npm run dev' in a separate terminal!
        mainWindow.loadURL('http://localhost:5174');
        console.log('[DEV] Loaded Vite Server: http://localhost:5174');

        // Open DevTools automatically in Dev
        mainWindow.webContents.openDevTools();
    }

    // DEBUG: Force Open DevTools
    mainWindow.webContents.openDevTools();

    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function startPythonBackend() {
    // Spawn Python process
    const pythonCmd = 'python'; // Assumes python is in PATH for now
    let scriptPath;
    let cwd;

    if (app.isPackaged) {
        // In Prod: resources/backend/app.py
        scriptPath = path.join(process.resourcesPath, 'backend', 'app.py');
        cwd = path.join(process.resourcesPath, 'backend');
    } else {
        // In Dev: backend/app.py
        scriptPath = path.join(__dirname, 'backend', 'app.py');
        cwd = path.join(__dirname, 'backend');
    }

    console.log(`Starting Python Backend: ${scriptPath}`);

    pythonProcess = spawn(pythonCmd, [scriptPath], {
        cwd: cwd,
        stdio: ['pipe', 'pipe', 'pipe'], // Stdin, Stdout, Stderr
        env: {
            ...process.env,
            PYTHONIOENCODING: 'utf-8'
        }
    });

    let dataBuffer = '';
    pythonProcess.stdout.on('data', (data) => {
        dataBuffer += data.toString();

        let boundary = dataBuffer.indexOf('\n');
        while (boundary !== -1) {
            const message = dataBuffer.substring(0, boundary);
            dataBuffer = dataBuffer.substring(boundary + 1);

            console.log(`[PYTHON]: ${message}`);
            if (mainWindow) {
                mainWindow.webContents.send('python-output', message);
            }

            boundary = dataBuffer.indexOf('\n');
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`[PYTHON ERR]: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`Python process exited with code ${code}`);
    });
}

const killPythonSubprocesses = (mainPid) => {
    const exec = require('child_process').exec;
    // Windows specific kill
    exec(`taskkill /pid ${mainPid} /T /F`);
};


app.on('ready', () => {
    createWindow();
    startPythonBackend();
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        if (pythonProcess) {
            killPythonSubprocesses(pythonProcess.pid);
        }
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) createWindow();
});

// IPC Handling
ipcMain.on('to-python', (event, args) => {
    if (pythonProcess && pythonProcess.stdin) {
        pythonProcess.stdin.write(JSON.stringify(args) + '\n');
    }
});

ipcMain.handle('dialog:openDirectory', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
        properties: ['openDirectory']
    });
    if (canceled) {
        return null;
    } else {
        return filePaths[0];
    }
});

ipcMain.handle('vscode:readSettings', async () => {
    try {
        const settingsPath = path.join(process.env.APPDATA, 'Code', 'User', 'settings.json');
        if (fs.existsSync(settingsPath)) {
            const data = fs.readFileSync(settingsPath, 'utf-8');
            // Remove comments (JSONC) roughly or just try parsing
            // VS Code uses JSON with comments. Simple strip:
            const jsonContent = data.replace(/\/\/.*|\/\*[\s\S]*?\*\//g, "");
            return JSON.parse(jsonContent);
        }
    } catch (e) {
        console.error("Failed to read VS Code settings:", e);
    }
    return null;
});
