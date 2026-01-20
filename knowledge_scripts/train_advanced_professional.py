"""
🎓 ADVANCED KNOWLEDGE - MASTER RUNNER (4 Novos Domínios)
Roda: Medicina, Direito, Engenharia, Finanças Quant
"""

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_advanced_knowledge_training():
    """Executa os 4 novos módulos de conhecimento profissional."""
    
    scripts = [
        ("train_medicine.py", "⚕️ Medicina & Saúde"),
        ("train_law.py", "⚖️ Direito & Tributário"),
        ("train_engineering.py", "🏗️ Engenharia"),
        ("train_quant_finance.py", "💹 Finanças Quantitativas")
    ]
    
    print("\n" + "=" * 80)
    print("🎓 CODEX ADVANCED PROFESSIONAL KNOWLEDGE - INICIANDO")
    print("=" * 80)
    print("\n📚 4 Módulos Profissionais de Alto Nível:")
    for i, (_, name) in enumerate(scripts, 1):
        print(f"   {i}. {name}")
    
    print("\n⏱️  Tempo estimado: 10-15 minutos (depende da API)")
    user_input = input("\n✅ Pressione ENTER para começar (ou 'skip' para pular)...")
    
    if user_input.lower() == 'skip':
        print("⏭️  Treinamento pulado")
        return
    
    start_time = time.time()
    
    for i, (script, name) in enumerate(scripts, 1):
        print(f"\n{'='*80}")
        print(f"[{i}/4] {name}")
        print(f"{'='*80}")
        
        try:
            # Importa e roda dinamicamente
            module_name = script.replace('.py', '')
            exec(f"from knowledge_scripts.{module_name} import *")
            
            # Executa a função main
            if "medicine" in script:
                exec("train_medical_knowledge()")
            elif "law" in script:
                exec("train_legal_knowledge()")
            elif "engineering" in script:
                exec("train_engineering_knowledge()")
            elif "quant" in script:
                exec("train_quant_finance()")
                
            print(f"\n✅ {name}: COMPLETO")
            
        except Exception as e:
            print(f"\n⚠️  Erro em {name}: {str(e)}")
            continue
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print("\n" + "=" * 80)
    print("🎓 CONHECIMENTO PROFISSIONAL AVANÇADO COMPLETO!")
    print("=" * 80)
    print(f"⏱️  Tempo total: {minutes}m {seconds}s")
    print("\n📊 Novo conhecimento indexado:")
    print("   • Medicina (EBM, Farmacologia, Saúde Pública)")
    print("   • Direito (Contratos, Societário, Tributário, LGPD)")
    print("   • Engenharia (Civil, Elétrica, Mecânica, Automação)")
    print("   • Finanças Quant (Derivativos, Portfolio, Algo Trading)")
    print("\n💡 Codex agora possui conhecimento multidisciplinar profissional.")

if __name__ == "__main__":
    run_advanced_knowledge_training()
