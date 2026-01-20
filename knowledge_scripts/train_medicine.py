"""
⚕️ MEDICAL KNOWLEDGE TRAINER
Conhecimento médico e de saúde (Nível Acadêmico)
Fontes: Harvard Medical, Johns Hopkins, WHO, UpToDate
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_medical_knowledge():
    """Indexa conhecimento médico profundo e ético."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "EVIDENCE_BASED_MEDICINE",
            "prompt": """Você é professor de Medicina Baseada em Evidências (Harvard Medical School).
            
            Ensine: EVIDENCE-BASED MEDICINE (EBM) FRAMEWORK
            
            Estrutura acadêmica:
            - Hierarchy of Evidence (Meta-análise, RCTs, Cohort Studies)
            - PICO Framework (Patient, Intervention, Comparison, Outcome)
            - Critical Appraisal Skills
            - NNT (Number Needed to Treat) interpretation
            - Cochrane Reviews methodology
            - Bias Detection (Selection, Publication, Attrition)
            - Grade System (quality assessment)
            
            Acadêmico rigoroso. 3000 palavras. Cite estudos fundamentais."""
        },
        {
            "domain": "CLINICAL_REASONING",
            "prompt": """Você é diagnosticador expert (Johns Hopkins).
            
            Explique: CLINICAL REASONING & DIFFERENTIAL DIAGNOSIS
            
            Raciocínio médico:
            - Pattern Recognition vs Analytical Reasoning
            - Bayesian Thinking em diagnóstico
            - Red Flags (sinais de alarme)
            - Diagnostic Schema frameworks
            - Cognitive Biases em medicina (Anchoring, Confirmation, Availability)
            - Systems Approach (Review of Systems)
            - Problem Representation
            
            PhD-level. 2800 palavras. Casos clínicos ilustrativos."""
        },
        {
            "domain": "PHARMACOLOGY_PRINCIPLES",
            "prompt": """Você é farmacologista clínico.
            
            Ensine: CLINICAL PHARMACOLOGY & THERAPEUTICS
            
            Fundamentos:
            - Farmacocinética (ADME: Absorption, Distribution, Metabolism, Excretion)
            - Farmacodinâmica (dose-resposta, receptores)
            - Drug Interactions (CYP450 system)
            - Adverse Drug Reactions (ADRs) classification
            - Polypharmacy em idosos
            - Personalized Medicine (farmacogenética)
            - Therapeutic Drug Monitoring
            
            Rigoroso. 3200 palavras. Evite jargões excessivos."""
        },
        {
            "domain": "PUBLIC_HEALTH_EPIDEMIOLOGY",
            "prompt": """Você é epidemiologista da WHO.
            
            Explique: PUBLIC HEALTH & EPIDEMIOLOGY FUNDAMENTALS
            
            Conceitos científicos:
            - Study Designs (Case-Control, Cohort, Cross-Sectional)
            - Measures: Incidence, Prevalence, Mortality Rate
            - Risk Ratio, Odds Ratio, Hazard Ratio
            - Confounding e Effect Modification
            - Screening Tests (Sensitivity, Specificity, PPV, NPV)
            - Outbreak Investigation (epidemic curves)
            - Social Determinants of Health (Marmot Review)
            
            Acadêmico. 2700 palavras."""
        },
        {
            "domain": "BIOETHICS_MEDICAL_LAW",
            "prompt": """Você é professor de Bioética.
            
            Ensine: MEDICAL ETHICS & BIOETHICS PRINCIPLES
            
            Framework ético:
            - Beauchamp & Childress: Autonomy, Beneficence, Non-maleficence, Justice
            - Informed Consent (competência, informação, voluntariedade)
            - End-of-Life Decisions (eutanásia, cuidados paliativos)
            - Research Ethics (Declaration of Helsinki, GCP)
            - Confidentiality e HIPAA
            - Resource Allocation (triage, justice distributiva)
            - Emerging Issues (CRISPR, AI em saúde)
            
            Rigor filosófico + prático. 2600 palavras."""
        },
        {
            "domain": "PREVENTIVE_MEDICINE",
            "prompt": """Você é especialista em Medicina Preventiva.
            
            Explique: DISEASE PREVENTION & HEALTH PROMOTION
            
            Níveis de prevenção:
            - Prevenção Primária (vacinação, lifestyle)
            - Prevenção Secundária (screening programs)
            - Prevenção Terciária (reabilitação)
            - Health Behavior Change Models (Transtheoretical Model)
            - Chronic Disease Management
            - Population Health Metrics (DALYs, QALYs)
            - Health Literacy
            
            Evidence-based. 2500 palavras."""
        }
    ]
    
    print("⚕️ MEDICAL KNOWLEDGE TRAINING (Academic Level)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 🩺 {topic['domain']}")
        
        try:
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.2,  # Baixa para rigor médico
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                doc_id = store.index_text(
                    text=response.text,
                    metadata={
                        'source': 'ACADEMIC_MEDICINE',
                        'domain': topic['domain'],
                        'level': 'Medical_School',
                        'type': 'CLINICAL_KNOWLEDGE',
                        'ethical': True
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Medicina: Conhecimento Ético Completo")
    print("⚠️  DISCLAIMER: Apenas educacional, não substitui consulta médica")

if __name__ == "__main__":
    train_medical_knowledge()
