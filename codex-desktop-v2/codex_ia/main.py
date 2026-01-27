
import typer
from rich.console import Console
from rich.markdown import Markdown
from codex_ia.core.context import ContextManager
from codex_ia.core.llm_client import GeminiClient
from codex_ia.core.immunity_agent import ImmunityAgent
from codex_ia.core.ascension_agent import AscensionAgent
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = typer.Typer()
console = Console()

@app.command()
def audit(path: str = "."):
    """
    Auita o código em busca de melhorias de arquitetura.
    """
    console.print(f"[bold blue]Iniciando auditoria em: {path}[/bold blue]")
    
    context_mgr = ContextManager(path)
    context_data = context_mgr.get_context()
    
    client = GeminiClient()
    analysis = client.analyze_architecture(context_data)
    
    console.print(analysis)

@app.command()
def explain(file_path: str):
    """
    Explica o funcionamento de um arquivo específico.
    """
    console.print(f"[bold green]Lendo arquivo: {file_path}[/bold green]")
    
    context_mgr = ContextManager(".") 
    # Use context_manager relative to current dir, but file_path is passed explicitly
    # Ideally ContextManager should handle the file path resolving relative to root
    # But for now passing '.' as root is safe for CLI usage in project root
    
    file_content = context_mgr.get_file_context(file_path)
    
    if "Error" in file_content:
        console.print(f"[bold red]{file_content}[/bold red]")
        return

    client = GeminiClient()
    with console.status("[bold green]Gerando explicação com Gemini...[/bold green]"):
        explanation = client.explain_code(file_content)
        
    console.print(Markdown(explanation))

@app.command()
def refactor(
    file_path: str, 
    instructions: str = typer.Option("", help="Instruções específicas para refatoração"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Aplica as mudanças diretamente no arquivo")
):
    """
    Sugere refatoração para um arquivo específico. Use --interactive para aplicar.
    """
    console.print(f"[bold blue]Analisando para refatoração: {file_path}[/bold blue]")
    
    context_mgr = ContextManager(".")
    file_content = context_mgr.get_file_context(file_path)
    
    if "Error" in file_content:
        console.print(f"[bold red]{file_content}[/bold red]")
        return

    client = GeminiClient()
    with console.status("[bold blue]Gerando sugestões de refatoração...[/bold blue]"):
        suggestion = client.refactor_code(file_content, instructions)
    
    console.print(Markdown(suggestion))
    
    if interactive:
        # Check if suggestion contains a markdown code block provided by the LLM
        import re
        # Regex to find the LAST code block which usually contains the full refactored code
        # This is a heuristic and might need improvement (e.g. asking LLM for a specific format)
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", suggestion, re.DOTALL)
        
        if not code_blocks:
            console.print("[bold yellow]Não foi possível identificar um bloco de código na resposta para aplicar.[/bold yellow]")
            return
            
        new_code = code_blocks[-1] # Assume the last block is the full code
        
        confirm = typer.confirm("Deseja aplicar estas alterações no arquivo?")
        if confirm:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_code)
                console.print(f"[bold green]Alterações aplicadas com sucesso em {file_path}![/bold green]")
            except Exception as e:
                console.print(f"[bold red]Erro ao salvar arquivo: {e}[/bold red]")
        else:
            console.print("[yellow]Operação cancelada.[/yellow]")

@app.command()
def immunity(path: str = "."):
    """
    [NÍVEL 12] Inicia o Agente de Imunidade (Watchdog) para reverter alterações quebradas.
    """
    console.print(f"[bold red]Iniciando Protocolo de Imunidade em: {path}[/bold red]")
    console.print("[dim]Pressione Ctrl+C para parar.[/dim]")
    
    agent = ImmunityAgent(path)
    agent.activate_watchdog()
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()
        console.print("[yellow]Imunidade desativada.[/yellow]")

@app.command()
def ascension():
    """
    [NÍVEL 13] Inicia protocolo de Ascensão (Introspecção).
    """
    # Verify Safety Locks first? The Agent handles it.
    console.print("[bold magenta]Iniciando Agente de Ascensão...[/bold magenta]")
    
    agent = AscensionAgent(".")
    structure = agent.introspect()
    
    console.print(Panel(structure, title="Codebase DNA", border_style="magenta"))
    console.print("[bold green]O Agente está ciente de sua própria estrutura.[/bold green]")

@app.command()
def chat(
    path: str = typer.Option(".", "--path", "-p", help="Caminho do projeto para analisar")
):
    """
    Inicia uma sessão de chat interativo com o Codex-IA sobre o projeto.
    """
    from codex_ia.core.agent import CodexAgent
    from rich.prompt import Prompt
    from rich.panel import Panel

    console.print(Panel(f"[bold white]Iniciando Codex-IA Agent em: {path}[/bold white]", title="Codex-IA", border_style="blue"))
    
    agent = CodexAgent(path)
    console.print("[dim]Sistema inicializado. Carregando lista de arquivos...[/dim]")
    
    # Initial handshake
    console.print("\n[bold green]Codex-IA:[/bold green] Olá! Estou pronto para conversar sobre seu código. O que você gostaria de saber?")
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold blue]Você[/bold blue]")
            
            if user_input.lower() in ['exit', 'quit', 'sair']:
                console.print("[yellow]Encerrando sessão. Até logo![/yellow]")
                break
                
            if not user_input.strip():
                continue
                
            # with console.status("[bold blue]Pensando...[/bold blue]"):
            console.print("[dim]Codex-IA está pensando...[/dim]")
            response = agent.chat(user_input)
                
            console.print(f"\n[bold green]Codex-IA:[/bold green]")
            console.print(Markdown(response))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Sessão interrompida.[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Erro inesperado: {e}[/bold red]")

if __name__ == "__main__":
    app()
