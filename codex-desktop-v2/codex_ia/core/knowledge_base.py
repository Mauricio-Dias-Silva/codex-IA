import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class KnowledgeBase:
    """
    Simples base de conhecimento persistente para o Codex-IA.
    Armazena metadados do projeto, resumo de arquivos e relacionamentos.
    """
    
    def __init__(self, storage_path: str = ".codex_memory.json"):
        self.storage_path = Path(storage_path)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        """Carrega a base de dados do disco."""
        if not self.storage_path.exists():
            return {
                "project_summary": "",
                "file_index": {},  # path -> {hash, summary, last_updated}
                "dependencies": {}, # module -> [imported_by]
                "tech_stack": [],
                "last_scan": None
            }
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self):
        """Salva a base de dados no disco."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar KnowledgeBase: {e}")

    def update_file_summary(self, file_path: str, summary: str, file_hash: str):
        """Atualiza o resumo e hash de um arquivo."""
        self.data["file_index"][file_path] = {
            "summary": summary,
            "hash": file_hash,
            "last_updated": datetime.now().isoformat()
        }

    def get_file_summary(self, file_path: str) -> Optional[str]:
        """Retorna o resumo armazenado de um arquivo."""
        meta = self.data["file_index"].get(file_path)
        return meta.get("summary") if meta else None

    def set_project_summary(self, summary: str):
        self.data["project_summary"] = summary
        
    def get_project_summary(self) -> str:
        return self.data.get("project_summary", "")

    def update_scan_time(self):
        self.data["last_scan"] = datetime.now().isoformat()
