# Codex IA Directory Map

This document explains the organization of the `codex-IA` folder.

## 📂 Core Components

### 1. `codex-desktop-v2/` (The Desktop App)
- **What it is:** The modern Electron/React interface for Codex.
- **Launcher:** `run_app.bat` (inside this folder).
- **Tech Stack:** Electron, React, Vite.
- **Status:** **ACTIVE**. Use this for the visual interface.

### 2. `codex_ia/` (The Brain)
- **What it is:** The Python package containing the intelligence (LLM logic, agents, tools).
- **Core Logic:** `codex_ia/core/` (Agent, BrainRouter, Skills).
- **Shared:** Used by both the Desktop App and the Cloud Server.

### 3. `codex_cli.py` (The Terminal Agent)
- **What it is:** A direct command-line interface to the Brain.
- **Launcher:** `run_codex.bat`.
- **Status:** **ACTIVE**. Use this for fast, text-only interaction.

---

## ☁️ Cloud & Server Components (VM / Port 8142)

### 4. `run_codex_server.bat` / `run_codex_server_v2.ps1`
- **What it is:** Scripts to launch the backend server acting as the "Brain API" for PythonJet or remote access.
- **Port:** Typically 8142.

### 5. `codex_web/`
- **What it is:** Web-specific interface/API endpoints (likely FastApi or Django integration) for the cloud version.

---

## 🗑️ Legacy / Archived

### 6. `_legacy_flet/`
- **What it is:** Archives of the old Flet-based interface which is no longer used.
- **Content:** `run_gui.bat`, `.spec` files, old build scripts.

---

## 🛠️ Configuration
- `.env`: API Keys (Gemini, etc.) - **CRITICAL**.
- `requirements.txt`: Python dependencies for the Brain.
