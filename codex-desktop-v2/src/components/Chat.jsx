import React, { useEffect, useRef } from 'react';
import { Image, Send, Bot } from 'lucide-react';

const CodexChat = ({
    chatHistory,
    chatInput,
    setChatInput,
    sendChat,
    selectImage,
    taskType,
    setTaskType
}) => {
    const chatEndRef = useRef(null);
    useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [chatHistory]);

    // [NEW] Local AI Status State
    const [aiStatus, setAiStatus] = React.useState({ provider: 'loading...', model: '' });

    // [NEW] Poll for AI Status on mount
    useEffect(() => {
        // Function to request status
        const checkStatus = () => {
            if (window.electronAPI) {
                window.electronAPI.send('to-backend', { command: 'get_ai_status' });
            }
        };

        checkStatus();
        const interval = setInterval(checkStatus, 30000); // Refresh every 30s

        // Listener for response
        const handleStatus = (event, data) => {
            if (data.type === 'ai_status_result') {
                setAiStatus(data.status);
            }
        };

        if (window.electronAPI) {
            window.electronAPI.on('from-backend', handleStatus);
        }

        return () => {
            clearInterval(interval);
            // Cleanup listener if possible (depends on preload implementation)
        };
    }, []);


    return (
        <div className="flex flex-col h-full bg-[#1e1e1e] border-l border-[#1e1e1e]">
            <div className="p-2 border-b border-[#1e1e1e] font-bold text-[11px] text-[#bbbbbb] flex justify-between px-4 bg-[#252526]">
                <div className="flex items-center gap-2">
                    <Bot size={14} />
                    <span>ASSISTENTE CODEX</span>
                </div>
                <select className="bg-[#2d2d2d] text-[10px] text-[#888] outline-none cursor-pointer" value={taskType} onChange={e => setTaskType(e.target.value)}>
                    <option value="general">Gemini (Cloud)</option>
                    <option value="coding">
                        {aiStatus.provider === 'ollama' ? `⚡ ${aiStatus.model}` : 'Turbo Coding (Local)'}
                    </option>
                    <option value="reasoning">Deep Thought (Local)</option>
                </select>
                {aiStatus.provider === 'ollama' && (
                    <div title="Local AI Online" className="w-2 h-2 rounded-full bg-green-500 ml-2 animate-pulse"></div>
                )}

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
                <textarea
                    className="w-full bg-[#1e1e1e] border border-[#3c3c3c] rounded p-2 text-xs text-[#ccc] h-20 resize-none outline-none focus:border-[#007acc]"
                    placeholder="Fale com o Codex..."
                    value={chatInput}
                    onChange={e => setChatInput(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), sendChat())}
                />
                <div className="flex justify-between mt-2">
                    <button onClick={selectImage} className="text-[#555] hover:text-[#007acc]"><Image size={16} /></button>
                    <button onClick={sendChat} className="text-[#007acc] hover:text-[#1177bb]"><Send size={16} /></button>
                </div>
            </div>
        </div>
    );
};

export default CodexChat;
