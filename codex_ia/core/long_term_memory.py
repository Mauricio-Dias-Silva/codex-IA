"""
🧠 LONG-TERM MEMORY - Persistent Project Memory
Memória de longo prazo para projetos de semanas/meses
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class LongTermMemory:
    """
    Sistema de memória persistente para o Codex.
    Armazena: conversas, decisões, contexto de projetos, aprendizados.
    """
    
    def __init__(self, db_path: str = ".codex_long_memory.db"):
        self.db_path = Path(db_path)
        self.conn = None
        self._init_db()
        
    def _init_db(self):
        """Cria schema do banco."""
        self.conn = sqlite3.connect(str(self.db_path))
        cursor = self.conn.cursor()
        
        # Tabela de Projetos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            tech_stack TEXT,  -- JSON
            created_at TEXT,
            last_modified TEXT,
            status TEXT  -- active, paused, completed
        )
        """)
        
        # Tabela de Decisões (Design Decisions)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            decision TEXT NOT NULL,
            rationale TEXT,
            alternatives TEXT,  -- JSON
            timestamp TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        """)
        
        # Tabela de Contexto (Key-Value store por projeto)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS context (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            key TEXT NOT NULL,
            value TEXT,
            type TEXT,  -- string, json, file_path
            timestamp TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        """)
        
        # Tabela de Learnings (O que o Codex aprendeu)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS learnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,  -- conversation, error, documentation
            timestamp TEXT
        )
        """)
        
        # Tabela de Conversas (para replay)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            role TEXT,  -- user, assistant
            content TEXT,
            timestamp TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        """)
        
        self.conn.commit()
        print(f"💾 Long-Term Memory inicializada: {self.db_path}")
        
    # --- Project Management ---
    
    def create_project(self, name: str, description: str = "", tech_stack: List[str] = None) -> int:
        """Cria novo projeto."""
        cursor = self.conn.cursor()
        
        tech_stack_json = json.dumps(tech_stack or [])
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO projects (name, description, tech_stack, created_at, last_modified, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name, description, tech_stack_json, now, now, "active"))
        
        self.conn.commit()
        project_id = cursor.lastrowid
        
        print(f"📁 Projeto criado: {name} (ID: {project_id})")
        return project_id
        
    def get_project(self, name: str) -> Optional[Dict]:
        """Recupera projeto por nome."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE name = ?", (name,))
        row = cursor.fetchone()
        
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "tech_stack": json.loads(row[3]),
                "created_at": row[4],
                "last_modified": row[5],
                "status": row[6]
            }
        return None
        
    def list_projects(self, status: str = "active") -> List[Dict]:
        """Lista todos os projetos."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE status = ? ORDER BY last_modified DESC", (status,))
        
        projects = []
        for row in cursor.fetchall():
            projects.append({
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "tech_stack": json.loads(row[3]),
                "created_at": row[4],
                "last_modified": row[5],
                "status": row[6]
            })
        return projects
        
    # --- Decision Tracking ---
    
    def record_decision(self, project_id: int, decision: str, rationale: str, alternatives: List[str] = None):
        """Registra uma decisão de design."""
        cursor = self.conn.cursor()
        
        alternatives_json = json.dumps(alternatives or [])
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO decisions (project_id, decision, rationale, alternatives, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (project_id, decision, rationale, alternatives_json, now))
        
        self.conn.commit()
        print(f"✅ Decisão registrada: {decision[:50]}...")
        
    def get_decisions(self, project_id: int) -> List[Dict]:
        """Recupera todas as decisões de um projeto."""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM decisions WHERE project_id = ? ORDER BY timestamp DESC
        """, (project_id,))
        
        decisions = []
        for row in cursor.fetchall():
            decisions.append({
                "id": row[0],
                "decision": row[2],
                "rationale": row[3],
                "alternatives": json.loads(row[4]),
                "timestamp": row[5]
            })
        return decisions
        
    # --- Context Storage ---
    
    def set_context(self, project_id: int, key: str, value: any, value_type: str = "string"):
        """Armazena contexto do projeto."""
        cursor = self.conn.cursor()
        
        if value_type == "json":
            value = json.dumps(value)
            
        now = datetime.now().isoformat()
        
        # Upsert
        cursor.execute("""
        DELETE FROM context WHERE project_id = ? AND key = ?
        """, (project_id, key))
        
        cursor.execute("""
        INSERT INTO context (project_id, key, value, type, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (project_id, key, str(value), value_type, now))
        
        self.conn.commit()
        
    def get_context(self, project_id: int, key: str) -> Optional[any]:
        """Recupera contexto do projeto."""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT value, type FROM context WHERE project_id = ? AND key = ?
        """, (project_id, key))
        
        row = cursor.fetchone()
        if row:
            value, value_type = row
            if value_type == "json":
                return json.loads(value)
            return value
        return None
        
    # --- Learning Storage ---
    
    def record_learning(self, topic: str, content: str, source: str = "conversation"):
        """Registra aprendizado."""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO learnings (topic, content, source, timestamp)
        VALUES (?, ?, ?, ?)
        """, (topic, content, source, now))
        
        self.conn.commit()
        print(f"📚 Aprendizado registrado: {topic}")
        
    def search_learnings(self, topic: str) -> List[Dict]:
        """Busca aprendizados por tópico."""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT * FROM learnings WHERE topic LIKE ? ORDER BY timestamp DESC
        """, (f"%{topic}%",))
        
        learnings = []
        for row in cursor.fetchall():
            learnings.append({
                "id": row[0],
                "topic": row[1],
                "content": row[2],
                "source": row[3],
                "timestamp": row[4]
            })
        return learnings
        
    # --- Conversation Replay ---
    
    def save_message(self, project_id: int, role: str, content: str):
        """Salva mensagem da conversa."""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        cursor.execute("""
        INSERT INTO conversations (project_id, role, content, timestamp)
        VALUES (?, ?, ?, ?)
        """, (project_id, role, content, now))
        
        self.conn.commit()
        
    def get_conversation_history(self, project_id: int, limit: int = 50) -> List[Dict]:
        """Recupera histórico de conversa."""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT role, content, timestamp FROM conversations
        WHERE project_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """, (project_id, limit))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                "role": row[0],
                "content": row[1],
                "timestamp": row[2]
            })
        return list(reversed(history))  # Ordem cronológica
        
    def close(self):
        """Fecha conexão."""
        if self.conn:
            self.conn.close()


# --- DEMO ---
if __name__ == "__main__":
    memory = LongTermMemory()
    
    # Cria projeto
    project_id = memory.create_project(
        name="compra-coletiva",
        description="E-commerce com agente autônomo",
        tech_stack=["Python", "Django", "Gemini AI"]
    )
    
    # Registra decisão
    memory.record_decision(
        project_id=project_id,
        decision="Usar Gemini Vision para autonomous shopping",
        rationale="Grátis, multimodal, integra com ChromaDB",
        alternatives=["GPT-4V (pago)", "Claude Computer Use (beta)"]
    )
    
    # Armazena contexto
    memory.set_context(project_id, "database_url", "postgres://...", "string")
    memory.set_context(project_id, "features", ["AI posting", "auto-pricing"], "json")
    
    # Registra aprendizado
    memory.record_learning(
        topic="Playwright automation",
        content="Usar async/await com context managers para browser lifecycle",
        source="documentation"
    )
    
    # Busca
    decisions = memory.get_decisions(project_id)
    print(f"\n📋 Decisões do projeto: {len(decisions)}")
    for d in decisions:
        print(f"   • {d['decision']}")
        print(f"     Porque: {d['rationale']}")
    
    memory.close()
