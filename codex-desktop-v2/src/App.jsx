import React, { useState, useEffect, useRef } from 'react';
import Editor, { loader } from "@monaco-editor/react";
import {
    Folder, FileCode, Search, Settings,
    ChevronRight, ChevronDown, Play,
    Terminal, Bot, Cloud, Send,
    Image, Code, Sparkles, AlertTriangle
} from 'lucide-react';

// VS CODE THEME CONSTANTS
// Activity Bar: #333333
// Sidebar: #252526
// Editor Group Header: #2d2d2d
// Editor: #1e1e1e
// Status Bar: #007acc (Blue) or #7160e8 (Purple for Ascension)

// FIX: Load Monaco from local assets
// In production (Electron packaged), use absolute path from process.resourcesPath
// In development, use relative './vs'
const getMonacoPath = () => {
    if (window.electronPaths && window.electronPaths.resourcesPath) {
        // Production: file:///C:/.../resources/vs
        return `file:///${window.electronPaths.resourcesPath.replace(/\\/g, '/')}/vs`;
    }
    return './vs'; // Development
};

loader.config({ paths: { vs: getMonacoPath() } });

const FileTreeNode = ({ node, onFileClick, depth = 0 }) => {
    const [isOpen, setIsOpen] = useState(false);

    // Sort: Directories first, then files
    const sortedChildren = node.children
        ? [...node.children].sort((a, b) => (a.type === b.type ? a.name.localeCompare(b.name) : a.type === 'directory' ? -1 : 1))
        : [];

    if (node.type === 'file') {
        // Git Colors (Phase 6)
        let textColor = "#cccccc";
        let statusLabel = null;

        if (node.status === 'modified') {
            textColor = "#e2c08d"; // VS Code Yellow
            statusLabel = "M";
        } else if (node.status === 'untracked') {
            textColor = "#73c991"; // VS Code Green
            statusLabel = "U";
        }

        return (
            <div
                className="flex items-center gap-1 py-0.5 px-3 hover:bg-[#2a2d2e] cursor-pointer hover:text-white transition text-[13px] group"
                style={{ paddingLeft: `${depth * 12 + 12}px`, color: textColor }}
                onClick={() => onFileClick(node.path)}
            >
                <FileCode size={14} className="min-w-[14px]" style={{ color: node.status ? textColor : "#519aba" }} />
                <span className="truncate flex-1">{node.name}</span>
                {statusLabel && <span className="text-[9px] font-bold opacity-0 group-hover:opacity-100 ml-2">{statusLabel}</span>}
            </div>
        );
    }

    return (
        <div>
            <div
                className="flex items-center gap-1 py-0.5 px-3 hover:bg-[#2a2d2e] cursor-pointer text-[#cccccc] hover:text-white transition text-[13px] font-bold"
                style={{ paddingLeft: `${depth * 12 + 12}px` }}
                onClick={() => setIsOpen(!isOpen)}
            >
                {isOpen ? <ChevronDown size={14} className="min-w-[14px]" /> : <ChevronRight size={14} className="min-w-[14px]" />}
                <Folder size={14} className={`${isOpen ? 'text-[#dcb67a]' : 'text-[#dcb67a]'} min-w-[14px]`} />
                <span className="truncate">{node.name}</span>
            </div>
            {isOpen && (
                <div>
                    {sortedChildren.map((child, i) => (
                        <FileTreeNode key={i} node={child} onFileClick={onFileClick} depth={depth + 1} />
                    ))}
                </div>
            )}
        </div>
    );

};

