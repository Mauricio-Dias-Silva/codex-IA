import React, { useState, useEffect, useRef } from 'react';
import { Moon, Sparkles, Activity, Play, StopCircle, Terminal as TerminalIcon } from 'lucide-react';

const NightShift = () => {
    const [isRunning, setIsRunning] = useState(false);
    const [logs, setLogs] = useState([]);
    const bottomRef = useRef(null);

    useEffect(() => {
        if (window.ipcRenderer) {
            const handleLog = (event, data) => {
                try {
                    const res = JSON.parse(data);
                    if (res.type === 'night_shift_log') {
                        setLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), msg: res.message }]);
                    } else if (res.type === 'night_shift_complete') {
                        setIsRunning(false);
                        setLogs(prev => [...prev, { time: new Date().toLocaleTimeString(), msg: "✨ Night Shift Completed." }]);
                    }
                } catch (e) {
                    console.error("Night Shift Parse Error", e);
                }
            };
            window.ipcRenderer.on('python-output', handleLog);
            return () => window.ipcRenderer.removeListener('python-output', handleLog);
        }
    }, []);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [logs]);

    const handleStart = () => {
        if (isRunning) return;
        setIsRunning(true);
        setLogs([{ time: new Date().toLocaleTimeString(), msg: "🌙 Initializing Night Shift Protocol..." }]);

        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: 'start_night_shift',
                path: null // Backend uses current project
            });
        }
    };

    return (
        <div className="flex flex-col h-full bg-[#0d1117] text-[#c9d1d9] p-6 overflow-hidden relative">
            {/* Background Ambience */}
            <div className="absolute top-0 right-0 w-96 h-96 bg-purple-900/10 rounded-full blur-3xl pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-900/10 rounded-full blur-3xl pointer-events-none"></div>

            {/* Header */}
            <div className="flex items-center justify-between mb-8 z-10">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-indigo-500/20 rounded-xl border border-indigo-500/30">
                        <Moon className="w-8 h-8 text-indigo-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold text-white tracking-tight flex items-center gap-2">
                            Night Shift
                            {isRunning && <span className="flex h-3 w-3 relative">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                            </span>}
                        </h1>
                        <p className="text-gray-500">Autonomous Code Evolution Protocol</p>
                    </div>
                </div>

                <button
                    onClick={handleStart}
                    disabled={isRunning}
                    className={`px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-all shadow-lg ${isRunning
                            ? 'bg-gray-800 text-gray-500 cursor-not-allowed border border-gray-700'
                            : 'bg-indigo-600 hover:bg-indigo-500 text-white hover:scale-105 border border-indigo-500'
                        }`}
                >
                    {isRunning ? <Activity className="animate-pulse" size={20} /> : <Play size={20} />}
                    {isRunning ? "Evolving..." : "Start Protocol"}
                </button>
            </div>

            {/* Main Console Area */}
            <div className="flex-1 bg-[#161b22] border border-[#30363d] rounded-xl shadow-2xl flex flex-col overflow-hidden z-10 font-mono text-sm relative">
                {/* Window Controls Decoration */}
                <div className="h-8 bg-[#21262d] border-b border-[#30363d] flex items-center px-4 gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                    <div className="ml-4 text-xs text-gray-500 flex items-center gap-2">
                        <TerminalIcon size={12} /> execution_log.txt
                    </div>
                </div>

                {/* Log Stream */}
                <div className="flex-1 overflow-y-auto p-6 space-y-2">
                    {logs.length === 0 && !isRunning && (
                        <div className="h-full flex flex-col items-center justify-center text-gray-600 opacity-50">
                            <Sparkles size={48} className="mb-4" />
                            <p>Ready to improve codebase quality.</p>
                            <p className="text-xs">Scans for complexity, tech debt, and missing tests.</p>
                        </div>
                    )}

                    {logs.map((log, i) => (
                        <div key={i} className="flex gap-3 hover:bg-[#1f2428] p-1 rounded -mx-1 animate-fade-in">
                            <span className="text-gray-600 select-none">[{log.time}]</span>
                            <span className="text-indigo-300">$</span>
                            <span className={log.msg.includes("Error") ? "text-red-400" : "text-gray-300"}>
                                {log.msg}
                            </span>
                        </div>
                    ))}
                    <div ref={bottomRef} />
                </div>
            </div>

            {/* Stats/Info Footer */}
            <div className="mt-6 grid grid-cols-3 gap-4 z-10">
                <div className="bg-[#161b22] border border-[#30363d] rounded-lg p-4 flex items-center gap-3">
                    <Activity className="text-green-500" />
                    <div>
                        <div className="text-xs text-gray-500 uppercase font-bold">Heuristic Scan</div>
                        <div className="text-white font-bold">Active</div>
                    </div>
                </div>
                <div className="bg-[#161b22] border border-[#30363d] rounded-lg p-4 flex items-center gap-3">
                    <Sparkles className="text-yellow-500" />
                    <div>
                        <div className="text-xs text-gray-500 uppercase font-bold">Refactoring</div>
                        <div className="text-white font-bold">Enabled</div>
                    </div>
                </div>
                <div className="bg-[#161b22] border border-[#30363d] rounded-lg p-4 flex items-center gap-3">
                    <Moon className="text-blue-500" />
                    <div>
                        <div className="text-xs text-gray-500 uppercase font-bold">Mode</div>
                        <div className="text-white font-bold">Autonomous</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default NightShift;
