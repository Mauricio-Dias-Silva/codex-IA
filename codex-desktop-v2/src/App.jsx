import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './components/Sidebar';
import CodexEditor from './components/Editor';
import CodexTerminal from './components/Terminal';
import MenuBar from './components/MenuBar';
import Missions from './components/Missions';
import AutoFix from './components/AutoFix';
import NightShift from './components/NightShift';
import DatabasePanel from './components/DatabasePanel';

const App = () => {
    // === STATE ===
    const [output, setOutput] = useState([]);
    const [terminalOutput, setTerminalOutput] = useState("");
    const [code, setCode] = useState("# Bem-vindo ao Codex-IA 2.0\n# O Cérebro PythonJet está Ativo.");
    const [projectPath, setProjectPath] = useState("C:\\Users\\Mauricio\\Desktop\\codex-IA");
    const [isProjectLoaded, setIsProjectLoaded] = useState(false);
    const [activeFile, setActiveFile] = useState("app.py");
    const [ipcConnected, setIpcConnected] = useState(false);

    // [FEATURE] VS Code Integration
    const [editorSettings, setEditorSettings] = useState({
        fontFamily: "'Fira Code', Consolas, monospace",
        fontSize: 14,
        theme: "vs-dark"
    });

    // View State
    const [activeView, setActiveView] = useState('editor');
    const [showTerminal, setShowTerminal] = useState(true);
    const [showSidebar, setShowSidebar] = useState(true); // New State

    // ... (rest of state items: fileTree, chat, etc.) keep them ...
    const [fileTree, setFileTree] = useState([]);
    const [chatInput, setChatInput] = useState("");
    const [chatHistory, setChatHistory] = useState([{ role: 'ai', content: "Olá! Eu sou o Codex. Abra um projeto para começar." }]);
    const [taskType, setTaskType] = useState("general");
    const [selectedImage, setSelectedImage] = useState(null);

    // ... (IPC Handling useEffects and Handlers) keep them ...
    // === IPC HANDLING ===
    useEffect(() => {
        if (window.ipcRenderer) {
            setIpcConnected(true);
            window.ipcRenderer.send('to-python', { command: 'get_vscode_settings' });
            window.ipcRenderer.on('python-output', (event, data) => {
                try {
                    const parsed = JSON.parse(data);
                    handleBackendResponse(parsed);
                } catch (e) {
                    console.warn("[IPC] Non-JSON output received from Python:", data);
                    // Handle non-JSON as log/terminal output
                    setTerminalOutput((prev) => prev + `\x1b[1;30m[PYTHON LOG] ${data}\x1b[0m\r\n`);
                }
            });
        }
    }, [projectPath]);

    const handleBackendResponse = (res) => {
        // ... (Keep existing handler logic) ...
        if (res.type === 'project_loaded') {
            setIsProjectLoaded(true);
            setProjectPath(res.path);
            setTerminalOutput(`\x1b[1;32m[SYSTEM] Project Loaded: ${res.path}\x1b[0m\r\n`);
            if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'get_file_tree', path: res.path });
        } else if (res.type === 'file_tree') {
            setFileTree(buildTree(res.files));
        } else if (res.type === 'vscode_settings') {
            setEditorSettings(prev => ({ ...prev, ...res.settings }));
            setTerminalOutput(`\x1b[1;36m[SYSTEM] Synced VS Code Settings: ${res.settings.fontFamily}\x1b[0m\r\n`);
        } else if (res.type === 'file_content') {
            setCode(res.content);
            setActiveFile(res.file);
        } else if (res.type === 'chat_response') {
            setChatHistory(prev => [...prev, { role: 'ai', content: res.text }]);
        } else if (res.type === 'shell_output') {
            const formatted = res.output.replace(/\n/g, '\r\n');
            setTerminalOutput(formatted);
        } else if (res.type === 'error') {
            setTerminalOutput(`\x1b[1;31m[ERROR] ${res.message}\x1b[0m\r\n`);
            if (res.message.includes('Cannot read binary')) setCode("// Arquivo binário ou não suportado.");
        }
    };

    const buildTree = (files) => {
        const root = { name: 'root', type: 'directory', children: [] };
        files.forEach(f => {
            const parts = f.path.split('\\').join('/').split('/');
            let current = root;
            parts.forEach((part, i) => {
                let existing = current.children.find(c => c.name === part);
                if (!existing) {
                    const isFile = i === parts.length - 1;
                    const newNode = { name: part, type: isFile ? 'file' : 'directory', path: f.path, children: isFile ? null : [] };
                    current.children.push(newNode);
                    current = newNode;
                } else { current = existing; }
            });
        });
        return root.children;
    };

    // Actions
    const sendChat = () => { if (chatInput.trim() && window.ipcRenderer) { setChatHistory(prev => [...prev, { role: 'user', content: chatInput }]); window.ipcRenderer.send('to-python', { command: 'agent_message', message: chatInput, task_type: taskType, image: selectedImage }); setChatInput(""); } };
    const runTerminalCommand = (cmd) => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'shell_exec', cmd: cmd, cwd: projectPath }); };
    const openFile = (fp) => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'read_file', file: fp, project_path: projectPath }); };
    const loadProject = () => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'set_project', path: projectPath }); else setIsProjectLoaded(true); };
    const saveFile = () => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'save_file', file: activeFile, content: code, project_path: projectPath }); };
    const createNewFile = () => {
        // prompt() is not supported in many Electron envs, using a default or we can add a proper modal later
        const filename = "novo_arquivo.py";
        if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'create_file', file: filename, project_path: projectPath });
    };
    const openNativeFolder = async () => {
        console.log("[DEBUG] openNativeFolder clicked");
        if (window.ipcRenderer) {
            try {
                const p = await window.ipcRenderer.invoke('dialog:openDirectory');
                console.log("[DEBUG] Folder selected:", p);
                if (p) {
                    setProjectPath(p);
                    window.ipcRenderer.send('to-python', { command: 'set_project', path: p });
                }
            } catch (err) {
                console.error("[DEBUG] Error opening folder:", err);
            }
        } else {
            console.error("[DEBUG] ipcRenderer not found");
        }
    };
    const deployProject = () => { if (window.ipcRenderer) { setTerminalOutput("\x1b[1;36m[CODEX AGENT] Requesting Deployment...\x1b[0m\r\n"); setShowTerminal(true); window.ipcRenderer.send('to-python', { command: 'deploy', path: projectPath }); } };
    const selectImage = () => { const i = document.createElement('input'); i.type = 'file'; i.accept = 'image/*'; i.onchange = (e) => { const f = e.target.files[0]; if (f) { const r = new FileReader(); r.onload = (ev) => setSelectedImage(ev.target.result); r.readAsDataURL(f); } }; i.click(); };

    const handleRefactor = (instructions) => {
        if (window.ipcRenderer) {
            setTerminalOutput(`\x1b[1;36m[CODEX AGENT] Refactoring ${activeFile}...\x1b[0m\r\n`);
            window.ipcRenderer.send('to-python', {
                command: 'refactor_file',
                file: activeFile,
                instructions: instructions,
                project_path: projectPath
            });
        }
    };

    // Neural Context
    const absorbProjects = () => {
        if (window.ipcRenderer) {
            setTerminalOutput("\x1b[1;35m[NEURAL AGENT] Absorbing Legacy Projects into Vector Memory...\x1b[0m\r\n");
            setShowTerminal(true);
            const legacyPaths = [
                "c:\\Users\\Mauricio\\Desktop\\sysgov-project",
                "c:\\Users\\Mauricio\\Desktop\\edufuturo",
                "c:\\Users\\Mauricio\\Desktop\\scalabis",
                "c:\\Users\\Mauricio\\Desktop\\painel-pythonjet",
                "c:\\Users\\Mauricio\\Desktop\\baassimulator"
            ];
            window.ipcRenderer.send('to-python', { command: 'absorb_projects', paths: legacyPaths });
        }
    };

    // Self-Healing
    const runAutoTests = () => {
        if (window.ipcRenderer) {
            setTerminalOutput("\x1b[1;33m[TESTER AGENT] Running Diagnostics & Auto-Healing...\x1b[0m\r\n");
            setShowTerminal(true);
            window.ipcRenderer.send('to-python', { command: 'run_auto_tests' });
        }
    };

    // === EDITOR API ===
    const editorRef = useRef(null);
    const onEditorMount = (editor) => { editorRef.current = editor; };

    const handleUndo = () => editorRef.current?.trigger('api', 'undo');
    const handleRedo = () => editorRef.current?.trigger('api', 'redo');
    const handleCut = () => { editorRef.current?.focus(); document.execCommand('cut'); };
    const handleCopy = () => { editorRef.current?.focus(); document.execCommand('copy'); };
    const handlePaste = () => { editorRef.current?.focus(); navigator.clipboard.readText().then(t => editorRef.current.trigger('keyboard', 'type', { text: t })); };

    // Zoom Logic
    const handleZoomIn = () => setEditorSettings(prev => ({ ...prev, fontSize: Math.min(prev.fontSize + 2, 32) }));
    const handleZoomOut = () => setEditorSettings(prev => ({ ...prev, fontSize: Math.max(prev.fontSize - 2, 8) }));

    // === RENDER ===
    return (
        <div className="flex h-screen bg-[#1e1e1e] text-[#cccccc] overflow-hidden flex-col">

            {/* NEW MENU BAR */}
            <MenuBar
                onNewFile={createNewFile}
                onOpenFile={openNativeFolder}
                onSave={saveFile}
                onExit={() => window.close()}
                onUndo={handleUndo}
                onRedo={handleRedo}
                onCut={handleCut}
                onCopy={handleCopy}
                onPaste={handlePaste}
                onToggleSidebar={() => setShowSidebar(!showSidebar)}
                onToggleTerminal={() => setShowTerminal(!showTerminal)}
                onZoomIn={handleZoomIn}
                onZoomOut={handleZoomOut}
                onRun={deployProject}
                onDebug={deployProject}
                onNewTerminal={() => runTerminalCommand('powershell')}
                onKillTerminal={() => setTerminalOutput('')}
                onAbout={() => alert("Codex Desktop V2.5\nPowered by Gemini & Antigravity")}
            />

            <div className="flex-1 flex overflow-hidden">
                {/* 1. SIDEBAR (Navigation & Files) */}
                {showSidebar && (
                    <div className={`flex flex-col border-r border-[#1e1e1e] ${isProjectLoaded ? 'w-80' : 'w-12'} transition-all`}>
                        <Sidebar
                            activeView={activeView} setActiveView={setActiveView}
                            isProjectLoaded={isProjectLoaded} loadProject={loadProject}
                            fileTree={fileTree} openFile={openFile}
                            chatHistory={chatHistory} chatInput={chatInput} setChatInput={setChatInput}
                            sendChat={sendChat} selectImage={selectImage} taskType={taskType} setTaskType={setTaskType}
                            selectedImage={selectedImage} setSelectedImage={setSelectedImage}
                            onAbsorbProjects={absorbProjects}
                            onRunTests={runAutoTests}
                        />
                    </div>
                )}

                {/* 2. MAIN CONTENT (Editor & Terminal & Missions) */}
                <div className="flex-1 flex flex-col min-w-0">

                    {/* DYNAMIC VIEW SWITCHER */}
                    <div className="flex-1 flex flex-col overflow-hidden relative">
                        {activeView === 'editor' && (
                            <CodexEditor
                                activeFile={activeFile}
                                code={code}
                                setCode={setCode}
                                isProjectLoaded={isProjectLoaded}
                                onLoadProject={loadProject}
                                onNewFile={createNewFile}
                                onOpenNativeFolder={openNativeFolder}
                                onRefactor={handleRefactor}
                                settings={editorSettings}
                                onEditorMount={onEditorMount}
                            />
                        )}
                        {activeView === 'missions' && (
                            <Missions />
                        )}
                        {activeView === 'night' && (
                            <NightShift />
                        )}
                        {activeView === 'database' && (
                            <DatabasePanel />
                        )}
                    </div>

                    {/* Terminal Panel (Bottom) */}
                    {showTerminal && isProjectLoaded && (
                        <div className="h-48 bg-[#1e1e1e] border-t border-[#3e3e3e] flex flex-col">
                            <div className="bg-[#252526] px-4 py-1 flex justify-between items-center text-[11px] font-bold text-[#bbb]">
                                <span>TERMINAL</span>
                                <button onClick={() => setShowTerminal(false)} className="hover:text-white">x</button>
                            </div>
                            <div className="flex-1 overflow-hidden">
                                <CodexTerminal
                                    onInput={runTerminalCommand}
                                    outputStream={terminalOutput}
                                />
                            </div>
                        </div>
                    )}
                </div>{/* Close Main Content */}
            </div>{/* Close Flex Row Wrapper */}

            {/* Status Bar */}
            <div className="bg-[#007acc] text-white flex items-center px-4 h-5 text-[10px] justify-between font-bold shrink-0 z-50">
                <div className="flex gap-4">
                    <span>{ipcConnected ? '⚡ CONNECTED' : '🔌 DISCONNECTED'}</span>
                    <span>{activeFile}</span>
                </div>
                <span>{taskType.toUpperCase()} MODE</span>
            </div>
        </div>
    );
};

export default App;

