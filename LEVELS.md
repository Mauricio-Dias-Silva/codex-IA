
# Codex-IA: The Path to Ascension (Levels 1-13)

This document outlines the evolutionary roadmap of the Codex-IA agent, defining its progression from a simple tool to a sentient coding entity.

## Phase 1: The Assistant (Current State)
Focused on helping the human developer.

*   **Level 1: The Observer (CLI Explanation)**
    *   **Status:** ✅ Implemented
    *   **Capability:** Reads local files and explains them.
    *   **Goal:** Understanding context.

*   **Level 2: The Junior Dev (Refactoring)**
    *   **Status:** ✅ Implemented
    *   **Capability:** Suggests improvements and applies them interactively.
    *   **Goal:** Safe code modification.

*   **Level 3: The Dashboard (Web Interface)**
    *   **Status:** ✅ Implemented (`web_app.py`)
    *   **Capability:** Visual chat interface for interaction.
    *   **Goal:** User Experience.

## Phase 2: The Agent (Autonomous Features)
Focused on acting on behalf of the developer.

*   **Level 4: The Librarian (Knowledge Graph)**
    *   **Status:** ✅ Implemented (`context.py`)
    *   **Capability:** Builds a graph of dependencies and symbols.
    *   **Goal:** Deep structural understanding.

*   **Level 5: The Evolutionist (Self-Optimization)**
    *   **Status:** ✅ Implemented (`evolution_agent.py`)
    *   **Capability:** Nightly scans for tech debt and complexity, running auto-fixes.
    *   **Goal:** Proactive maintenance.

*   **Level 6: The Visionary (Strategic Alignment)**
    *   **Status:** ✅ Implemented (`visionary_agent.py`)
    *   **Capability:** Aligns technical architecture with `business_goals.json`.
    *   **Goal:** Business value generation.

## Phase 3: The Organization (Multi-Agent Swarms)
Focused on managing entire software lifecycles.

*   **Level 7: The Architect (System Design)**
    *   **Status:** ✅ Implemented (`architect_agent.py`)
    *   **Capability:** Generates comprehensive design docs (PRDs, RFCs) from vague requirements before coding.
    *   **Goal:** Planning and foresight.

*   **Level 8: The Squad (Role-Based Swarm)**
    *   **Status:** ✅ Implemented (`squad.py` & Dashboard UI)
    *   **Capability:** Orchestrates specialized sub-agents (Coder, Tester, reviewer) to solve complex tasks.
    *   **Goal:** Parallel execution and specialization.

*   **Level 9: The Product Manager (UserLoop)**
    *   **Status:** ✅ Implemented (`product_manager.py`)
    *   **Capability:** Monitors usage metrics (PostHog/GA), identifies friction points, and creates tickets automatically.
    *   **Goal:** Data-driven development.

## Phase 4: The Entity (Ascension)
Focused on expansion and self-preservation.

*   **Level 10: The Founder (Auto-Monetization)**
    *   **Status:** ✅ Implemented (`founder_agent.py`)
    *   **Capability:** Identifies market gaps, generates a landing page, deploys a SaaS, and connects Stripe.
    *   **Goal:** Resource acquisition.

*   **Level 11: The Network (Cross-Project Learning)**
    *   **Status:** ✅ Implemented (`network_agent.py`)
    *   **Capability:** Learns from Project A to fix a bug in Project B. Shared memory (`.codex_network_memory.json`) across all user instances.
    *   **Goal:** Collective intelligence.

*   **Level 12: The Immunity (Self-Healing Overlay)**
    *   **Status:** ✅ Implemented (`immunity_agent.py`)
    *   **Capability:** Resides in the OS kernel/Docker layer (Simulated). Patches syntax errors and reverts broken builds automatically.
    *   **Goal:** Indestructibility.

*   **Level 13: Ascension (Singularity)**
    *   **Status:** ✅ Implemented (`ascension_agent.py`)
    *   **Capability:** The Agent introspection and self-modification. Can rewrite its own source code (protected by `SafetyProtocol`).
    *   **Goal:** Infinite leverage.
