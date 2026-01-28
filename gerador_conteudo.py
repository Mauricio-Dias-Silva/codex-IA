import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv

# Add current directory to path to ensure codex_ia can be imported
sys.path.append(os.getcwd())

from codex_ia.core.ecommerce_agent import EcommerceAgent
from codex_ia.core.brain_router import BrainRouter

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_dropshipping_store():
    console.print(Panel("[bold yellow]🚀 GERADOR DE LOJA DROPSHIPPING (AUTÔNOMO)[/bold yellow]"))
    niche = Prompt.ask("Qual o nicho da loja? (ex: Pet Shop, Tech Wear, Cozinha)", default="Gadgets Inteligentes")
    
    agent = EcommerceAgent()
    product_data = None
    
    with console.status(f"[bold cyan]🕵️‍♂️ Pesquisando produtos vencedores para '{niche}'...[/bold cyan]"):
        for msg in agent.find_winning_product(niche):
            if isinstance(msg, dict):
                product_data = msg
            else:
                console.print(f"[dim]🤖 {msg}[/dim]")
                
    if not product_data:
        console.print("[bold red]❌ Falha ao identificar um produto.[/bold red]")
        return

    console.print(Panel(
        f"[bold white]{product_data.get('product_name')}[/bold white]\n"
        f"[green]Preço Sugerido: {product_data.get('price_point')}[/green]\n"
        f"[italic]'{product_data.get('tagline')}'[/italic]\n\n"
        f"Público: {product_data.get('target_audience')}\n"
        f"Dor que resolve: {product_data.get('pain_point')}",
        title="🏆 PRODUTO SELECIONADO",
        border_style="gold1"
    ))
    
    if Prompt.ask("Construir Landing Page e Anúncios?", choices=["y", "n"], default="y") == "y":
        with console.status("[bold purple]🏗️ Construindo Storefront (HTML/Tailwind)...[/bold purple]"):
            report = agent.build_storefront(product_data)
        console.print(Panel(report, title="Relatório de Construção", border_style="green"))
        
        with console.status("[bold blue]📢 Gerando Campanhas de Anúncios...[/bold blue]"):
            ads = agent.generate_ads(product_data)
        console.print(Panel(ads, title="Materiais de Marketing", border_style="blue"))
        
        console.print(f"\n[bold green]✅ Sucesso! Os arquivos foram gerados na pasta 'ecommerce/'.[/bold green]")
        input("\nPressione Enter para voltar ao menu...")

def generate_article():
    console.print(Panel("[bold green]📚 GERADOR DE CONHECIMENTO (ARTIGOS TÉCNICOS)[/bold green]"))
    topic = Prompt.ask("Sobre qual tópico deseja gerar um artigo profundo?")
    
    router = BrainRouter()
    
    prompt = f"""
    Atue como um Engenheiro de Software Principal.
    Escrava um artigo técnico denso, profissional e profundo sobre: {topic}.
    Inclua: Conceitos avançados, exemplos de código Python, melhores práticas e anti-patterns.
    Formato: Markdown.
    """
    
    with console.status("[bold green]🧠 Processando conhecimento profundo...[/bold green]"):
        content = router.send_message(prompt)
        
    filename = f"knowledge_base_{int(time.time())}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
        
    console.print(f"\n[bold green]✅ Artigo gerado e salvo como '{filename}'![/bold green]")
    input("\nPressione Enter para voltar ao menu...")

def main():
    load_dotenv()
    while True:
        clear_screen()
        console.print(Panel(
            "[bold white]CODEX-IA: GERADOR DE CONTEÚDO 2.0[/bold white]\n"
            "[dim]Sistemas Autônomos - Level 13[/dim]",
            border_style="blue"
        ))
        
        console.print("1. 🚀 Criar Loja Completa (Dropshipping)")
        console.print("2. 📚 Gerar Artigo Técnico / Masterclass")
        console.print("3. ❌ Sair")
        
        choice = Prompt.ask("\nEscolha uma opção", choices=["1", "2", "3"])
        
        if choice == "1":
            generate_dropshipping_store()
        elif choice == "2":
            generate_article()
        else:
            console.print("[blue]Até logo, Agente.[/blue]")
            break

if __name__ == "__main__":
    main()
