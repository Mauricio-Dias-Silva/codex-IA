import React, { useState, useEffect } from 'react';
import { Database, Table, Play, Plus, Server, FileDigit, X } from 'lucide-react';

const DatabasePanel = () => {
    const [connectionData, setConnectionData] = useState({
        type: 'sqlite',
        file_path: '',
        host: 'localhost',
        port: '',
        user: '',
        password: '',
        database: ''
    });

    const [isConnected, setIsConnected] = useState(false);
    const [schema, setSchema] = useState({});
    const [query, setQuery] = useState('SELECT * FROM sqlite_master;'); // Default for sqlite
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    // Listen for events from backend (like initial connection success)
    useEffect(() => {
        if (window.ipcRenderer) {
            const handleMessage = (event, data) => {
                try {
                    const res = JSON.parse(data);
                    if (res.type === 'db_connected') {
                        setIsConnected(true);
                        requestSchema();
                    } else if (res.type === 'db_schema') {
                        setSchema(res.schema);
                    } else if (res.type === 'db_result') {
                        setResults(res.data);
                        setError(null);
                    } else if (res.type === 'db_error') {
                        setError(res.message);
                    }
                } catch (e) { console.error(e); }
            };
            window.ipcRenderer.on('python-output', handleMessage);
            return () => window.ipcRenderer.removeListener('python-output', handleMessage);
        }
    }, []);

    const sendCommand = (cmd, payload) => {
        if (window.ipcRenderer) {
            window.ipcRenderer.send('to-python', { command: cmd, ...payload });
        }
    };

    const handleConnect = () => {
        sendCommand('db_connect', { config: connectionData });
    };

    const requestSchema = () => {
        sendCommand('db_get_schema', {});
    };

    const handleRunQuery = () => {
        if (!query.trim()) return;
        setResults(null);
        setError(null);
        sendCommand('db_query', { query });
    };

    const handleTableClick = (tableName) => {
        setQuery(`SELECT * FROM ${tableName} LIMIT 100;`);
    };

    return (
        <div className="flex h-full bg-[#1e1e1e] text-white">
            {/* Sidebar: Connections & Schema */}
            <div className="w-64 bg-[#252526] border-r border-[#3e3e42] flex flex-col">
                <div className="p-3 border-b border-[#3e3e42] flex items-center justify-between">
                    <span className="font-bold flex items-center gap-2 text-xs uppercase tracking-wider text-gray-400">
                        <Database size={14} /> Explorer
                    </span>
                </div>

                <div className="flex-1 overflow-y-auto p-2">
                    {!isConnected ? (
                        <div className="space-y-3">
                            <div>
                                <label className="text-xs text-gray-400 block mb-1">Type</label>
                                <select
                                    className="w-full bg-[#3c3c3c] border border-gray-600 rounded px-2 py-1 text-xs"
                                    value={connectionData.type}
                                    onChange={e => setConnectionData({ ...connectionData, type: e.target.value })}
                                >
                                    <option value="sqlite">SQLite</option>
                                    <option value="postgres">PostgreSQL</option>
                                    <option value="mysql">MySQL</option>
                                </select>
                            </div>

                            {connectionData.type === 'sqlite' ? (
                                <div>
                                    <label className="text-xs text-gray-400 block mb-1">File Path</label>
                                    <input
                                        type="text"
                                        className="w-full bg-[#3c3c3c] border border-gray-600 rounded px-2 py-1 text-xs"
                                        placeholder="/path/to/db.sqlite3"
                                        value={connectionData.file_path}
                                        onChange={e => setConnectionData({ ...connectionData, file_path: e.target.value })}
                                    />
                                </div>
                            ) : (
                                <>
                                    <div className="grid grid-cols-2 gap-2">
                                        <input className="bg-[#3c3c3c] rounded px-2 py-1 text-xs" placeholder="Host" value={connectionData.host} onChange={e => setConnectionData({ ...connectionData, host: e.target.value })} />
                                        <input className="bg-[#3c3c3c] rounded px-2 py-1 text-xs" placeholder="Port" value={connectionData.port} onChange={e => setConnectionData({ ...connectionData, port: e.target.value })} />
                                    </div>
                                    <input className="w-full bg-[#3c3c3c] rounded px-2 py-1 text-xs" placeholder="User" value={connectionData.user} onChange={e => setConnectionData({ ...connectionData, user: e.target.value })} />
                                    <input className="w-full bg-[#3c3c3c] rounded px-2 py-1 text-xs" placeholder="Password" type="password" value={connectionData.password} onChange={e => setConnectionData({ ...connectionData, password: e.target.value })} />
                                    <input className="w-full bg-[#3c3c3c] rounded px-2 py-1 text-xs" placeholder="Database Name" value={connectionData.database} onChange={e => setConnectionData({ ...connectionData, database: e.target.value })} />
                                </>
                            )}

                            <button
                                onClick={handleConnect}
                                className="w-full bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold py-2 rounded"
                            >
                                Connect
                            </button>
                        </div>
                    ) : (
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <span className="text-xs font-bold text-green-400 flex items-center gap-1">
                                    <Server size={12} /> Connected
                                </span>
                                <button onClick={() => setIsConnected(false)} className="text-gray-500 hover:text-white"><X size={12} /></button>
                            </div>

                            {/* Tables List */}
                            <div className="space-y-1">
                                {Object.keys(schema).map(table => (
                                    <div
                                        key={table}
                                        onClick={() => handleTableClick(table)}
                                        className="group cursor-pointer hover:bg-[#37373d] p-1 rounded flex items-center gap-2 text-sm"
                                    >
                                        <Table size={14} className="text-blue-400" />
                                        <span className="truncate">{table}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Main Area: Query Editor & Results */}
            <div className="flex-1 flex flex-col">
                {/* Query Editor */}
                <div className="h-40 bg-[#1e1e1e] border-b border-[#3e3e42] p-2 flex flex-col">
                    <div className="flex items-center justify-between mb-2">
                        <span className="text-xs text-gray-500 font-mono">SQL Query</span>
                        <button
                            onClick={handleRunQuery}
                            className="bg-green-700 hover:bg-green-600 px-3 py-1 rounded text-xs font-bold flex items-center gap-1"
                        >
                            <Play size={12} /> Run
                        </button>
                    </div>
                    <textarea
                        className="flex-1 bg-[#1e1e1e] text-gray-300 font-mono text-sm resize-none focus:outline-none"
                        value={query}
                        onChange={e => setQuery(e.target.value)}
                        placeholder="SELECT * FROM ..."
                    />
                </div>

                {/* Results Table */}
                <div className="flex-1 overflow-auto bg-[#1e1e1e] p-4">
                    {error && (
                        <div className="text-red-400 font-mono text-sm border border-red-900 bg-red-900/20 p-4 rounded">
                            {error}
                        </div>
                    )}

                    {results && results.rows && (
                        <table className="w-full text-left text-sm whitespace-nowrap">
                            <thead className="bg-[#252526] text-gray-400 sticky top-0">
                                <tr>
                                    {results.columns.map(col => (
                                        <th key={col} className="px-4 py-2 border-b border-[#3e3e42] font-mono">{col}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody>
                                {results.rows.map((row, i) => (
                                    <tr key={i} className="hover:bg-[#2a2d2e] border-b border-[#3e3e42]/50">
                                        {results.columns.map(col => (
                                            <td key={col} className="px-4 py-1 text-gray-300">{String(row[col])}</td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}

                    {results && !results.rows && results.message && (
                        <div className="text-green-400 font-mono text-sm m-4">
                            {results.message}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default DatabasePanel;
