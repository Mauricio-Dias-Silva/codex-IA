import React, { useState, useEffect, useRef } from 'react';
import { Rocket, Play, Activity, CheckCircle, XCircle, Clock } from 'lucide-react';

const Missions = ({ taskType, onStartMission }) => {
    const [missionInput, setMissionInput] = useState("");
    const [missions, setMissions] = useState([]); // List of active/past missions
    const [activeMission, setActiveMission] = useState(null);

    useEffect(() => {
        // Listen for mission updates from backend
        if (window.ipcRenderer) {
            const handleUpdate = (event, data) => {
                try {
                    const res = JSON.parse(data);
                    if (res.type === 'mission_update') {
                        updateMissionStatus(res);
                    } else if (res.type === 'mission_result') {
                        completeMission(res.report);
                    }
                } catch (e) {
                    console.error("Mission Parse Error", e);
                }
            };
            window.ipcRenderer.on('python-output', handleUpdate);
            return () => window.ipcRenderer.removeListener('python-output', handleUpdate);
        }
    }, []);

    const updateMissionStatus = (update) => {
        setActiveMission(prev => {
            if (!prev) return prev;
            return {
                ...prev,
                status: update.status, // 'planning', 'coding', 'testing'
                logs: [...prev.logs, { time: new Date().toLocaleTimeString(), msg: update.message }]
            };
        });
    };

    const completeMission = (report) => {
        setActiveMission(prev => {
            const completed = { ...prev, status: 'completed', report: report, completedAt: new Date() };
            setMissions(list => [completed, ...list]);
            return null; // Clear active
        });
    };

    const handleStart = () => {
        if (!missionInput.trim()) return;

        const newMission = {
            id: Date.now(),
            objective: missionInput,
            status: 'started',
            startTime: new Date(),
            logs: [{ time: new Date().toLocaleTimeString(), msg: "Mission dispatched to Squad Leader." }]
        };

        setActiveMission(newMission);
        setMissionInput("");

        // IPC Call
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: 'start_mission',
                mission: newMission.objective,
                path: null // Backend handles path context
            });
        }
    };

    return (
        <div className="flex flex-col h-full bg-[#1e1e1e] text-[#ccc] p-6 overflow-hidden">
            {/* Header */}
            <div className="flex items-center gap-3 mb-8">
                <div className="p-3 bg-purple-600/20 rounded-lg">
                    <Rocket className="w-8 h-8 text-purple-400" />
                </div>
                <div>
                    <h1 className="text-2xl font-bold text-white">Mission Control</h1>
                    <p className="text-sm text-gray-500">Assign complex tasks to the Autonomous Squad.</p>
                </div>
            </div>

            {/* Active Mission Display */}
            {activeMission ? (
                <div className="bg-[#252526] border border-purple-500/30 rounded-xl p-6 mb-6 shadow-2xl relative overflow-hidden">
                    <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-purple-500 via-blue-500 to-purple-500 animate-gradient-x"></div>

                    <div className="flex justify-between items-start mb-4">
                        <div>
                            <h2 className="text-lg font-bold text-white flex items-center gap-2">
                                <Activity className="w-5 h-5 text-green-400 animate-pulse" />
                                Mission in Progress
                            </h2>
                            <p className="text-gray-400 mt-1">{activeMission.objective}</p>
                        </div>
                        <span className="px-3 py-1 bg-purple-900/50 text-purple-200 text-xs rounded-full font-mono border border-purple-500/30">
                            STATUS: {activeMission.status.toUpperCase()}
                        </span>
                    </div>

                    {/* Terminal/Log View */}
                    <div className="bg-[#1e1e1e] rounded-lg p-4 font-mono text-xs h-48 overflow-y-auto mb-4 border border-[#333]">
                        {activeMission.logs.map((log, i) => (
                            <div key={i} className="mb-1">
                                <span className="text-gray-600">[{log.time}]</span>{" "}
                                <span className="text-green-400">{">"}</span>{" "}
                                <span className="text-gray-300">{log.msg}</span>
                            </div>
                        ))}
                        <div ref={useRef(null)} /> {/* Auto scroll target */}
                    </div>
                </div>
            ) : (
                /* Input Area */
                <div className="bg-[#252526] border border-[#333] rounded-xl p-6 mb-8 hover:border-purple-500/50 transition-colors">
                    <label className="block text-sm font-medium text-gray-400 mb-2">New Mission Objective</label>
                    <div className="flex gap-4">
                        <input
                            type="text"
                            className="flex-1 bg-[#1e1e1e] border border-[#3e3e3e] rounded-lg px-4 py-3 text-white focus:outline-none focus:border-purple-500 placeholder-gray-600"
                            placeholder="e.g., Create a login system with Flask and JWT..."
                            value={missionInput}
                            onChange={(e) => setMissionInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleStart()}
                        />
                        <button
                            onClick={handleStart}
                            className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-bold flex items-center gap-2 transition-colors"
                        >
                            <Play size={18} />
                            Launch
                        </button>
                    </div>
                </div>
            )}

            {/* Mission History */}
            <div className="flex-1 overflow-hidden flex flex-col">
                <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Mission Log</h3>
                <div className="flex-1 overflow-y-auto pr-2 space-y-3">
                    {missions.length === 0 && !activeMission && (
                        <div className="text-center text-gray-600 py-10 italic">
                            No missions recorded. The Squad is awaiting orders.
                        </div>
                    )}
                    {missions.map((m) => (
                        <div key={m.id} className="bg-[#252526] border border-[#333] rounded-lg p-4 flex justify-between items-center group hover:bg-[#2d2d2d] transition-colors">
                            <div className="flex items-start gap-3">
                                <div className="mt-1">
                                    <CheckCircle className="w-5 h-5 text-green-500" />
                                </div>
                                <div>
                                    <h4 className="font-medium text-gray-200 group-hover:text-white">{m.objective}</h4>
                                    <p className="text-xs text-gray-500">Completed at {m.completedAt.toLocaleTimeString()}</p>
                                </div>
                            </div>
                            <button className="text-xs bg-[#333] hover:bg-[#444] text-gray-300 px-3 py-1 rounded border border-[#444]">
                                View Report
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default Missions;
