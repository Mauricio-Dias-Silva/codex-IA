import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import ErrorBoundary from './ErrorBoundary.jsx'
import './index.css'
import { loader } from "@monaco-editor/react";

// Configure Monaco to use local files (copied from public/vs to dist/vs)
// This prevents CDN issues and fixes "loader not defined" in production
loader.config({ paths: { vs: "./vs" } });


ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <ErrorBoundary>
            <App />
        </ErrorBoundary>
    </React.StrictMode>,
)
