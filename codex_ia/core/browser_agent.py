"""
🤖 BROWSER AGENT - Autonomous Web Navigation
Ponte entre Codex e o Browser (Playwright + Vision)
"""

import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
from typing import Optional, Dict, List
import os

class BrowserAgent:
    """
    Agente autônomo que navega e interage com websites.
    Usa Gemini Vision para "ver" a tela e decidir ações.
    """
    
    def __init__(self, headless: bool = False):
        """
        Args:
            headless: Se True, roda sem abrir janela (modo servidor)
        """
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.headless = headless
        self.screenshots_dir = Path("screenshots")
        self.screenshots_dir.mkdir(exist_ok=True)
        
    async def start(self):
        """Inicializa o browser."""
        print("🚀 Iniciando Browser Agent...")
        self.playwright = await async_playwright().start()
        
        # Chromium é mais leve que Firefox/WebKit
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--start-maximized']
        )
        
        # Context com viewport grande (simula desktop)
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'
        )
        
        self.page = await context.new_page()
        print("✅ Browser pronto!")
        
    async def navigate(self, url: str):
        """Navega para uma URL."""
        print(f"🌐 Navegando para: {url}")
        await self.page.goto(url, wait_until='networkidle')
        print("✅ Página carregada")
        
    async def take_screenshot(self, name: str = "screen") -> Path:
        """Captura screenshot da página atual."""
        filepath = self.screenshots_dir / f"{name}.png"
        await self.page.screenshot(path=str(filepath), full_page=False)
        print(f"📸 Screenshot salvo: {filepath}")
        return filepath
        
    async def analyze_screen_with_vision(self, goal: str) -> Dict:
        """
        Usa Gemini Vision para analisar a tela e identificar elementos.
        
        Args:
            goal: O que procurar (ex: "botão de login", "campo de email")
            
        Returns:
            {
                "found": bool,
                "description": str,
                "selector": str (CSS selector se possível),
                "coordinates": {"x": int, "y": int}
            }
        """
        # Tira screenshot
        screenshot_path = await self.take_screenshot("analysis")
        
        # Carrega a imagem
        with open(screenshot_path, "rb") as f:
            image_bytes = f.read()
            
        # Usa GeminiClient para analisar
        from codex_ia.core.llm_client import GeminiClient
        from google.genai import types
        
        llm = GeminiClient()
        
        # Cria o part da imagem
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png"
        )
        
        # Prompt para Vision
        prompt = f"""
        Você é um agente de automação web.
        Analise esta captura de tela e encontre: {goal}
        
        Responda EXATAMENTE neste formato JSON:
        {{
            "found": true/false,
            "description": "descrição do elemento encontrado",
            "position": "top-left / center / bottom-right / etc",
            "text_visible": "texto visível no elemento"
        }}
        
        Se não encontrar, retorne found: false.
        """
        
        try:
            response = llm.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=[prompt, image_part],
                config=types.GenerateContentConfig(
                    temperature=0.1  # Baixa para precisão
                )
            )
            
            # Parse do JSON
            import json
            result_text = response.text.strip()
            
            # Remove markdown se presente
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
                
            result = json.loads(result_text)
            print(f"🧠 Vision Analysis: {result}")
            return result
            
        except Exception as e:
            print(f"⚠️  Erro na análise: {e}")
            return {"found": False, "description": str(e)}
            
    async def smart_click(self, element_description: str) -> bool:
        """
        Encontra um elemento usando Vision e clica nele.
        
        Args:
            element_description: "botão de login", "link de cadastro", etc
            
        Returns:
            True se clicou com sucesso
        """
        print(f"🎯 Procurando: {element_description}")
        
        # Analisa com Vision
        analysis = await self.analyze_screen_with_vision(element_description)
        
        if not analysis.get("found"):
            print(f"❌ Não encontrei: {element_description}")
            return False
            
        # Tenta clicar no texto visível (mais confiável)
        text = analysis.get("text_visible", "")
        if text:
            try:
                await self.page.click(f"text={text}")
                print(f"✅ Clicou em: {text}")
                await asyncio.sleep(1)  # Aguarda carregamento
                return True
            except:
                print(f"⚠️  Não consegui clicar no texto")
                
        # Fallback: tenta localizar por posição (menos preciso)
        print("⚠️  Modo fallback: clique manual necessário")
        return False
        
    async def type_text(self, text: str, field_description: str = "campo de texto"):
        """
        Encontra um campo e digita texto.
        
        Args:
            text: Texto para digitar
            field_description: Descrição do campo ("campo de email", etc)
        """
        print(f"⌨️  Digitando em: {field_description}")
        
        # Tenta focar no primeiro input visível
        try:
            await self.page.focus("input[type='text'], input[type='email'], input[type='password']")
            await self.page.keyboard.type(text, delay=50)  # 50ms entre teclas (humano)
            print(f"✅ Digitado: {text}")
        except Exception as e:
            print(f"⚠️  Erro ao digitar: {e}")
            
    async def wait_for_element(self, selector: str, timeout: int = 5000):
        """Aguarda elemento aparecer."""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except:
            return False
            
    async def close(self):
        """Fecha o browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("👋 Browser Agent encerrado")
        
    # --- Métodos de Conveniência ---
    
    async def get_current_url(self) -> str:
        """Retorna URL atual."""
        return self.page.url
        
    async def get_page_title(self) -> str:
        """Retorna título da página."""
        return await self.page.title()
        
    async def scroll_down(self, pixels: int = 500):
        """Rola a página para baixo."""
        await self.page.evaluate(f"window.scrollBy(0, {pixels})")
        await asyncio.sleep(0.5)
        
    async def go_back(self):
        """Volta para página anterior."""
        await self.page.go_back()
        await asyncio.sleep(1)


# --- Helper functions ---

async def demo_mercado_livre():
    """
    DEMO: Navega no Mercado Livre e identifica elementos.
    """
    agent = BrowserAgent(headless=False)
    
    try:
        await agent.start()
        
        # Passo 1: Navega
        await agent.navigate("https://www.mercadolivre.com.br")
        await asyncio.sleep(2)
        
        # Passo 2: Tira screenshot inicial
        await agent.take_screenshot("ml_home")
        
        # Passo 3: Usa Vision para encontrar o botão de vender
        print("\n" + "="*60)
        print("🧠 USANDO VISION PARA IDENTIFICAR ELEMENTOS...")
        print("="*60)
        
        result = await agent.analyze_screen_with_vision("botão ou link para vender produtos")
        
        if result.get("found"):
            print(f"\n✅ ENCONTRADO!")
            print(f"   Descrição: {result.get('description')}")
            print(f"   Posição: {result.get('position')}")
            print(f"   Texto: {result.get('text_visible')}")
            
            # Tenta clicar
            await agent.smart_click("vender")
        else:
            print("\n❌ Elemento não encontrado pelo Vision")
            
        # Aguarda para você ver
        print("\n⏸️  Aguardando 10 segundos para você observar...")
        await asyncio.sleep(10)
        
    finally:
        await agent.close()


if __name__ == "__main__":
    print("🤖 BROWSER AGENT - DEMO")
    print("Pressione Ctrl+C para encerrar\n")
    
    asyncio.run(demo_mercado_livre())