// Filling The Void: The Welcome Dashboard
const WelcomeDashboard = ({ onOpenProject, onNewFile, onOpenManual }) => {
    return (
        <div className="h-full flex flex-col items-center justify-center bg-[#1e1e1e] relative overflow-hidden select-none">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-b from-[#1e1e1e] via-[#252526] to-[#1e1e1e]" />
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[#61dafb] opacity-[0.03] rounded-full blur-[100px] animate-pulse-glow pointer-events-none" />

            {/* Core Content */}
            <div className="z-10 flex flex-col items-center animate-slide-down">
                <div className="mb-8 relative">
                    <div className="w-24 h-24 rounded-full border-2 border-[#007acc] flex items-center justify-center animate-pulse-glow shadow-[0_0_30px_rgba(0,122,204,0.5)]">
                        <Sparkles size={48} className="text-[#007acc] animate-spin-slow" />
                    </div>
                    <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                        <span className="text-[10px] font-mono text-[#007acc] tracking-[0.2em] uppercase glow-text">Output Log</span>
                    </div>
                </div>

                <h1 className="text-4xl font-bold text-white mb-2 tracking-tight glow-text font-sans">Codex-IA Desktop <span className="text-[#007acc]">V2</span></h1>
                <p className="text-[#666] text-lg mb-10 font-light">Seu Estúdio de Criação Autônoma</p>

                <div className="grid grid-cols-2 gap-4 w-[500px]">
                    <div onClick={onOpenProject} className="bg-[#252526] border border-[#333] hover:border-[#007acc] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2">
                            <Folder className="text-[#dcb67a] group-hover:scale-110 transition" size={24} />
                            <span className="font-bold text-[#ccc] group-hover:text-white">Abrir Projeto</span>
                        </div>
                        <div className="text-xs text-[#666]">Selecionar pasta local</div>
                    </div>

                    <div onClick={onNewFile} className="bg-[#252526] border border-[#333] hover:border-[#4ec9b0] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2">
                            <FileCode className="text-[#4ec9b0] group-hover:scale-110 transition" size={24} />
                            <span className="font-bold text-[#ccc] group-hover:text-white">Novo Arquivo</span>
                        </div>
                        <div className="text-xs text-[#666]">Criar script Python/JS</div>
                    </div>

                    <div onClick={() => window.ipcRenderer?.send('to-python', { command: 'trigger_ascension' })} className="bg-[#252526] border border-[#333] hover:border-[#dcdcaa] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2">
                            <Sparkles className="text-[#dcdcaa] group-hover:scale-110 transition" size={24} />
                            <span className="font-bold text-[#ccc] group-hover:text-white">Evoluir Sistema</span>
                        </div>
                        <div className="text-xs text-[#666]">Otimização Avançada (Level 13)</div>
                    </div>

                    <div onClick={onOpenManual} className="bg-[#252526] border border-[#333] hover:border-[#c586c0] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2">
                            <Bot className="text-[#c586c0] group-hover:scale-110 transition" size={24} />
                            <span className="font-bold text-[#ccc] group-hover:text-white">Manual</span>
                        </div>
                        <div className="text-xs text-[#666]">Documentação Oficial</div>
                    </div>
                </div>

                <div className="mt-12 text-[#444] text-xs font-mono max-w-md text-center italic">
                    "Code is not just logic. It is the language of creation."
                </div>
            </div>
        </div>
    );
};

const App = () => {
    const [output, setOutput] = useState([]);
    const [code, setCode] = useState("# Bem-vindo ao Codex-IA 2.0\n# O Cérebro PythonJet está Ativo.");
    const [projectPath, setProjectPath] = useState("C:\\Users\\Mauricio\\Desktop\\codex-IA");
    const [isProjectLoaded, setIsProjectLoaded] = useState(false);
    const [activeFile, setActiveFile] = useState("app.py");
    const [ipcConnected, setIpcConnected] = useState(false);
    const [terminalInput, setTerminalInput] = useState(""); // Terminal Input

    // UI States
    const [activeView, setActiveView] = useState('editor');
    const [sidebarTab, setSidebarTab] = useState('files');
    const [activeMenu, setActiveMenu] = useState(null); // 'file', 'edit', 'view' etc.
    const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false); // UX Quantum Leap
    const [vsCodeSettings, setVsCodeSettings] = useState(null); // VS Code Sync

    // File System State
    const [fileTree, setFileTree] = useState([]);

    // Chat State
    const [chatInput, setChatInput] = useState("");
    const [chatHistory, setChatHistory] = useState([
        { role: 'ai', content: "Olá! Eu sou o Codex. Abra um projeto para começar." }
    ]);
    const chatEndRef = useRef(null);

    // Mission State
    const [missionInput, setMissionInput] = useState("");
    const [missionLog, setMissionLog] = useState([]);

    // Night Shift State
    const [nightLog, setNightLog] = useState([]);
    const [isNightShiftRunning, setIsNightShiftRunning] = useState(false);

    // Ascension State (Levels 6, 9, 10, Cloud)
    const [ascensionLog, setAscensionLog] = useState([]);
    const [ascensionInput, setAscensionInput] = useState(""); // Input for Founder/Strategy
    const [selectedImage, setSelectedImage] = useState(null); // base64
    const [deployStatus, setDeployStatus] = useState(null); // idle, building, pushing, done

    // IPC with Electron

    useEffect(() => {
        if (window.ipcRenderer) {
            setIpcConnected(true);

            // UX Quantum Leap: Sync VS Code Settings
            window.ipcRenderer.invoke('vscode:readSettings').then(settings => {
                if (settings) {
                    console.log("VS Code Settings Synced:", settings);
                    setVsCodeSettings(settings);
                }
            });

            window.ipcRenderer.on('python-output', (event, data) => {
                try {
                    const response = JSON.parse(data);
                    handleBackendResponse(response);
                } catch (e) {
                    // Raw string output fallback
                    setOutput(prev => [...prev, data]);
                }
            });
        }
    }, []);

    const handleBackendResponse = (res) => {
        if (res.type === 'project_loaded') {
            setIsProjectLoaded(true);
            setOutput(prev => [...prev, `[SISTEMA] Projeto carregado: ${res.path}`]);
            setChatHistory(prev => [...prev, { role: 'ai', content: `Projeto carregado: ${res.path}. Cérebro inicializado.` }]);
            // Request file tree
            if (window.ipcRenderer) {
                window.ipcRenderer.send('to-python', { command: 'get_file_tree', path: res.path });
            }
        } else if (res.type === 'file_tree') {
            const tree = buildTree(res.files);
            setFileTree(tree);
        } else if (res.type === 'file_content') {
            setCode(res.content);
            setActiveFile(res.file);
        } else if (res.type === 'chat_response') {
            setChatHistory(prev => [...prev, { role: 'ai', content: res.text }]);
        } else if (res.type === 'mission_update') {
            setMissionLog(prev => [...prev, `[${res.status}] ${res.message}`]);
        } else if (res.type === 'mission_result') {
            setMissionLog(prev => [...prev, `[COMPLETO] Relatório da Missão: ${JSON.stringify(res.report, null, 2)}`]);
        } else if (res.type === 'night_shift_log') {
            setNightLog(prev => [...prev, res.message]);
        } else if (res.type === 'night_shift_complete') {
            setNightLog(prev => [...prev, "✅ Ciclo do Turno da Noite Completo."]);
            setIsNightShiftRunning(false);
        } else if (res.type === 'ascension_log') {
            setAscensionLog(prev => [...prev, res.message]);
        } else if (res.type === 'ascension_complete') {
            setAscensionLog(prev => [...prev, `✅ Tarefa ${res.agent} Concluída.`]);
        } else if (res.type === 'deploy_status') {
            setOutput(prev => [...prev, `[DEPLOY] ${res.message}`]);
            if (res.status === 'pushing') setDeployStatus('Enviando...');
        } else if (res.type === 'deploy_complete') {
            setOutput(prev => [...prev, `[DEPLOY] SUCESSO! Online em: ${res.url}`]);
            alert(`Implantação Bem-sucedida!\nURL: ${res.url}`);
            setDeployStatus(null);
        } else if (res.type === 'save_success') {
            setOutput(prev => [...prev, `[FILE] Salvo: ${res.file}`]);
        } else if (res.type === 'create_success') {
            setOutput(prev => [...prev, `[FILE] Criado: ${res.file}`]);
            // Trigger tree refresh
            if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'get_file_tree', path: projectPath });
        } else if (res.type === 'shell_output') {
            setOutput(prev => [...prev, res.output]);
        } else if (res.type === 'error') {
            setOutput(prev => [...prev, `[ERRO] ${res.message}`]);
            if (activeView === 'missions') setMissionLog(prev => [...prev, `❌ Erro: ${res.message}`]);
            if (activeView === 'night') setNightLog(prev => [...prev, `❌ Erro: ${res.message}`]);
            if (activeView === 'ascension') setAscensionLog(prev => [...prev, `❌ Erro: ${res.message}`]);
        } else {
            setOutput(prev => [...prev, JSON.stringify(res)]);
        }
    };

    // Helper to build tree from paths
    const buildTree = (paths) => {
        const root = { name: 'root', type: 'directory', children: [] };

        paths.forEach(path => {
            const parts = path.split('\\').join('/').split('/'); // Handle windows paths
            let current = root;

            parts.forEach((part, index) => {
                let existing = current.children.find(c => c.name === part);
                if (!existing) {
                    const isFile = index === parts.length - 1; // Assuming last part is file for simplicity involved in this context
                    const newNode = {
                        name: part,
                        type: isFile ? 'file' : 'directory',
                        path: path,
                        children: isFile ? null : []
                    };
                    current.children.push(newNode);
                    current = newNode;
                } else {
                    current = existing;
                }
            });
        });
        return root.children; // Return top level items
    };

    // Auto-scroll chat
    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [chatHistory]);

    const loadProject = () => {
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: 'set_project', path: projectPath });
        } else {
            setOutput(prev => [...prev, "Simulado: Carregando Projeto..."]);
            setIsProjectLoaded(true);
        }
    };

    const openFile = (filePath) => {
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: 'read_file', file: filePath, project_path: projectPath });
        }
    };

    const sendChat = () => {
        if (!chatInput.trim()) return;

        const msg = chatInput;
        setChatHistory(prev => [...prev, { role: 'user', content: msg }]);
        setChatInput("");

        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: 'agent_message', message: msg });
        } else {
            // Simulation
            setTimeout(() => {
                setChatHistory(prev => [...prev, { role: 'ai', content: "Estou no modo simulação." }]);
            }, 500);
        }
    };

    const startMission = () => {
        if (!missionInput.trim()) return;
        const mission = missionInput;
        setMissionLog(prev => [...prev, `🚀 Despachando Esquadrão: ${mission}`]);
        setMissionInput("");

        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: 'start_mission', mission, path: projectPath });
        }
    };

    const startNightShift = () => {
        setIsNightShiftRunning(true);
        setNightLog(prev => [...prev, "🌙 Iniciando Turno da Noite..."]);

        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: 'start_night_shift', path: projectPath });
        }
    };

    const runCode = () => {
        if (window.ipcRenderer) {
            setOutput(prev => [...prev, "[RUN] Enviando requisição de análise..."]);
            window.ipcRenderer.send('to-python', { command: 'analyze_code', code });
        }
    };

    const selectImage = () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    setSelectedImage(event.target.result); // Base64
                };
                reader.readAsDataURL(file);
            }
        };
        input.click();
    };

    const runAscensionAgent = (agentType) => {
        setAscensionLog(prev => [...prev, `🚀 Iniciando ${agentType}...`]);
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: agentType === 'pm' ? 'start_product_manager' : 'start_founder',
                prompt: ascensionInput
            });
        }
    };

    const deployProject = () => {
        if (window.ipcRenderer) {
            if (confirm("Implantar este projeto na Nuvem PythonJet?")) {
                setDeployStatus("Implantando...");
                window.ipcRenderer.send('to-python', { command: 'deploy_project' });
            }
        } else {
            alert("Implantação na Nuvem (Simulação): Sucesso!");
        }
    };

    const saveFile = () => {
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: 'save_file',
                file: activeFile,
                content: code,
                project_path: projectPath
            });
        }
    };

    const createNewFile = () => {
        const filename = prompt("Digite o nome do novo arquivo (ex: utils/helper.py):");
        if (filename && window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: 'create_file',
                file: filename,
                project_path: projectPath
            });
        }
    };

    const openNativeFolder = async () => {
        if (window.ipcRenderer) {
            const path = await window.ipcRenderer.invoke('dialog:openDirectory');
            if (path) {
                setProjectPath(path);
                // Trigger load logic manually since usage changed
                window.ipcRenderer.send('to-python', { command: 'set_project', path: path });
            }
        }
    };

    const openManual = () => {
        // Tries to open CODEX_MANUAL.md from project root
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: 'read_file',
                file: 'CODEX_MANUAL.md',
                project_path: projectPath
            });
            setActiveFile('CODEX_MANUAL.md');
        }
    };

    const sendTerminalCommand = (e) => {
        if (e.key === 'Enter' && terminalInput.trim()) {
            if (window.ipcRenderer) {
                setOutput(prev => [...prev, `> ${terminalInput}`]);
                window.ipcRenderer.send('to-python', { command: 'shell_exec', cmd: terminalInput });
                setTerminalInput("");
            }
        }
    };

    // Global Key Bindings
    useEffect(() => {
        const handleKeyDown = (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                saveFile();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [code, activeFile]); // Dependencies essential for closure code logic

    const renderView = () => {
        switch (activeView) {
            case 'editor':
                return (
                    <div className="flex-1 flex overflow-hidden">
                        {/* File Explorer (Left Panel) */}
                        <div className="w-60 bg-[#252526] glass-panel border-r border-[#1e1e1e] flex flex-col transition-all duration-300">
                            <div className="p-2 pl-4 text-[11px] font-bold text-[#bbbbbb] uppercase tracking-wide flex items-center justify-between select-none">
                                EXPLORADOR
                            </div>
                            <div className="flex-1 overflow-y-auto overflow-x-hidden pt-1">
                                {!isProjectLoaded ? (
                                    <div className="text-center mt-10 text-[#666] text-xs px-4">
                                        Nenhum Projeto<br />
                                        <button onClick={loadProject} className="mt-2 bg-[#0e639c] text-white px-3 py-1 rounded-sm hover:bg-[#1177bb] text-xs">Abrir Pasta</button>
                                    </div>
                                ) : (
                                    fileTree.map((node, i) => (
                                        <FileTreeNode key={i} node={node} onFileClick={openFile} />
                                    ))
                                )}
                            </div>
                            {/* Terminal Toggle / Extra Info */}
                            <div className="h-6 border-t border-[#3e3e3e] bg-[#222] text-[#ccc] text-xs flex items-center px-2">
                                <Terminal size={12} className="mr-2" /> ESTRUTURA
                            </div>
                        </div>

                        {/* Editor Area */}
                        <div className="flex-1 flex flex-col min-w-0 bg-[#1e1e1e] relative">
                            {!isProjectLoaded ? (
                                <WelcomeDashboard
                                    onOpenProject={openNativeFolder}
                                    onNewFile={createNewFile}
                                    onOpenManual={openManual}
                                />
                            ) : (
                                <>
                                    {/* Editor Tabs */}
                                    <div className="flex items-center bg-[#252526] overflow-x-auto no-scrollbar h-9">
                                        <div className="px-3 h-full bg-[#1e1e1e] text-[13px] text-[#ffffff] border-t border-t-blue-500 border-r border-r-[#252526] flex items-center gap-2 min-w-fit pr-6 relative group cursor-pointer">
                                            <FileCode size={14} className="text-yellow-400" /> {activeFile}
                                            <span className="absolute right-2 text-[#666] opacity-0 group-hover:opacity-100 font-bold">x</span>
                                        </div>
                                        <div className="px-3 h-full bg-[#2d2d2d] text-[13px] text-[#969696] border-r border-r-[#252526] flex items-center gap-2 min-w-fit cursor-pointer hover:bg-[#2a2d2e]">
                                            <span className="italic">welcome.py</span>
                                        </div>
                                    </div>

                                    {/* Breadcrumbs (Fake) */}
                                    <div className="h-6 bg-[#1e1e1e] flex items-center px-4 text-[13px] text-[#888]">
                                        codex-desktop-v2 <ChevronRight size={12} /> src <ChevronRight size={12} /> {activeFile}
                                    </div>

                                    <div className="flex-1 relative overflow-hidden">
                                        <Editor
                                            height="100%"
                                            defaultLanguage="python"
                                            language={activeFile.endsWith('.js') || activeFile.endsWith('.jsx') ? 'javascript' : 'python'}
                                            value={code}
                                            onChange={(value) => setCode(value)}
                                            theme="vs-dark"
                                            options={{
                                                minimap: { enabled: false },
                                                fontSize: vsCodeSettings?.['editor.fontSize'] || 14,
                                                fontFamily: vsCodeSettings?.['editor.fontFamily'] || "'Consolas', 'Courier New', monospace",
                                                padding: { top: 10 },
                                                scrollBeyondLastLine: false,
                                                cursorBlinking: "blink",
                                                smoothScrolling: true, // Re-enabled for 'feel'
                                                renderLineHighlight: 'all',
                                            }}
                                        />
                                    </div>

                                    {/* Integrated Terminal Panel */}
                                    <div className="h-32 bg-[#1e1e1e] border-t border-[#3e3e3e] flex flex-col">
                                        <div className="flex items-center gap-4 px-4 h-7 bg-[#1e1e1e] border-b border-[#252526] text-[11px] text-[#888] font-bold uppercase select-none">
                                            <span className="border-b border-white text-white cursor-pointer py-1">TERMINAL</span>
                                            <span className="hover:text-[#ccc] cursor-pointer">SAÍDA</span>
                                            <span className="hover:text-[#ccc] cursor-pointer">DEBUG</span>
                                            <span className="hover:text-[#ccc] cursor-pointer">PROBLEMAS</span>
                                            <div className="flex-1" />
                                            <div className="flex gap-2 text-[#ccc]">
                                                <ChevronDown size={14} />
                                            </div>
                                        </div>
                                        <div className="flex-1 overflow-y-auto p-2 font-mono text-xs text-[#cccccc] bg-[#1e1e1e]">
                                            <div className="mb-1 text-green-400">➜  codex-IA git:(main) <span className="text-[#ccc]">python {activeFile}</span></div>
                                            {output.slice(-5).map((line, i) => (
                                                <div key={i} className="whitespace-pre-wrap font-mono mb-0.5">{`${line}`}</div>
                                            ))}
                                            <div className="mt-1 flex items-center">
                                                <span className="text-green-400 mr-2">$</span>
                                                <input
                                                    className="bg-transparent border-none outline-none text-[#cccccc] w-full font-mono"
                                                    value={terminalInput}
                                                    onChange={(e) => setTerminalInput(e.target.value)}
                                                    onKeyDown={sendTerminalCommand}
                                                    placeholder="Digite um comando (ex: pip install requests)..."
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </>
                            )}
                        </div>

                        {/* Chat / Sidebar Right (Assitant) */}
                        <div className="w-80 bg-[#252526] border-l border-[#1e1e1e] flex flex-col">
                            <div className="p-2 border-b border-[#1e1e1e] font-bold text-[11px] text-[#bbbbbb] uppercase flex items-center justify-between px-4">
                                <span>ASSISTENTE CODEX</span>
                                <div className="flex gap-2">
                                    <div className="rounded-full bg-green-500 w-2 h-2" title="Online" />
                                </div>
                            </div>
                            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 bg-[#1e1e1e]">
                                {chatHistory.map((msg, i) => (
                                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[90%] rounded-sm p-3 text-sm shadow-md ${msg.role === 'user'
                                            ? 'bg-[#0e639c] text-white'
                                            : 'bg-[#252526] text-[#cccccc] border border-[#333]'
                                            }`}>
                                            {msg.role === 'ai' && <div className="font-bold text-[10px] text-[#888] mb-1 uppercase">Codex AI</div>}
                                            {msg.content.split('\n').map((line, j) => <p key={j} className="min-h-[1rem]">{line}</p>)}
                                        </div>
                                    </div>
                                ))}
                                <div ref={chatEndRef} />
                            </div>
                            <div className="p-3 border-t border-[#1e1e1e] bg-[#252526]">
                                {selectedImage && (
                                    <div className="mb-2 relative w-fit group">
                                        <img src={selectedImage} alt="Upload" className="h-16 rounded border border-[#444]" />
                                        <button onClick={() => setSelectedImage(null)} className="absolute -top-1 -right-1 bg-red-500 rounded-full w-4 h-4 flex items-center justify-center text-white text-[10px]">x</button>
                                    </div>
                                )}
                                <div className="relative">
                                    <textarea
                                        className="w-full bg-[#3c3c3c] border border-[#3c3c3c] rounded-sm py-2 pl-3 pr-10 text-sm text-[#ccc] focus:outline-none focus:border-[#007acc] resize-none h-16 min-h-[40px] placeholder-[#888]"
                                        placeholder="Pergunte ao Codex (Ctrl+Enter para enviar)..."
                                        value={chatInput}
                                        onChange={(e) => setChatInput(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter' && !e.shiftKey) {
                                                e.preventDefault();
                                                sendChat();
                                            }
                                        }}
                                    />
                                    <div className="absolute right-2 bottom-2 flex items-center gap-1">
                                        <button onClick={selectImage} className="text-[#888] hover:text-[#ccc]" title="Add Image">
                                            <Image size={14} />
                                        </button>
                                        <button onClick={sendChat} className="text-[#888] hover:text-white">
                                            <Send size={14} />
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            case 'missions':
                return (
                    <div className="flex-1 flex flex-col p-8 bg-[#1e1e1e] overflow-hidden">
                        <div className="max-w-4xl mx-auto w-full flex flex-col h-full">
                            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 text-[#cccccc]">
                                <Bot size={32} className="text-[#4ec9b0]" /> Delegar Tarefas (IA)
                            </h2>
                            <p className="text-[#888] mb-6">Atribua tarefas complexas para a equipe de agentes.</p>

                            <div className="flex gap-2 mb-6">
                                <input
                                    className="flex-1 bg-[#252526] border border-[#3c3c3c] rounded-sm p-4 text-white focus:outline-none focus:border-[#4ec9b0] font-mono text-sm"
                                    placeholder="Descreva a missão (ex: 'Refatorar utils.py para usar async')"
                                    value={missionInput}
                                    onChange={(e) => setMissionInput(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && startMission()}
                                />
                                <button
                                    onClick={startMission}
                                    className="bg-[#0e639c] hover:bg-[#1177bb] text-white font-bold py-3 px-6 rounded-sm transition"
                                >
                                    DESPACHAR
                                </button>
                            </div>

                            <div className="flex-1 bg-black rounded-sm border border-[#333] p-4 overflow-y-auto font-mono text-sm">
                                {missionLog.length === 0 && <span className="text-[#666]">Log da missão vazio. Aguardando ordens...</span>}
                                {missionLog.map((log, i) => (
                                    <div key={i} className="mb-2 border-b border-[#222] pb-1 text-[#ccc]">{log}</div>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            case 'night':
                return (
                    <div className="flex-1 flex flex-col p-8 bg-[#1e1e1e] overflow-hidden relative">
                        <div className="max-w-4xl mx-auto w-full flex flex-col h-full z-10">
                            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 text-[#c586c0]">
                                <Settings size={32} className="animate-spin-slow" /> Otimizador de Código
                            </h2>
                            <p className="text-[#888] mb-6">Revisão e melhoria autônoma enquanto você descansa.</p>

                            <div className="mb-6">
                                <button
                                    onClick={startNightShift}
                                    disabled={isNightShiftRunning}
                                    className={`w-full py-4 rounded-sm font-bold text-lg transition tracking-widest ${isNightShiftRunning
                                        ? 'bg-[#333] text-[#666] cursor-not-allowed border border-[#444]'
                                        : 'bg-[#6a32a1] hover:bg-[#7a3cb5] text-white shadow-xl'
                                        }`}
                                >
                                    {isNightShiftRunning ? 'OTIMIZAÇÃO ATIVA...' : 'INICIAR OTIMIZAÇÃO'}
                                </button>
                            </div>

                            <div className="flex-1 bg-[#050505] rounded-sm border border-[#333] p-6 overflow-y-auto font-mono text-sm shadow-inner">
                                {nightLog.map((log, i) => (
                                    <div key={i} className="mb-2 text-[#d4d4d4] border-l-2 border-[#6a32a1] pl-3 py-1">
                                        {log}
                                    </div>
                                ))}
                                {isNightShiftRunning && (
                                    <div className="animate-pulse text-[#c586c0] mt-4">Escaneando base de código por imperfeições...</div>
                                )}
                            </div>
                        </div>
                    </div>
                );
            case 'ascension':
                return (
                    <div className="flex-1 flex flex-col p-8 bg-[#1e1e1e] overflow-hidden relative">
                        <div className="max-w-5xl mx-auto w-full flex flex-col h-full z-10">
                            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2 text-[#dcdcaa]">
                                <Sparkles size={32} className="animate-pulse text-yellow-400" /> Central de Evolução
                            </h2>
                            <p className="text-[#888] mb-6">Ative os níveis mais altos da Inteligência Codex.</p>

                            {/* Prompt Input Area */}
                            <div className="mb-6">
                                <textarea
                                    className="w-full bg-[#252526] border border-[#3c3c3c] rounded-sm p-4 text-[#dcdcaa] focus:outline-none focus:border-[#dcdcaa] font-mono text-sm resize-none h-24 placeholder-[#555]"
                                    placeholder="Cole seu Prompt da Singularidade aqui para o Fundador..."
                                    value={ascensionInput}
                                    onChange={(e) => setAscensionInput(e.target.value)}
                                />
                            </div>

                            <div className="grid grid-cols-3 gap-4 mb-6">
                                {/* Level 9: Product Manager */}
                                <div onClick={() => runAscensionAgent('pm')} className="bg-[#252526] p-4 rounded-sm border border-[#333] hover:border-[#007acc] cursor-pointer transition group shadow-lg">
                                    <div className="font-bold text-[#569cd6] mb-1 flex items-center gap-2"><Bot size={18} /> Gerente de Produto</div>
                                    <div className="text-xs text-[#888] group-hover:text-[#ccc]">Analisar métricas & criar backlog.</div>
                                </div>

                                {/* Level 10: Founder */}
                                <div onClick={() => runAscensionAgent('founder')} className="bg-[#252526] p-4 rounded-sm border border-[#333] hover:border-[#c586c0] cursor-pointer transition group shadow-lg">
                                    <div className="font-bold text-[#c586c0] mb-1 flex items-center gap-2"><Sparkles size={18} /> Fundador (Ideias)</div>
                                    <div className="text-xs text-[#888] group-hover:text-[#ccc]">Brainstorm de ventures & planos de negócio.</div>
                                </div>

                                {/* Level 11: Network */}
                                <div onClick={() => window.ipcRenderer?.send('to-python', { command: 'sync_network' })} className="bg-[#252526] p-4 rounded-sm border border-[#333] hover:border-[#4ec9b0] cursor-pointer transition group shadow-lg">
                                    <div className="font-bold text-[#4ec9b0] mb-1 flex items-center gap-2"><Cloud size={18} /> Conectar Nuvem</div>
                                    <div className="text-xs text-[#888] group-hover:text-[#ccc]">Conectar à Sabedoria da Rede.</div>
                                </div>

                                {/* Level 12: Immunity */}
                                <div onClick={() => window.ipcRenderer?.send('to-python', { command: 'activate_immunity' })} className="bg-[#252526] p-4 rounded-sm border border-[#333] hover:border-[#f14c4c] cursor-pointer transition group shadow-lg">
                                    <div className="font-bold text-[#f14c4c] mb-1 flex items-center gap-2"><Settings size={18} /> Proteção de Erros</div>
                                    <div className="text-xs text-[#888] group-hover:text-[#ccc]">Proteção em tempo real.</div>
                                </div>

                                {/* Level 13: Ascension */}
                                <div onClick={() => window.ipcRenderer?.send('to-python', { command: 'trigger_ascension' })} className="bg-[#252526] p-4 rounded-sm border border-[#333] hover:border-[#dcdcaa] cursor-pointer transition group col-span-2 shadow-lg">
                                    <div className="font-bold text-[#dcdcaa] mb-1 flex items-center gap-2"><Sparkles size={18} /> DISPARAR EVOLUÇÃO (SINGULARIDADE)</div>
                                    <div className="text-xs text-[#888] group-hover:text-[#ccc]">Auto-Análise & Reescrita Recursiva de Código.</div>
                                </div>
                            </div>

                            <div className="flex-1 bg-[#1e1e1e] rounded-sm border border-[#333] p-4 overflow-y-auto font-mono text-sm shadow-inner">
                                <div className="text-[10px] text-[#666] mb-2 uppercase tracking-widest border-b border-[#333] pb-1">LOGS DO AGENTE</div>
                                {ascensionLog.length === 0 && <span className="text-[#555] italic">Aguardando ativação do agente...</span>}
                                {ascensionLog.map((log, i) => (
                                    <div key={i} className="mb-2 text-[#dcdcaa] border-l-2 border-[#dcdcaa] pl-3 py-1 whitespace-pre-wrap font-mono">
                                        {log}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                );
            default:
                return <div className="p-10">Visualização não implementada</div>;
        }
    };

    return (
        <div className="flex h-screen bg-[#1e1e1e] text-[#cccccc] font-sans overflow-hidden relative">

            {/* UX Quantum Leap: Command Palette Overlay */}
            {isCommandPaletteOpen && (
                <div className="absolute inset-0 z-[100] bg-black bg-opacity-60 backdrop-blur-sm flex justify-center pt-24 animate-fade-in" onClick={() => setIsCommandPaletteOpen(false)}>
                    <div className="w-[600px] bg-[#252526] border border-[#454545] shadow-2xl rounded-md overflow-hidden animate-slide-down flex flex-col" onClick={e => e.stopPropagation()}>
                        <div className="p-3 border-b border-[#3c3c3c] flex items-center gap-3 bg-[#2d2d2d]">
                            <ChevronRight size={18} className="text-[#007acc]" />
                            <input
                                autoFocus
                                className="bg-transparent outline-none text-white w-full text-base placeholder-[#666] font-mono"
                                placeholder="Type a command..."
                                onKeyDown={(e) => {
                                    if (e.key === 'Enter') {
                                        const cmd = e.target.value.toLowerCase();
                                        if (cmd.includes('night')) setActiveView('night');
                                        else if (cmd.includes('ascension')) setActiveView('ascension');
                                        else if (cmd.includes('open')) openNativeFolder();
                                        else if (cmd.includes('save')) saveFile();
                                        else if (cmd.includes('new')) createNewFile();
                                        else if (cmd.includes('help') || cmd.includes('manual')) openManual();
                                        setIsCommandPaletteOpen(false);
                                    }
                                }}
                            />
                        </div>
                        <div className="max-h-80 overflow-y-auto py-2">
                            {/* Mock Commands for Demo */}
                            <div className="px-3 py-2 hover:bg-[#04395e] cursor-pointer text-sm flex justify-between group items-center" onClick={() => { setActiveView('night'); setIsCommandPaletteOpen(false); }}>
                                <div className="flex flex-col">
                                    <span className="font-bold text-[#cccccc]">Ascension: Toggle Night Shift</span>
                                    <span className="text-xs text-[#666]">Automated Code Refactoring</span>
                                </div>
                                <Settings size={14} className="text-[#666]" />
                            </div>
                            <div className="px-3 py-2 hover:bg-[#04395e] cursor-pointer text-sm flex justify-between group items-center" onClick={() => { saveFile(); setIsCommandPaletteOpen(false); }}>
                                <div className="flex flex-col">
                                    <span className="font-bold text-[#cccccc]">File: Save</span>
                                    <span className="text-xs text-[#666]">Save current file changes</span>
                                </div>
                                <span className="text-xs text-[#888] font-mono bg-[#333] px-1 rounded">Ctrl+S</span>
                            </div>
                            <div className="px-3 py-2 hover:bg-[#04395e] cursor-pointer text-sm flex justify-between group items-center" onClick={() => { openNativeFolder(); setIsCommandPaletteOpen(false); }}>
                                <div className="flex flex-col">
                                    <span className="font-bold text-[#cccccc]">File: Open Folder...</span>
                                    <span className="text-xs text-[#666]">Open a project from disk</span>
                                </div>
                                <span className="text-xs text-[#888] font-mono bg-[#333] px-1 rounded">Ctrl+O</span>
                            </div>
                            <div className="px-3 py-2 hover:bg-[#04395e] cursor-pointer text-sm flex justify-between group items-center" onClick={() => { setActiveView('ascension'); setIsCommandPaletteOpen(false); }}>
                                <div className="flex flex-col">
                                    <span className="font-bold text-[#cccccc]">System: Ascension Chamber</span>
                                    <span className="text-xs text-[#666]">Access Level 13 Controls</span>
                                </div>
                                <Sparkles size={14} className="text-yellow-500" />
                            </div>
                            <div className="px-3 py-2 hover:bg-[#04395e] cursor-pointer text-sm flex justify-between group items-center" onClick={() => { openManual(); setIsCommandPaletteOpen(false); }}>
                                <div className="flex flex-col">
                                    <span className="font-bold text-[#cccccc]">Help: Open User Manual</span>
                                    <span className="text-xs text-[#666]">Read the official documentation</span>
                                </div>
                                <span className="text-xs text-[#888] font-mono bg-[#333] px-1 rounded">F1</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Activity Bar (Leftmost) */}
            <div className="w-12 bg-[#333333] flex flex-col items-center py-2 z-10">
                <div className="mb-4 p-2 cursor-pointer text-white opacity-90 hover:opacity-100">
                    <Code size={28} className="text-blue-500" />
                </div>
                <div className="flex flex-col gap-4 w-full items-center">
                    <div
                        onClick={() => setActiveView('editor')}
                        className={`p-3 cursor-pointer border-l-2 w-full flex justify-center transition hover:text-white ${activeView === 'editor' ? 'border-white text-white' : 'border-transparent text-[#858585]'}`}
                        title="Explorador (Ctrl+Shift+E)"
                    >
                        <FileCode size={24} strokeWidth={1.5} />
                    </div>
                    <div
                        onClick={() => setActiveView('missions')}
                        className={`p-3 cursor-pointer border-l-2 w-full flex justify-center transition hover:text-white ${activeView === 'missions' ? 'border-white text-white' : 'border-transparent text-[#858585]'}`}
                        title="Missões do Esquadrão"
                    >
                        <Bot size={24} strokeWidth={1.5} />
                    </div>
                    <div
                        onClick={() => setActiveView('night')}
                        className={`p-3 cursor-pointer border-l-2 w-full flex justify-center transition hover:text-white ${activeView === 'night' ? 'border-white text-white' : 'border-transparent text-[#858585]'}`}
                        title="Turno da Noite"
                    >
                        <Settings size={24} strokeWidth={1.5} />
                    </div>
                    <div
                        onClick={() => setActiveView('ascension')}
                        className={`p-3 cursor-pointer border-l-2 w-full flex justify-center transition hover:text-white ${activeView === 'ascension' ? 'border-yellow-500 text-yellow-500' : 'border-transparent text-[#858585]'}`}
                        title="Ascensão (Singularidade)"
                    >
                        <Sparkles size={24} strokeWidth={1.5} />
                    </div>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col min-w-0">

                {/* Top Title Bar / Command Palette */}
                <div className="h-9 bg-[#3c3c3c] flex items-center px-4 justify-between select-none relative" onClick={() => setActiveMenu(null)}>
                    <div className="text-xs text-[#cccccc] flex items-center gap-4">
                        <span className="font-bold mr-2">Codex-IA Desktop</span>

                        {/* Custom Menu Bar */}
                        <div className="hidden md:flex gap-1 relative z-50">
                            <div className="relative">
                                <span
                                    className={`hover:bg-[#4a4a4a] px-2 py-1 rounded cursor-pointer ${activeMenu === 'file' ? 'bg-[#4a4a4a] text-white' : ''}`}
                                    onClick={(e) => { e.stopPropagation(); setActiveMenu(activeMenu === 'file' ? null : 'file'); }}
                                >
                                    Arquivo
                                </span>
                                {activeMenu === 'file' && (
                                    <div className="absolute top-7 left-0 w-48 bg-[#252526] border border-[#454545] shadow-xl rounded-sm py-1 flex flex-col z-50">
                                        <div onClick={createNewFile} className="px-3 py-1.5 hover:bg-[#094771] hover:text-white cursor-pointer flex justify-between">
                                            <span>Novo Arquivo</span> <span className="text-[#888]">Ctrl+N</span>
                                        </div>
                                        <div onClick={openNativeFolder} className="px-3 py-1.5 hover:bg-[#094771] hover:text-white cursor-pointer flex justify-between">
                                            <span>Abrir Pasta...</span> <span className="text-[#888]">Ctrl+O</span>
                                        </div>
                                        <div className="h-[1px] bg-[#454545] my-1" />
                                        <div onClick={saveFile} className="px-3 py-1.5 hover:bg-[#094771] hover:text-white cursor-pointer flex justify-between">
                                            <span>Salvar</span> <span className="text-[#888]">Ctrl+S</span>
                                        </div>
                                    </div>
                                )}
                            </div>

                            <span className="hover:bg-[#4a4a4a] px-2 py-1 rounded cursor-pointer">Editar</span>
                            <span className="hover:bg-[#4a4a4a] px-2 py-1 rounded cursor-pointer">Ver</span>
                            <span className="hover:bg-[#4a4a4a] px-2 py-1 rounded cursor-pointer">Ir</span>
                            <span onClick={openManual} className="hover:bg-[#4a4a4a] px-2 py-1 rounded cursor-pointer">Ajuda</span>
                        </div>
                    </div>

                    {/* Project Selector (Now Read-Only Display + Open Button) */}
                    <div className="flex-1 max-w-lg mx-4 flex gap-2">
                        <div
                            className="flex-1 bg-[#252526] border border-[#555] rounded-md flex items-center px-2 py-0.5 text-xs text-[#cccccc] hover:border-[#007acc] transition cursor-pointer"
                            onClick={openNativeFolder}
                            title="Clique para abrir pasta (Estilo VS Code)"
                        >
                            <Folder size={12} className="mr-2 text-[#dcb67a]" />
                            <span className="truncate">{projectPath}</span>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <button
                            onClick={deployProject}
                            className={`px-2 py-0.5 rounded text-[11px] font-bold transition flex items-center gap-1 ${deployStatus ? 'bg-orange-600 text-white animate-pulse' : 'bg-[#0e639c] hover:bg-[#1177bb] text-white'}`}
                        >
                            <Cloud size={12} /> {deployStatus || 'Implantar'}
                        </button>
                    </div>
                </div>

                {renderView()}

                {/* Status Bar (Bottom) */}
                <div className="h-6 bg-[#007acc] text-white flex items-center px-4 text-[11px] justify-between select-none font-sans">
                    <div className="flex items-center gap-4">
                        <div className="flex items-center gap-1 cursor-pointer hover:bg-[#1f8ad2] px-1 h-full"><div className="w-2 h-2 rounded-full bg-white" /> main*</div>
                        <div className="flex items-center gap-1 cursor-pointer hover:bg-[#1f8ad2] px-1 h-full">0 erros</div>
                        <div className="flex items-center gap-1 cursor-pointer hover:bg-[#1f8ad2] px-1 h-full">MODO {activeView.toUpperCase()}</div>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="cursor-pointer hover:bg-[#1f8ad2] px-1 h-full">Ln 12, Col 45</span>
                        <span className="cursor-pointer hover:bg-[#1f8ad2] px-1 h-full">UTF-8</span>
                        <span className="cursor-pointer hover:bg-[#1f8ad2] px-1 h-full">Python</span>
                        <span className="cursor-pointer hover:bg-[#1f8ad2] px-1 h-full"><Bot size={12} className={`inline mr-1 ${ipcConnected ? 'text-white' : 'text-red-300'}`} /> Agente Codex {ipcConnected ? 'Conectado' : 'Offline'}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default App;
