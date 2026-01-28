import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import ErrorBoundary from './ErrorBoundary.jsx'
import './index.css'
import { loader } from "@monaco-editor/react";

// Configure Monaco to use local files (copied from public/vs to dist/vs)
// Using document.baseURI ensures it resolves correctly in both Dev (localhost) and Prod (file://)
// Configure Monaco to use local files
// In Electron with nodeIntegration: true, we must use file paths, NOT http urls
const path = require('path');

let vsPath;
if (import.meta.env.DEV) {
    // DEV: Use the local public/vs folder or node_modules
    // Currently public/vs is populated, so let's use that.
    vsPath = path.join(process.cwd(), 'public', 'vs');
} else {
    // PROD: The 'vs' folder is copied to extraResources
    // "to": "vs" relative to resources
    vsPath = path.join(process.resourcesPath, 'vs');
}

// Convert to file URI
const vsUri = `file:///${vsPath.replace(/\\/g, '/')}`;
console.log("[MONACO] Loading from:", vsUri);

loader.config({ paths: { vs: vsUri } });


ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <ErrorBoundary>
            <App />
        </ErrorBoundary>
    </React.StrictMode>,
)
