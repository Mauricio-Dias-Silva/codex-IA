import React, { useState, useEffect } from 'react';
import { AlertTriangle, Wrench, X } from 'lucide-react';

const AutoFix = () => {
    const [suggestion, setSuggestion] = useState(null);

    useEffect(() => {
        if (window.ipcRenderer) {
            const handleSuggestion = (event, data) => {
                try {
                    const res = JSON.parse(data);
                    if (res.type === 'analysis_suggestion') {
                        setSuggestion(res);
                    }
                } catch (e) {
                    console.error("AutoFix Parse Error", e);
                }
            };
            window.ipcRenderer.on('python-output', handleSuggestion);
            return () => window.ipcRenderer.removeListener('python-output', handleSuggestion);
        }
    }, []);

    const handleApplyFix = () => {
        if (!suggestion) return;

        // Notify backend to execute the fix plan
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', {
                command: 'start_mission', // Reuse mission logic for fixing
                mission: `CRITICAL FIX: ${suggestion.message}. Error Context: ${suggestion.error}`,
                path: null
            });
        }
        setSuggestion(null);
    };

    if (!suggestion) return null;

    return (
        <div className="fixed bottom-4 right-4 max-w-md bg-[#252526] border border-red-500/50 rounded-lg shadow-2xl overflow-hidden animate-slide-up z-[9999]">
            <div className="bg-red-900/20 p-4 border-b border-red-500/20 flex items-start gap-3">
                <AlertTriangle className="text-red-400 w-6 h-6 flex-shrink-0" />
                <div className="flex-1">
                    <h3 className="text-white font-bold text-sm">System Error Detected</h3>
                    <p className="text-gray-400 text-xs mt-1">{suggestion.message}</p>
                    <div className="mt-2 bg-[#1e1e1e] p-2 rounded text-[10px] font-mono text-red-300 max-h-24 overflow-y-auto">
                        {suggestion.error}
                    </div>
                </div>
                <button
                    onClick={() => setSuggestion(null)}
                    className="text-gray-500 hover:text-white"
                >
                    <X size={16} />
                </button>
            </div>

            <div className="p-3 bg-[#1e1e1e] flex justify-end gap-2">
                <button
                    onClick={() => setSuggestion(null)}
                    className="px-3 py-1.5 text-xs text-gray-400 hover:text-white transition-colors"
                >
                    Ignore
                </button>
                <button
                    onClick={handleApplyFix}
                    className="px-3 py-1.5 text-xs bg-green-600 hover:bg-green-700 text-white rounded flex items-center gap-2 font-bold transition-colors"
                >
                    <Wrench size={12} />
                    Auto-Fix
                </button>
            </div>
        </div>
    );
};

export default AutoFix;
