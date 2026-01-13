import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],
    base: './', // Essential for Electron relative paths
    build: {
        outDir: 'dist',
    }
});
