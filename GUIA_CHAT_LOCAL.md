# 🚀 Guia Codex-IA: Chat 100% Local e Grátis

Para parar de depender da API do Gemini e não ter mais sustos com a conta, siga estes 3 passos simples para configurar o seu "Cérebro Local".

## 1. Instalar o Ollama
O Ollama é a ferramenta que permite rodar IAs poderosas direto no seu Windows.
- **Download:** [Acesse ollama.com](https://ollama.com) e baixe a versão para Windows.
- Instale como qualquer programa normal.

## 2. Baixar o Modelo (Otimizado para o seu PC)
Como sua placa de vídeo é a **Intel HD 620**, selecionamos um modelo super leve e inteligente que vai rodar bem sem travar seu computador.

Abra o seu Terminal (PowerShell ou CMD) e digite:
```powershell
ollama pull llama3.2:3b
```
> [!TIP]
> Este modelo tem "apenas" 2GB, então o download é rápido e ele não consome muita memória RAM.

### Opção B: Via GUI (Novo!)
No seu Codex-IA, vá na aba **"IoT Lab"**:
1. Você verá uma seção chamada **"Local Model Manager (Ollama)"**.
2. Clique no botão do modelo desejado (recomendo o **Llama 3.2 3B**).
3. O Codex-IA fará o download para você em segundo plano.

## 3. Usar no Codex-IA
No Chat do seu **Codex-IA**, agora você verá um seletor no topo e **ícones de status**:
1. **Ícones de Status:** Verifique se o ícone de computador (Ollama) está **verde**.
2. Clique no seletor (que deve estar em "Brain Router (Auto)").
3. Selecione **"Ollama (Local - 0 Custo)"**.
4. **Pronto!** Suas mensagens agora serão processadas 100% no seu PC.

---

### Por que usar o Local?
- **Totalmente Grátis:** Pode conversar 24h por dia sem gastar 1 centavo.
- **Privacidade Máxima:** Seus segredos de código não saem da sua máquina.
- **Offline:** Funciona mesmo se você estiver sem internet.

> [!IMPORTANT]
> Lembre-se de deixar o ícone do Ollama aberto na barra de tarefas (perto do relógio) para o Codex-IA conseguir se conectar a ele.
