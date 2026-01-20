"""
💹 QUANTITATIVE FINANCE TRAINER
Finanças Quantitativas (Nível PhD - Quant Finance)
Fontes: MIT Sloan, Wharton, CFA Institute, Quant Trading firms
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codex_ia.core.vector_store import CodexVectorStore
from codex_ia.core.llm_client import GeminiClient
from google.genai import types

def train_quant_finance():
    """Indexa conhecimento de finanças quantitativas de alto nível."""
    
    store = CodexVectorStore()
    llm = GeminiClient()
    
    topics = [
        {
            "domain": "DERIVATIVES_PRICING",
            "prompt": """Você é quant da Goldman Sachs/JPMorgan.
            
            Ensine: DERIVATIVES PRICING & BLACK-SCHOLES MODEL
            
            Fundamentos matemáticos:
            - Black-Scholes-Merton Equation (derivação estocástica)
            - Greeks (Delta, Gamma, Vega, Theta, Rho)
            - Implied Volatility e Volatility Smile
            - Binomial Tree Model (Cox-Ross-Rubinstein)
            - Monte Carlo Simulation para pricing
            - Exotic Options (Asian, Barrier, Digital)
            - Interest Rate Derivatives (Swaps, Caps, Floors)
            
            PhD-level matemático. 3000 palavras."""
        },
        {
            "domain": "PORTFOLIO_OPTIMIZATION",
            "prompt": """Você é estrategista quantitativo (Citadel, Two Sigma).
            
            Explique: MODERN PORTFOLIO THEORY & OPTIMIZATION
            
            Framework Markowitz:
            - Mean-Variance Optimization
            - Efficient Frontier
            - Capital Asset Pricing Model (CAPM)
            - Sharpe Ratio, Sortino Ratio, Information Ratio
            - Factor Models (Fama-French 3/5 factors)
            - Risk Parity Strategies
            - Black-Litterman Model
            - Rebalancing e Transaction Costs
            
            Rigor acadêmico. 2800 palavras."""
        },
        {
            "domain": "ALGORITHMIC_TRADING",
            "prompt": """Você é quant trader (Renaissance Technologies, Jane Street).
            
            Ensine: ALGORITHMIC TRADING & MARKET MICROSTRUCTURE
            
            Trading quant:
            - Market Making strategies
            - Statistical Arbitrage (pairs trading, cointegration)
            - Momentum e Mean Reversion
            - High-Frequency Trading (HFT)
            - Order Types e Execution Algorithms (VWAP, TWAP, POV)
            - Slippage e Market Impact Models
            - Backtesting Frameworks (vectorized vs event-driven)
            - Risk Management (VaR, CVaR, Stress Testing)
            
            Técnico avançado. 3200 palavras."""
        },
        {
            "domain": "FIXED_INCOME_ANALYTICS",
            "prompt": """Você é analista de renda fixa (PIMCO, BlackRock).
            
            Explique: FIXED INCOME SECURITIES & TERM STRUCTURE
            
            Conceitos matemáticos:
            - Duration e Convexity
            - Yield Curve (Spot, Forward, Par rates)
            - Term Structure Models (Vasicek, CIR, HJM)
            - Credit Spreads e Default Probability
            - Merton Model (structural credit risk)
            - Securitization (MBS, CDO)
            - Immunization Strategies
            
            PhD-level. 2700 palavras."""
        },
        {
            "domain": "RISK_MANAGEMENT_QUANT",
            "prompt": """Você é Chief Risk Officer quant.
            
            Ensine: QUANTITATIVE RISK MANAGEMENT
            
            Framework matemático:
            - Value at Risk (VaR): Historical, Parametric, Monte Carlo
            - Conditional VaR (Expected Shortfall)
            - Extreme Value Theory (EVT)
            - Copulas para dependência multivariada
            - Stress Testing e Scenario Analysis
            - Basel III Capital Requirements
            - Counterparty Credit Risk (CVA, DVA)
            - Model Risk Management
            
            Rigoroso. 2600 palavras."""
        },
        {
            "domain": "TIME_SERIES_ECONOMETRICS",
            "prompt": """Você é econometrista financeiro (PhD).
            
            Explique: TIME SERIES ANALYSIS FOR FINANCE
            
            Modelos econométricos:
            - ARIMA (AutoRegressive Integrated Moving Average)
            - GARCH (volatility modeling)
            - VAR (Vector Autoregression)
            - Cointegration (Engle-Granger, Johansen)
            - Kalman Filter
            - Machine Learning em séries temporais
            - Regime Switching Models (Markov)
            
            PhD-level matemático. 2500 palavras."""
        }
    ]
    
    print("💹 QUANTITATIVE FINANCE KNOWLEDGE (PhD-Level)...")
    print("=" * 70)
    
    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] 📊 {topic['domain']}")
        
        try:
            response = llm.client.models.generate_content(
                model=llm.model,
                contents=topic['prompt'],
                config=types.GenerateContentConfig(
                    temperature=0.15,  # Muito baixa para precisão matemática
                    max_output_tokens=4000
                )
            )
            
            if response and response.text:
                doc_id = store.index_text(
                    text=response.text,
                    metadata={
                        'source': 'ACADEMIC_QUANT_FINANCE',
                        'domain': topic['domain'],
                        'level': 'PhD',
                        'type': 'QUANTITATIVE_FINANCE',
                        'mathematical': True
                    }
                )
                print(f"   ✅ {doc_id[:16]}... | ~{len(response.text.split())} palavras")
                
        except Exception as e:
            print(f"   ⚠️  {str(e)}")
    
    print("\n" + "=" * 70)
    print("✅ Quant Finance: Arsenal Matemático Completo")
    print("⚠️  DISCLAIMER: Não é conselho de investimento")

if __name__ == "__main__":
    train_quant_finance()
