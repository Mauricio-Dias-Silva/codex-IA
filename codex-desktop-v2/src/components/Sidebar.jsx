import React, { useState, useEffect, useRef } from 'react';
import {
    Folder, FileCode, ChevronRight, ChevronDown,
    Code, Bot, Settings, Sparkles, Image, Send, Rocket, Database, Moon, X
} from 'lucide-react';

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

const Sidebar = ({
    activeView, setActiveView,
    isProjectLoaded, loadProject, fileTree, openFile,
    chatHistory, chatInput, setChatInput, sendChat, selectImage, taskType, setTaskType,
    selectedImage, setSelectedImage,
    onAbsorbProjects,
    onRunTests
}) => {
    const chatEndRef = useRef(null);
    useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [chatHistory]);

    return (
        <div className="flex h-full">
            {/* Activity Bar */}
            <div className="w-12 bg-[#333333] flex flex-col py-2 items-center gap-4 border-r border-black/20 z-20">
                <Code size={24} className="text-blue-500 mb-4" />
                <div onClick={() => setActiveView('editor')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'editor' ? 'text-white' : 'text-[#858585]'}`} title="Editor"><FileCode size={24} /></div>
                <div onClick={() => setActiveView('missions')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'missions' ? 'text-purple-400' : 'text-[#858585]'}`} title="Mission Control"><Rocket size={24} /></div>
                <div onClick={() => setActiveView('database')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'database' ? 'text-blue-400' : 'text-[#858585]'}`} title="Data Studio"><Database size={24} /></div>
                <div onClick={() => setActiveView('night')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'night' ? 'text-white' : 'text-[#858585]'}`} title="Night Shift"><Moon size={24} /></div>
                <div onClick={() => setActiveView('ascension')} className={`p-2 rounded hover:bg-[#444] cursor-pointer transition ${activeView === 'ascension' ? 'text-white' : 'text-[#858585]'}`} title="Ascension"><Sparkles size={24} /></div>
            </div>

            {/* Side Panel Content */}
            <div className="flex-1 flex flex-col min-w-[250px] max-w-[300px] bg-[#252526] border-r border-[#1e1e1e] overflow-hidden">
                {activeView === 'editor' && (
                    <>
                        <div className="p-2 pl-4 text-[11px] font-bold text-[#bbbbbb] uppercase flex justify-between items-center">
                            EXPLORADOR
                        </div>
                        <div className="flex-1 overflow-y-auto">
                            {!isProjectLoaded ? (
                                <div className="p-4">
                                    <button onClick={loadProject} className="w-full bg-[#0e639c] text-white px-3 py-1 rounded-sm text-xs hover:bg-[#1177bb] transition">Abrir Pasta</button>
                                </div>
                            ) : (
                                fileTree.map((n, i) => <FileTreeNode key={i} node={n} onFileClick={openFile} />)
                            )}
                        </div>

                        {/* Chat Embedded in Sidebar for VSCode feel */}
                        <div className="h-[50%] border-t border-[#1e1e1e] flex flex-col">
                            <div className="p-2 border-b border-[#1e1e1e] font-bold text-[11px] text-[#bbbbbb] flex justify-between px-4 bg-[#252526]">
                                <span>ASSISTENTE CODEX</span>
                                <select className="bg-[#2d2d2d] text-[10px] text-[#888] outline-none cursor-pointer" value={taskType} onChange={e => setTaskType(e.target.value)}>
                                    <option value="general">Cloud (Gemini)</option>
                                    <option value="coding">Local (Turbo)</option>
                                    <option value="reasoning">Local (Deep)</option>
                                </select>
                            </div>
                            <div className="flex-1 overflow-y-auto p-2 flex flex-col gap-3 bg-[#1e1e1e]">
                                {chatHistory.map((m, i) => (
                                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                        <div className={`max-w-[100%] rounded-sm p-2 text-xs ${m.role === 'user' ? 'bg-[#0e639c] text-white' : 'bg-[#252526] text-[#cccccc] border-l-2 border-l-[#007acc]'}`}>
                                            {m.role === 'ai' && <div className="font-bold text-[9px] mb-1 opacity-50">CODEX SYSTEM</div>}
                                            {m.content}
                                        </div>
                                    </div>
                                ))}
                                <div ref={chatEndRef} />
                            </div>
                            <div className="p-2 bg-[#252526] border-t border-[#1e1e1e]">
                                {selectedImage && (
                                    <div className="relative mb-2 inline-block group">
                                        <img src={selectedImage} alt="Preview" className="h-16 w-16 object-cover rounded border border-[#007acc]" />
                                        <button
                                            onClick={() => setSelectedImage(null)}
                                            className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-0.5 opacity-0 group-hover:opacity-100 transition"
                                        >
                                            <X size={12} />
                                        </button>
                                    </div>
                                )}
                                <textarea className="w-full bg-[#1e1e1e] border border-[#3c3c3c] rounded p-2 text-xs text-[#ccc] h-16 resize-none outline-none focus:border-[#007acc]" placeholder={selectedImage ? "Ask Codex Vision about this image..." : "Fale com o Codex..."} value={chatInput} onChange={e => setChatInput(e.target.value)} onKeyDown={e => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendChat())} />
                                <div className="flex justify-between mt-1">
                                    <button onClick={selectImage} className={`hover:text-[#007acc] ${selectedImage ? 'text-[#007acc]' : 'text-[#555]'}`} title="Attach Image for Vision"><Image size={14} /></button>
                                    <button onClick={sendChat} className="text-[#007acc] hover:text-[#1177bb]"><Send size={14} /></button>
                                </div>
                            </div>
                        </div>
                    </>
                )}

                {activeView === 'ascension' && (
                    <div className="flex flex-col h-full bg-[#1e1e1e]">
                        <div className="p-2 pl-4 text-[11px] font-bold text-[#bbbbbb] uppercase flex justify-between items-center bg-[#252526]">
                            ASCENSION PROTOCOLS
                            <Sparkles size={12} className="text-yellow-400" />
                        </div>
                        <div className="p-4 flex flex-col gap-4 overflow-y-auto">
                            <div className="border border-[#7e57c2] bg-[#7e57c2]/10 rounded p-3">
                                <div className="flex items-center gap-2 mb-2">
                                    <Sparkles className="text-[#7e57c2]" size={16} />
                                    <span className="font-bold text-sm text-[#ddd]">Neural Context</span>
                                </div>
                                <p className="text-xs text-[#999] mb-3 leading-relaxed">
                                    Index legacy projects (SysGov, EduFuturo, etc.) into the Vector Database.
                                </p>
                                <button
                                    onClick={onAbsorbProjects}
                                    className="w-full bg-[#7e57c2] hover:bg-[#9575cd] text-white py-1.5 px-3 rounded text-xs font-bold transition flex items-center justify-center gap-2"
                                >
                                    <Database size={12} /> Absorb All Projects
                                </button>
                            </div>

                            <div className="border border-[#e2c08d] bg-[#e2c08d]/10 rounded p-3">
                                <div className="flex items-center gap-2 mb-2">
                                    <Bot className="text-[#e2c08d]" size={16} />
                                    <span className="font-bold text-sm text-[#ddd]">Immune System</span>
                                </div>
                                <p className="text-xs text-[#999] mb-3 leading-relaxed">
                                    Run self-diagnostics and auto-patching for the current project.
                                </p>
                                <button
                                    onClick={onRunTests}
                                    className="w-full bg-[#e2c08d] hover:bg-[#efcf9f] text-[#1e1e1e] py-1.5 px-3 rounded text-xs font-bold transition flex items-center justify-center gap-2"
                                >
                                    <Sparkles size={12} /> Run Auto-Healing
                                </button>
                            </div>

                            <div className="border border-[#333] bg-[#252526] rounded p-3 opacity-75">
                                <div className="flex items-center gap-2 mb-2">
                                    <Bot className="text-[#4ec9b0]" size={16} />
                                    <span className="font-bold text-sm text-[#ddd]">Active Agents</span>
                                </div>
                                <div className="flex flex-col gap-2 text-xs text-[#aaa]">
                                    <div className="flex justify-between"><span>👻 Ghost Writer</span><span className="text-[#4ec9b0]">Active</span></div>
                                    <div className="flex justify-between"><span>🛡️ Immunity</span><span className="text-[#4ec9b0]">Active</span></div>
                                    <div className="flex justify-between"><span>👁️ Vision</span><span className="text-[#4ec9b0]">Active</span></div>
                                    <div className="flex justify-between"><span>🧠 Neural</span><span className="text-yellow-500">Standby</span></div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Sidebar;
