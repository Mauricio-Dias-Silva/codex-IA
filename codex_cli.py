#!/usr/bin/env python3
import os
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from dotenv import load_dotenv

# Initialize Rich Console
console = Console()

def setup_environment():
    """Validates environment variables safely."""
    from dotenv import dotenv_values
    
    # Manually load variables to avoid crashing on malformed lines
    try:
        env_vars = dotenv_values(".env")
        for k, v in env_vars.items():
            if k and v:
                try:
                    os.environ[k] = v
                except OSError:
                    console.print(f"[yellow]Warning: Could not set env var '{k}' due to OS constraints.[/yellow]")
    except Exception as e:
        console.print(f"[yellow]Warning: Error parsing .env file: {e}[/yellow]")

    # Check for critical keys
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GENAI_API_KEY")
    if not api_key:
        console.print("[bold red]❌ Error: GEMINI_API_KEY not found in .env[/bold red]")
        console.print("[yellow]Please create a .env file with your API key.[/yellow]")
        sys.exit(1)

def main():
    console.print(Panel("[bold blue]Codex-IA Desktop[/bold blue]\n[italic]Autonomous Coding Agent - Level 13 (Standalone)[/italic]", border_style="blue"))
    
    setup_environment()
    
    try:
        from codex_ia.core.agent import CodexAgent
    except ImportError as e:
        console.print(f"[bold red]❌ Import Error:[/bold red] {e}")
        console.print("[yellow]Ensure 'codex_ia' folder is in the same directory.[/yellow]")
        sys.exit(1)
        
    # Initialize Agent
    try:
        # CodexAgent(project_dir) - no auto_confirm
        agent = CodexAgent(project_dir=".")
        console.print("[green]✓ Agent Initialized successfully[/green]")
        console.print(f"[dim]Network Memory (Active): {agent.network_agent}[/dim]\n")
        
        # Check for BrainRouter
        use_router = hasattr(agent, 'llm_client') and hasattr(agent.llm_client, 'set_brain')
        if use_router:
            console.print("[bold purple]🧠 The Council (Multi-Brain Router) is ACTIVE.[/bold purple]")
            console.print("Available Brains: Gemini, OpenAI, Groq, DeepSeek, xAI, Ollama")

    except Exception as e:
        console.print(f"[bold red]❌ Initialization Failed:[/bold red] {e}")
        sys.exit(1)

    # Interactive Loop
    while True:
        try:
            # Dynamic prompt showing active brain
            active_brain = "Default"
            if use_router:
                active_brain = agent.llm_client.active_brain.upper()
                
            user_input = Prompt.ask(f"[bold green]Codex ({active_brain})[/bold green]")
            
            if user_input.lower() in ['exit', 'quit']:
                console.print("[blue]Goodbye![/blue]")
                break
                
            if not user_input.strip():
                continue

            # COMMAND: HELP
            if user_input == "/help":
                console.print(Panel("""
                [bold]Commands:[/bold]
                /brain [name]   - Switch Active Brain (gemini, openai, groq, deepseek, xai, ollama)
                /council [topic]- Convene The Council for multi-brain debate
                /squad [task]   - Dispatch the Autonomous Squad
                /switch [path]  - Change project directory
                exit            - Quit
                """, title="Help"))
                continue

            # COMMAND: BRAIN
            if user_input.startswith("/brain "):
                if not use_router:
                    console.print("[red]BrainRouter not available.[/red]")
                    continue
                new_brain = user_input.split(" ", 1)[1].strip().lower()
                if agent.llm_client.set_brain(new_brain):
                    console.print(f"[bold purple]🧠 Brain Switched to: {new_brain.upper()}[/bold purple]")
                else:
                    console.print(f"[red]Failed to switch to {new_brain}. Is the API key set?[/red]")
                continue

            # COMMAND: COUNCIL
            if user_input.startswith("/council "):
                if not use_router:
                    console.print("[red]BrainRouter not available.[/red]")
                    continue
                topic = user_input.split(" ", 1)[1].strip()
                console.print(f"[bold purple]📜 Convening The Council for: '{topic}'[/bold purple]")
                with console.status("[bold purple]The Council is debating...[/bold purple]", spinner="earth"):
                     verdict = agent.llm_client.council_meeting(topic)
                console.print(Panel(verdict, title="Council Verdict", border_style="purple"))
                continue

            # COMMAND: SWITCH
            if user_input.startswith("/switch ") or user_input.startswith("cd "):
                new_path = user_input.split(" ", 1)[1].strip()
                if os.path.exists(new_path):
                    agent.set_context(new_path)
                    console.print(f"[bold green]✓ Switched context to:[/bold green] {new_path}")
                else:
                    console.print(f"[bold red]❌ Path not found:[/bold red] {new_path}")
                continue

            # COMMAND: SQUAD
            if user_input.startswith("/squad ") or user_input.startswith("squad "):
                mission = user_input.split(" ", 1)[1].strip()
                console.print(f"[bold yellow]🚀 Dispatching Squad for mission:[/bold yellow] {mission}")
                
                from codex_ia.core.squad import SquadLeader
                squad = SquadLeader(agent.project_dir)
                
                with console.status("[bold cyan]Squad is planning & coding...[/bold cyan]", spinner="bouncingBar"):
                    # For CLI, apply=True by default for power users
                    report = squad.assign_mission(mission, apply=True)
                
                console.print(Panel(f"[bold]Mission Report[/bold]\n\n[cyan]Plan:[/cyan] {report['plan']}\n\n[green]Code Generated:[/green] {len(report['code'])} chars\n\n[blue]Tests:[/blue] {len(report['tests'])} chars\n\n[bold red]Status:[/bold red] {report['apply_status']}", title="Squad Results"))
                continue

            # COMMAND: DROPSHIP (THE ENDGAME)
            if user_input.startswith("/dropship "):
                niche = user_input.split(" ", 1)[1].strip()
                console.print(f"[bold gold1]🤑 INITIALIZING AUTONOMOUS E-COMMERCE MODE for niche: '{niche}'[/bold gold1]")
                
                from codex_ia.core.ecommerce_agent import EcommerceAgent
                ceo = EcommerceAgent(agent.project_dir)
                
                product_data = None
                
                # Phase 1: Research
                with console.status("[bold cyan]🕵️‍♂️ Hunting Winning Products...[/bold cyan]", spinner="earth"):
                    generator = ceo.find_winning_product(niche)
                    for step in generator:
                         if isinstance(step, dict):
                             product_data = step
                         else:
                             console.print(f"[dim]{step}[/dim]")
                
                if not product_data:
                    console.print("[red]Failed to identify a product. Aborting.[/red]")
                    continue

                console.print(Panel(
                    f"[bold white]{product_data.get('product_name')}[/bold white]\n"
                    f"[green]Price: {product_data.get('price_point')}[/green]\n"
                    f"[italic]'{product_data.get('tagline')}'[/italic]\n\n"
                    f"Audience: {product_data.get('target_audience')}\n"
                    f"Target Pain: {product_data.get('pain_point')}",
                    title="🏆 WINNING PRODUCT SELECTED",
                    border_style="gold1"
                ))
                
                confirm = Prompt.ask("Proceed to Build Store?", choices=["y", "n"], default="y")
                if confirm == "y":
                     with console.status("[bold purple]🏗️ Squad is building the Storefront... (This takes a minute)[/bold purple]", spinner="bouncingBar"):
                          report = ceo.build_storefront(product_data)
                     
                     console.print(Panel(report, title="Store Build Report", border_style="green"))
                     console.print("🚀 Storefront code generated in 'ecommerce/' folder.")

                     # Phase 3: Ads
                     with console.status("[bold blue]📢 Generating Ad Campaigns...[/bold blue]"):
                          ads = ceo.generate_ads(product_data)
                     console.print(Panel(ads, title="Marketing Materials", border_style="blue"))

                continue

            # NORMAL CHAT
            with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
                response = agent.chat(user_input)
            
            console.print(f"\n{response}\n")
            
        except KeyboardInterrupt:
            console.print("\n[blue]Goodbye![/blue]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
