import React, { useState, useEffect, useRef } from 'react';
import {
    Terminal,
    X, Maximize, Minus
} from 'lucide-react';

const MenuBar = ({
    onNewFile, onOpenFile, onSave, onExit,
    onUndo, onRedo, onCut, onCopy, onPaste,
    onToggleSidebar, onToggleTerminal, onZoomIn, onZoomOut,
    onRun, onDebug,
    onNewTerminal, onKillTerminal,
    onAbout
}) => {
    const [activeMenu, setActiveMenu] = useState(null);
    const menuRef = useRef(null);

    // Close menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (menuRef.current && !menuRef.current.contains(event.target)) {
                setActiveMenu(null);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const menus = [
        {
            label: 'File',
            items: [
                { label: 'New File', action: onNewFile, shortcut: 'Ctrl+N' },
                { label: 'Open File...', action: onOpenFile, shortcut: 'Ctrl+O' },
                { label: 'Open Folder...', action: onOpenFile, shortcut: 'Ctrl+K Ctrl+O' },
                { type: 'separator' },
                { label: 'Save', action: onSave, shortcut: 'Ctrl+S' },
                { label: 'Save As...', action: onSave, shortcut: 'Ctrl+Shift+S' },
                { type: 'separator' },
                { label: 'Exit', action: onExit, shortcut: 'Alt+F4' }
            ]
        },
        {
            label: 'Edit',
            items: [
                { label: 'Undo', action: onUndo, shortcut: 'Ctrl+Z' },
                { label: 'Redo', action: onRedo, shortcut: 'Ctrl+Y' },
                { type: 'separator' },
                { label: 'Cut', action: onCut, shortcut: 'Ctrl+X' },
                { label: 'Copy', action: onCopy, shortcut: 'Ctrl+C' },
                { label: 'Paste', action: onPaste, shortcut: 'Ctrl+V' }
            ]
        },
        {
            label: 'Cloud',
            items: [
                { label: 'Deploy to PythonJet 🚀', action: onRun, shortcut: 'Ctrl+D' }
            ]
        },
        {
            label: 'View',
            items: [
                { label: 'Toggle Sidebar', action: onToggleSidebar, shortcut: 'Ctrl+B' },
                { label: 'Toggle Terminal', action: onToggleTerminal, shortcut: 'Ctrl+J' },
                { type: 'separator' },
                { label: 'Zoom In', action: onZoomIn, shortcut: 'Ctrl+=' },
                { label: 'Zoom Out', action: onZoomOut, shortcut: 'Ctrl+-' }
            ]
        },
        {
            label: 'Run',
            items: [
                { label: 'Run Without Debugging', action: onRun, shortcut: 'Ctrl+F5' },
                { label: 'Start Debugging', action: onDebug, shortcut: 'F5' }
            ]
        },
        {
            label: 'Terminal',
            items: [
                { label: 'New Terminal', action: onNewTerminal, shortcut: 'Ctrl+Shift+`' },
                { label: 'Kill Terminal', action: onKillTerminal }
            ]
        },
        {
            label: 'Help',
            items: [
                { label: 'About Codex-IA', action: onAbout }
            ]
        }
    ];

    return (
        <div className="h-8 bg-[#1e1e1e] flex items-center select-none border-b border-[#333] text-[13px] relative z-50 drag-region" ref={menuRef}>
            {/* App Icon */}
            <div className="px-3 flex items-center justify-center">
                <Terminal size={14} className="text-[#007acc]" />
            </div>

            {/* Menus */}
            <div className="flex h-full no-drag-region">
                {menus.map((menu, index) => (
                    <div key={index} className="relative group">
                        <div
                            className={`h-full px-3 flex items-center cursor-pointer hover:bg-[#333] text-[#ccc] hover:text-white ${activeMenu === index ? 'bg-[#333] text-white' : ''}`}
                            onClick={() => setActiveMenu(activeMenu === index ? null : index)}
                            onMouseEnter={() => activeMenu !== null && setActiveMenu(index)}
                        >
                            {menu.label}
                        </div>

                        {/* Dropdown */}
                        {activeMenu === index && (
                            <div className="absolute top-full left-0 bg-[#252526] border border-[#454545] shadow-xl text-white min-w-[200px] py-1 rounded-sm z-[9999]">
                                {menu.items.map((item, i) => (
                                    item.type === 'separator' ? (
                                        <div key={i} className="h-[1px] bg-[#454545] my-1 mx-2" />
                                    ) : (
                                        <div
                                            key={i}
                                            className="px-3 py-1.5 hover:bg-[#094771] flex justify-between items-center cursor-pointer group/item"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                item.action && item.action();
                                                setActiveMenu(null);
                                            }}
                                        >
                                            <span>{item.label}</span>
                                            {item.shortcut && <span className="text-xs text-[#888] group-hover/item:text-white ml-4">{item.shortcut}</span>}
                                        </div>
                                    )
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* Title Centered (Optional/draggable) */}
            <div className="flex-1 text-center text-[#888] text-xs font-sans draggable">
                Codex-IA - {document.title}
            </div>

            {/* Window Controls (Mockup) */}
            <div className="flex text-[#ccc] no-drag-region">
                <div className="px-4 py-2 hover:bg-[#333] hover:text-white cursor-pointer"><Minus size={14} /></div>
                <div className="px-4 py-2 hover:bg-[#333] hover:text-white cursor-pointer"><Maximize size={12} /></div>
                <div className="px-4 py-2 hover:bg-[#e81123] hover:text-white cursor-pointer"><X size={14} /></div>
            </div>
        </div>
    );
};

export default MenuBar;
