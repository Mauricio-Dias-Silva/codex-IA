#!/bin/bash
# Deploy ChromaDB para VM (Quantum Leap Knowledge)

echo "🌌 Transferindo Quantum Leap ChromaDB para VM..."

# Compactar ChromaDB local
echo "📦 Compactando ChromaDB..."
cd /c/Users/Mauricio/Desktop/codex-IA
tar -czf chroma_quantum.tar.gz .codex_memory/

# SCP para VM
echo "🚀 Enviando para VM..."
scp chroma_quantum.tar.gz mauriciodsilva205@34.148.70.131:/home/mauriciodsilva205/

# SSH para descompactar e reiniciar
echo "📂 Descompactando na VM..."
ssh mauriciodsilva205@34.148.70.131 << 'EOF'
cd ~/codex-IA
tar -xzf ~/chroma_quantum.tar.gz
rm ~/chroma_quantum.tar.gz
sudo systemctl restart codex-ia
echo "✅ ChromaDB atualizado com 2,322 documentos!"
EOF

# Limpar arquivo local
rm chroma_quantum.tar.gz

echo "🌌 Quantum Leap deployado com sucesso!"
echo "🌐 Acesse: http://34.148.70.131:8551/chat/"
