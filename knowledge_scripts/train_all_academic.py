"""
🎓 ACADEMIC KNOWLEDGE - MASTER TRAINER
Roda todos os 4 módulos acadêmicos em sequência
"""

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_academic_training():
    """Executa todos os treinamentos acadêmicos."""
    
    scripts = [
        ("train_entrepreneurship.py", "🚀 Empreendedorismo"),
        ("train_strategic_mgmt.py", "🏛️ Gestão Estratégica"),
        ("train_urban_governance.py", "🏙️ Governança Urbana"),
        ("train_sustainability.py", "🌍 Sustentabilidade")
    ]
    
    print("\n" + "=" * 80)
    print("🎓 CODEX ACADEMIC KNOWLEDGE LIBRARY - INICIANDO")
    print("=" * 80)
    print("\n📚 4 Módulos de Nível Doutorado:")
    for i, (_, name) in enumerate(scripts, 1):
        print(f"   {i}. {name}")
    
    print("\n⏱️  Tempo estimado: 8-12 minutos (depende da API)")
    input("\n✅ Pressione ENTER para começar...")
    
    start_time = time.time()
    
    for i, (script, name) in enumerate(scripts, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/4] {name}")
        print(f"{'='*80}")
        
        script_path = os.path.join("knowledge_scripts", script)
        
        try:
            # Importa e roda dinamicamente
            module_name = script.replace('.py', '')
            exec(f"from knowledge_scripts.{module_name} import *")
            
            # Executa a função main
            if "entrepreneurship" in script:
                exec("train_entrepreneurship()")
            elif "strategic" in script:
                exec("train_strategic_management()")
            elif "urban" in script:
                exec("train_urban_governance()")
            elif "sustainability" in script:
                exec("train_sustainability()")
                
            print(f"\n✅ {name}: COMPLETO")
            
        except Exception as e:
            print(f"\n⚠️  Erro em {name}: {str(e)}")
            continue
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "=" * 80)
    print("🎓 BIBLIOTECA ACADÊMICA COMPLETA!")
    print("=" * 80)
    print(f"⏱️  Tempo total: {minutes}m {seconds}s")
    print("\n📊 Conhecimento indexado:")
    print("   • Empreendedorismo (Lean, Effectuation, VC)")
    print("   • Estratégia (Porter, Mintzberg, Barney)")
    print("   • Governança Urbana (Smart Cities, SDGs)")
    print("   • Sustentabilidade (ESG, Circular Economy)")
    print("\n💡 Codex agora possui conhecimento de nível PhD em gestão.")

if __name__ == "__main__":
    run_all_academic_training()
