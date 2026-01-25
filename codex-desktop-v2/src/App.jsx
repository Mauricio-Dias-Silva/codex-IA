import React, { useState, useEffect, useRef } from 'react';
import {
    Folder, FileCode, Search, Settings,
    ChevronRight, ChevronDown, Play,
    Terminal, Bot, Cloud, Send,
    Image, Code, Sparkles, AlertTriangle
} from 'lucide-react';

import Editor, { loader } from "@monaco-editor/react";

// FIX: Use local path with dot to signify current directory relative to index.html
// This works in Vite dev (localhost:5173/vs) and Electron Prod (file://.../vs)
loader.config({ paths: { vs: './vs' } });

const FileTreeNode = ({ node, onFileClick, depth = 0 }) => {
    const [isOpen, setIsOpen] = useState(false);
    const sortedChildren = node.children
        ? [...node.children].sort((a, b) => (a.type === b.type ? a.name.localeCompare(b.name) : a.type === 'directory' ? -1 : 1))
        : [];

    if (node.type === 'file') {
        let textColor = "#cccccc";
        let statusLabel = null;
        if (node.status === 'modified') { textColor = "#e2c08d"; statusLabel = "M"; }
        else if (node.status === 'untracked') { textColor = "#73c991"; statusLabel = "U"; }

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
                <Folder size={14} className="text-[#dcb67a] min-w-[14px]" />
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

const WelcomeDashboard = ({ onOpenProject, onNewFile, onOpenManual }) => {
    return (
        <div className="h-full flex flex-col items-center justify-center bg-[#1e1e1e] relative overflow-hidden select-none">
            <div className="z-10 flex flex-col items-center animate-slide-down">
                <div className="mb-8 relative">
                    <div className="w-24 h-24 rounded-full border-2 border-[#007acc] flex items-center justify-center animate-pulse-glow shadow-[0_0_30px_rgba(0,122,204,0.5)]">
                        <Sparkles size={48} className="text-[#007acc] animate-spin-slow" />
                    </div>
                </div>
                <h1 className="text-4xl font-bold text-white mb-2 tracking-tight glow-text font-sans">Codex-IA Desktop <span className="text-[#007acc]">V2</span></h1>
                <p className="text-[#666] text-lg mb-10 font-light">Seu Estúdio de Criação Autônoma</p>
                <div className="grid grid-cols-2 gap-4 w-[500px]">
                    <div onClick={onOpenProject} className="bg-[#252526] border border-[#333] hover:border-[#007acc] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2"><Folder className="text-[#dcb67a]" size={24} /><span className="font-bold text-[#ccc] group-hover:text-white">Abrir Projeto</span></div>
                        <div className="text-xs text-[#666]">Selecionar pasta local</div>
                    </div>
                    <div onClick={onNewFile} className="bg-[#252526] border border-[#333] hover:border-[#4ec9b0] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2"><FileCode className="text-[#4ec9b0]" size={24} /><span className="font-bold text-[#ccc] group-hover:text-white">Novo Arquivo</span></div>
                        <div className="text-xs text-[#666]">Criar script Python/JS</div>
                    </div>
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
    const [terminalInput, setTerminalInput] = useState("");

    const [activeView, setActiveView] = useState('editor');
    const [sidebarTab, setSidebarTab] = useState('files');
    const [activeMenu, setActiveMenu] = useState(null);
    const [isCommandPaletteOpen, setIsCommandPaletteOpen] = useState(false);
    const [vsCodeSettings, setVsCodeSettings] = useState(null);

    const [fileTree, setFileTree] = useState([]);

    const [chatInput, setChatInput] = useState("");
    const [chatHistory, setChatHistory] = useState([{ role: 'ai', content: "Olá! Eu sou o Codex. Abra um projeto para começar." }]);
    const chatEndRef = useRef(null);
    const [taskType, setTaskType] = useState("general");
    const [selectedImage, setSelectedImage] = useState(null);

    const [missionInput, setMissionInput] = useState("");
    const [missionLog, setMissionLog] = useState([]);

    const [nightLog, setNightLog] = useState([]);
    const [isNightShiftRunning, setIsNightShiftRunning] = useState(false);

    const [ascensionLog, setAscensionLog] = useState([]);
    const [ascensionInput, setAscensionInput] = useState("");
    const [deployStatus, setDeployStatus] = useState(null);

    useEffect(() => {
        if (window.ipcRenderer) {
            setIpcConnected(true);
            window.ipcRenderer.invoke('vscode:readSettings').then(setVsCodeSettings);
            window.ipcRenderer.on('python-output', (event, data) => {
                try {
                    const res = JSON.parse(data);
                    handleBackendResponse(res);
                } catch (e) {
                    // Non-JSON output (prints from backend)
                    setOutput(prev => [...prev, data.toString()]);
                }
            });
        }
    }, []);

    const handleBackendResponse = (res) => {
        if (res.type === 'project_loaded') {
            setIsProjectLoaded(true);
            setProjectPath(res.path);
            setOutput(prev => [...prev, `[SISTEMA] Projeto carregado: ${res.path}`]);
            setChatHistory(prev => [...prev, { role: 'ai', content: `Projeto carregado: ${res.path}. Cérebro inicializado.` }]);
            if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'get_file_tree', path: res.path });
        } else if (res.type === 'file_tree') {
            setFileTree(buildTree(res.files));
        } else if (res.type === 'file_content') {
            setCode(res.content);
            setActiveFile(res.file);
        } else if (res.type === 'chat_response') {
            setChatHistory(prev => [...prev, { role: 'ai', content: res.text }]);
        } else if (res.type === 'mission_update') {
            setMissionLog(prev => [...prev, `[${res.status}] ${res.message}`]);
        } else if (res.type === 'night_shift_log') {
            setNightLog(prev => [...prev, res.message]);
        } else if (res.type === 'ascension_log') {
            setAscensionLog(prev => [...prev, res.message]);
        } else if (res.type === 'shell_output') {
            setOutput(prev => [...prev, res.output]);
        } else if (res.type === 'error') {
            setOutput(prev => [...prev, `[ERRO] ${res.message}`]);
            setChatHistory(prev => [...prev, { role: 'ai', content: `⚠️ Erro: ${res.message}` }]);
            // If error relates to file reading, don't show "Loading..." forever or wrong content
            if (res.message.includes('Cannot read binary')) {
                setCode("// Arquivo binário ou não suportado para edição.");
            }
        }
    };

    const buildTree = (files) => {
        const root = { name: 'root', type: 'directory', children: [] };
        files.forEach(f => {
            // f is {path: '...', status: '...'}
            const parts = f.path.split('\\').join('/').split('/');
            let current = root;
            parts.forEach((part, i) => {
                let existing = current.children.find(c => c.name === part);
                if (!existing) {
                    const isFile = i === parts.length - 1;
                    const newNode = {
                        name: part,
                        type: isFile ? 'file' : 'directory',
                        path: f.path,
                        status: isFile ? f.status : null,
                        children: isFile ? null : []
                    };
                    current.children.push(newNode);
                    current = newNode;
                } else { current = existing; }
            });
        });
        return root.children;
    };

    useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [chatHistory]);

    const sendChat = () => {
        if (!chatInput.trim()) return;
        const msg = chatInput;
        setChatHistory(prev => [...prev, { role: 'user', content: msg }]);
        setChatInput("");
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: 'agent_message', message: msg, task_type: taskType, image: selectedImage });
        } else {
            setTimeout(() => setChatHistory(prev => [...prev, { role: 'ai', content: "Estou no modo simulação." }]), 500);
        }
    };

    const openFile = (fp) => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'read_file', file: fp, project_path: projectPath }); };
    const loadProject = () => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'set_project', path: projectPath }); else setIsProjectLoaded(true); };
    const saveFile = () => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'save_file', file: activeFile, content: code, project_path: projectPath }); };
    const createNewFile = () => { const f = prompt("Nome do arquivo:"); if (f && window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'create_file', file: f, project_path: projectPath }); };
    const openManual = () => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'read_file', file: 'CODEX_MANUAL.md', project_path: projectPath }); setActiveFile('CODEX_MANUAL.md'); };
    const deployProject = () => { if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'deploy_project' }); };
    const openNativeFolder = async () => {
        if (window.ipcRenderer) {
            const p = await window.ipcRenderer.invoke('dialog:openDirectory');
            if (p) {
                setProjectPath(p);
                window.ipcRenderer.send('to-python', { command: 'set_project', path: p });
            }
        }
    };
    const startMission = () => { if (missionInput.trim() && window.ipcRenderer) { setMissionLog(prev => [...prev, `🚀 Mission: ${missionInput}`]); window.ipcRenderer.send('to-python', { command: 'start_mission', mission: missionInput, path: projectPath }); setMissionInput(""); } };
    const startNightShift = () => { setIsNightShiftRunning(true); setNightLog(prev => [...prev, "🌙 Starting..."]); if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: 'start_night_shift', path: projectPath }); };
    const runAscensionAgent = (type) => { setAscensionLog(prev => [...prev, `🚀 Starting ${type}...`]); if (window.ipcRenderer) window.ipcRenderer.send('to-python', { command: type === 'pm' ? 'start_product_manager' : 'start_founder', prompt: ascensionInput }); };
    const selectImage = () => { const i = document.createElement('input'); i.type = 'file'; i.accept = 'image/*'; i.onchange = (e) => { const f = e.target.files[0]; if (f) { const r = new FileReader(); r.onload = (ev) => setSelectedImage(ev.target.result); r.readAsDataURL(f); } }; i.click(); };

    const renderView = () => {
        switch (activeView) {
            case 'editor':
                return (
                    <div className="flex-1 flex overflow-hidden">
                        <div className="w-60 bg-[#252526] border-r border-[#1e1e1e] flex flex-col">
                            <div className="p-2 pl-4 text-[11px] font-bold text-[#bbbbbb] uppercase">EXPLORADOR</div>
                            <div className="flex-1 overflow-y-auto">
                                {!isProjectLoaded ? <div className="p-4"><button onClick={loadProject} className="w-full bg-[#0e639c] text-white px-3 py-1 rounded-sm text-xs hover:bg-[#1177bb] transition">Abrir Pasta</button></div> : fileTree.map((n, i) => <FileTreeNode key={i} node={n} onFileClick={openFile} />)}
                            </div>
                        </div>
                        <div className="flex-1 flex flex-col min-w-0 bg-[#1e1e1e]">
                            {!isProjectLoaded ? <WelcomeDashboard onOpenProject={openNativeFolder} onNewFile={createNewFile} onOpenManual={openManual} /> : (
                                <>
                                    <div className="flex bg-[#252526] h-9"><div className="px-3 h-full bg-[#1e1e1e] text-[13px] text-white border-t border-t-blue-500 flex items-center gap-2 pr-6"><FileCode size={14} className="text-yellow-400" /> {activeFile}</div></div>
                                    <div className="flex-1 relative overflow-hidden">
                                        <Editor
                                            height="100%"
                                            defaultLanguage="python"
                                            theme="vs-dark"
                                            value={code}
                                            onChange={setCode}
                                            loading={<div className="text-[#666] flex items-center justify-center h-full">Inicializando Monaco Editor...</div>}
                                            options={{ fontSize: 14, minimap: { enabled: false }, automaticLayout: true }}
                                        />
                                    </div>
                                    <div className="h-32 bg-[#1e1e1e] border-t border-[#3e3e3e] flex flex-col">
                                        <div className="p-2 flex-1 overflow-y-auto font-mono text-xs text-[#cccccc] flex flex-col gap-0.5">
                                            {output.slice(-20).map((l, i) => <div key={i} className="whitespace-pre-wrap">{l}</div>)}
                                        </div>
                                    </div>
                                </>
                            )}
                        </div>
                        <div className="w-80 bg-[#252526] border-l border-[#1e1e1e] flex flex-col">
                            <div className="p-2 border-b border-[#1e1e1e] font-bold text-[11px] text-[#bbbbbb] flex justify-between px-4">
                                <span>ASSISTENTE CODEX</span>
                                <select className="bg-[#2d2d2d] text-[10px] text-[#888] outline-none cursor-pointer" value={taskType} onChange={e => setTaskType(e.target.value)}>
                                    <option value="general">Auto</option>
                                    <option value="coding">Coding (Local)</option>
                                    <option value="reasoning">Thought (Local)</option>
                                </select>
                            </div>
                            <div className="flex-1 overflow-y-auto p-4 flex flex-col gap-4 bg-[#1e1e1e]">
                                {chatHistory.map((m, i) => (
                                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[100%] rounded-sm p-3 text-sm ${m.role === 'user' ? 'bg-[#0e639c] text-white' : 'bg-[#252526] text-[#cccccc] border-l-2 border-l-[#007acc]'}`}>
                                            {m.role === 'ai' && <div className="font-bold text-[10px] mb-1 opacity-50">CODEX SYSTEM</div>}
                                            {m.content}
                                        </div>
                                    </div>
                                ))}
                                <div ref={chatEndRef} />
                            </div>
                            <div className="p-3 bg-[#252526] border-t border-[#1e1e1e]">
                                <textarea className="w-full bg-[#1e1e1e] border border-[#3c3c3c] rounded p-2 text-xs text-[#ccc] h-20 resize-none outline-none focus:border-[#007acc]" placeholder="Fale com o Codex..." value={chatInput} onChange={e => setChatInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendChat())} />
                                <div className="flex justify-between mt-2"><button onClick={selectImage} className="text-[#555] hover:text-[#007acc]"><Image size={16} /></button><button onClick={sendChat} className="text-[#007acc] hover:text-[#1177bb]"><Send size={16} /></button></div>
                            </div>
                        </div>
                    </div>
                );
            case 'missions': return <div className="p-8 h-full bg-[#1e1e1e]"><h2>Missões do Esquadrão</h2><div className="flex gap-2 mt-4"><input className="bg-[#252526] border border-[#333] p-2 flex-1 text-white" value={missionInput} onChange={e => setMissionInput(e.target.value)} /><button onClick={startMission} className="bg-[#0e639c] px-4">Start</button></div><div className="mt-4 bg-black p-4 h-64 overflow-y-auto font-mono text-xs">{missionLog.map((l, i) => <div key={i}>{l}</div>)}</div></div>;
            case 'night': return <div className="p-8 h-full bg-[#1e1e1e]"><h2>Turno da Noite Ops</h2><button onClick={startNightShift} className="bg-[#6a32a1] px-4 py-2 mt-4">Ativar Otimização Autônoma</button><div className="mt-4 bg-black p-4 h-64 overflow-y-auto font-mono text-xs text-purple-300">{nightLog.map((l, i) => <div key={i}>{l}</div>)}</div></div>;
            case 'ascension': return <div className="p-8 h-full bg-[#1e1e1e]"><h2>Câmara de Ascensão</h2><textarea className="bg-[#252526] w-full p-2 h-24 text-yellow-200" placeholder="Prompt da Singularidade..." value={ascensionInput} onChange={e => setAscensionInput(e.target.value)} /><div className="flex gap-4 mt-4"><button onClick={() => runAscensionAgent('pm')} className="bg-[#0e639c] px-4 py-2">PM Analysis</button><button onClick={() => runAscensionAgent('founder')} className="bg-[#6a32a1] px-4 py-2">Founder Brainstorm</button></div><div className="mt-4 bg-black p-4 h-64 overflow-y-auto font-mono text-xs text-yellow-500">{ascensionLog.map((l, i) => <div key={i}>{l}</div>)}</div></div>;
            default: return null;
        }
    };

    return (
        <div className="flex h-screen bg-[#1e1e1e] text-[#cccccc] overflow-hidden">
            <div className="w-12 bg-[#333333] flex flex-col py-2 items-center gap-4 border-r border-black/20">
                <Code size={24} className="text-blue-500 mb-4" />
                <div onClick={() => setActiveView('editor')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'editor' ? 'text-white' : 'text-[#858585]'}`} title="Editor"><FileCode size={24} /></div>
                <div onClick={() => setActiveView('missions')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'missions' ? 'text-white' : 'text-[#858585]'}`} title="Missions"><Bot size={24} /></div>
                <div onClick={() => setActiveView('night')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'night' ? 'text-white' : 'text-[#858585]'}`} title="Night Shift"><Settings size={24} /></div>
                <div onClick={() => setActiveView('ascension')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'ascension' ? 'text-white' : 'text-[#858585]'}`} title="Ascension"><Sparkles size={24} /></div>
            </div>
            <div className="flex-1 flex flex-col">
                <div className="h-9 bg-[#3c3c3c] flex items-center px-4 justify-between select-none titlebar">
                    <span className="text-[11px] font-bold tracking-widest text-[#888]">CODEX-IA DESKTOP V2</span>
                    <div className="flex-1 max-w-lg mx-4 bg-[#252526] px-3 text-[11px] truncate py-1 rounded border border-[#444] text-[#aaa] cursor-pointer hover:border-[#666] no-drag" onClick={openNativeFolder} title="Clique para abrir pasta">{projectPath}</div>
                    <button onClick={deployProject} className="bg-[#0e639c] hover:bg-[#1177bb] transition text-white text-[11px] px-3 py-1 rounded-sm font-bold no-drag">DEPLOY</button>
                </div>
                {renderView()}
                <div className="h-6 bg-[#007acc] text-white flex items-center px-4 text-[10px] justify-between font-bold tracking-tight">
                    <div className="flex gap-4">
                        <span>ESTADO: {ipcConnected ? 'CONECTADO' : 'OFFLINE'}</span>
                        <span>AGENTE: ATIVO</span>
                    </div>
                    <span>{activeView.toUpperCase()} MODE</span>
                </div>
            </div>
        </div>
    );
};

export default App;
