import React from 'react';
import { Play, Save, Box, Terminal, Settings, Menu, X, Minus, Square } from 'lucide-react';

const Titlebar = ({ onSave, onDeploy, terminalVisible, onToggleTerminal }) => {
    const handleMenuClick = (menu) => {
        // Simple handlers for now
        if (menu === 'File') alert("Menu File: Save (Ctrl+S), Open (Ctrl+O) - Not yet fully implemented UI");
        if (menu === 'View') onToggleTerminal();
        if (menu === 'Run') onDeploy();
        if (menu === 'Help') alert("Codex Desktop v2.0 - Quantum Leap Edition");
    };

    return (
        <div className="h-8 bg-[#333333] flex items-center justify-between px-2 select-none text-[13px] text-[#cccccc] w-full border-b border-[#1e1e1e] shrink-0">
            {/* Left: Icon & Menus */}
            <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 mr-2">
                    <Box size={16} className="text-[#007acc]" />
                    <span className="font-bold hidden sm:block">Codex</span>
                </div>

                {/* Menus */}
                <div className="hidden md:flex space-x-1">
                    {['File', 'Edit', 'Selection', 'View', 'Go', 'Run', 'Terminal', 'Help'].map(item => (
                        <div
                            key={item}
                            onClick={() => handleMenuClick(item)}
                            className="hover:bg-[#505050] px-2 py-0.5 rounded cursor-pointer transition-colors"
                        >
                            {item}
                        </div>
                    ))}
                </div>
            </div>

            {/* Center: Title */}
            <div className="absolute left-1/2 transform -translate-x-1/2 text-gray-400 text-xs hidden lg:block">
                Codex Desktop - Quantum Leap Edition
            </div>

            {/* Right: Actions & Tools */}
            <div className="flex items-center space-x-2">

                {/* Quick Actions Toolbar */}
                <div className="flex items-center space-x-1 mr-4 border-r border-[#444] pr-4">
                    <button
                        onClick={onSave}
                        className="p-1 hover:bg-[#444] rounded text-gray-300 transition-colors"
                        title="Save (Ctrl+S)"
                    >
                        <Save size={14} />
                    </button>
                    <button
                        onClick={onToggleTerminal}
                        className={`p-1 hover:bg-[#444] rounded transition-colors ${terminalVisible ? 'text-white' : 'text-gray-500'}`}
                        title="Toggle Terminal (Ctrl+J)"
                    >
                        <Terminal size={14} />
                    </button>
                    <button
                        onClick={onDeploy}
                        className="flex items-center space-x-1 bg-[#1e8e3e] hover:bg-[#2eaa56] text-white px-2 py-0.5 rounded transition-colors ml-2"
                        title="Deploy Project"
                    >
                        <Play size={12} fill="white" />
                        <span className="text-xs font-semibold">Deploy</span>
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Titlebar;
