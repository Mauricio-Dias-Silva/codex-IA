import React, { useEffect, useRef } from 'react';
import { Terminal } from '@xterm/xterm';
import { FitAddon } from '@xterm/addon-fit';
import '@xterm/xterm/css/xterm.css';

const CodexTerminal = ({ onInput, outputStream }) => {
    const terminalRef = useRef(null);
    const xtermRef = useRef(null);
    const fitAddonRef = useRef(null);

    useEffect(() => {
        if (!terminalRef.current) return;

        // Initialize xterm.js
        const term = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#1e1e1e',
                foreground: '#cccccc',
                cursor: '#ffffff',
                selectionBackground: '#5da5d533',
                black: '#000000',
                red: '#cd3131',
                green: '#0dbc79',
                yellow: '#e5e510',
                blue: '#2472c8',
                magenta: '#bc3fbc',
                cyan: '#11a8cd',
                white: '#e5e5e5',
                brightBlack: '#666666',
                brightRed: '#f14c4c',
                brightGreen: '#23d18b',
                brightYellow: '#f5f543',
                brightBlue: '#3b8eea',
                brightMagenta: '#d670d6',
                brightCyan: '#29b8db',
                brightWhite: '#e5e5e5'
            },
            fontFamily: "'Fira Code', Consolas, 'Courier New', monospace",
            fontSize: 13,
            lineHeight: 1.2
        });

        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);

        term.open(terminalRef.current);
        fitAddon.fit();

        xtermRef.current = term;
        fitAddonRef.current = fitAddon;

        // Welcome Message
        term.writeln('\x1b[1;36mCodex-IA Terminal v2.0\x1b[0m');
        term.writeln('Powered by PythonJet Engine');
        term.write('\r\n$ ');

        // Input Handling
        let command = '';
        term.onData(e => {
            switch (e) {
                case '\r': // Enter
                    term.write('\r\n');
                    if (command.trim()) {
                        onInput(command.trim());
                    }
                    command = '';
                    break;
                case '\u007F': // Backspace
                    if (command.length > 0) {
                        term.write('\b \b');
                        command = command.slice(0, -1);
                    }
                    break;
                default: // Clean input
                    if (e >= String.fromCharCode(0x20) && e <= String.fromCharCode(0x7E) || e >= '\u00a0') {
                        command += e;
                        term.write(e);
                    }
            }
        });

        // Resize observer
        const resizeObserver = new ResizeObserver(() => {
            fitAddon.fit();
        });
        resizeObserver.observe(terminalRef.current);

        return () => {
            term.dispose();
            resizeObserver.disconnect();
        };
    }, []);

    // Handle output stream from backend
    useEffect(() => {
        if (xtermRef.current && outputStream) {
            // If the output is just a string line, write it
            xtermRef.current.writeln(outputStream);
            xtermRef.current.write('$ ');
        }
    }, [outputStream]);

    return (
        <div className="h-full w-full bg-[#1e1e1e] p-2 overflow-hidden">
            <div ref={terminalRef} className="h-full w-full" />
        </div>
    );
};

export default CodexTerminal;
