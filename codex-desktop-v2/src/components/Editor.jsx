import React from 'react';
import Editor from "@monaco-editor/react";
import { FileCode } from 'lucide-react';

const CodexEditor = ({
    activeFile,
    code,
    setCode,
    isProjectLoaded,
    onLoadProject,
    onNewFile,
    onOpenManual,
    onOpenNativeFolder,
    onRefactor,
    settings,
    onEditorMount // [NEW] Expose editor instance
}) => {

    // Sub-component for Empty State
    const WelcomeDashboard = () => (
        <div className="h-full flex flex-col items-center justify-center bg-[#1e1e1e] relative overflow-hidden select-none">
            <div className="z-10 flex flex-col items-center animate-slide-down">
                <div className="mb-8 relative">
                    <div className="w-24 h-24 rounded-full border-2 border-[#007acc] flex items-center justify-center animate-pulse-glow shadow-[0_0_30px_rgba(0,122,204,0.5)]">
                        <FileCode size={48} className="text-[#007acc] animate-spin-slow" />
                    </div>
                </div>
                <h1 className="text-4xl font-bold text-white mb-2 tracking-tight glow-text font-sans">Codex-IA Desktop <span className="text-[#007acc]">V2</span></h1>
                <p className="text-[#666] text-lg mb-10 font-light">Seu Estúdio de Criação Autônoma</p>
                <div className="grid grid-cols-2 gap-4 w-[500px]">
                    <div onClick={onOpenNativeFolder} className="bg-[#252526] border border-[#333] hover:border-[#007acc] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2"><span className="text-[#dcb67a]">📂</span><span className="font-bold text-[#ccc] group-hover:text-white">Abrir Projeto</span></div>
                        <div className="text-xs text-[#666]">Selecionar pasta local</div>
                    </div>
                    <div onClick={onNewFile} className="bg-[#252526] border border-[#333] hover:border-[#4ec9b0] p-4 rounded cursor-pointer group transition-all hover:bg-[#2d2d2d] hover:-translate-y-1">
                        <div className="flex items-center gap-3 mb-2"><span className="text-[#4ec9b0]">+</span><span className="font-bold text-[#ccc] group-hover:text-white">Novo Arquivo</span></div>
                        <div className="text-xs text-[#666]">Criar script Python/JS</div>
                    </div>
                </div>
            </div>
        </div>
    );

    if (!isProjectLoaded) return <WelcomeDashboard />;

    return (
        <div className="flex flex-col h-full bg-[#1e1e1e]">
            <div className="flex bg-[#252526] h-9">
                <div className="px-3 h-full bg-[#1e1e1e] text-[13px] text-white border-t border-t-blue-500 flex items-center gap-2 pr-6 border-r border-[#333]">
                    <FileCode size={14} className="text-yellow-400" /> {activeFile}
                </div>
            </div>
            <div className="flex-1 relative overflow-hidden">
                <Editor
                    height="100%"
                    defaultLanguage="python"
                    theme={settings?.theme || "vs-dark"}
                    value={code}
                    onChange={setCode}
                    onMount={(editor, monaco) => {
                        // Add "Refactor with Codex" Context Menu Action
                        editor.addAction({
                            id: 'refactor-with-codex',
                            label: '✨ Refactor with Codex Agent',
                            contextMenuGroupId: 'navigation',
                            contextMenuOrder: 1,
                            run: (ed) => {
                                const instructions = "Optimize and clean up this code.";
                                if (onRefactor) {
                                    onRefactor(instructions);
                                }
                                alert("Refatoração iniciada com instruções padrão. Use o chat para comandos específicos!");
                            }
                        });

                        // Call parent onMount if exists
                        if (onEditorMount) onEditorMount(editor, monaco);
                    }}
                    loading={<div className="text-[#666] flex items-center justify-center h-full">Inicializando Monaco Editor...</div>}
                    options={{
                        fontSize: settings?.fontSize || 14,
                        fontFamily: settings?.fontFamily || "'Fira Code', Consolas, 'Courier New', monospace",
                        minimap: { enabled: true, renderCharacters: false },
                        smoothScrolling: true,
                        cursorBlinking: "smooth",
                        cursorSmoothCaretAnimation: "on",
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                        fontLigatures: settings?.isLigatures || true,
                        renderLineHighlight: "all",
                        bracketPairColorization: { enabled: true },
                        contextmenu: true // Ensure context menu is enabled
                    }}
                />
            </div>
        </div>
    );
};

export default CodexEditor;
