import json
import os
import logging
from typing import Dict, Any, Optional
import datetime

logger = logging.getLogger(__name__)

class NetworkAgent:
    """
    Level 11: The Network
    Manages shared knowledge across different projects/instances.
    Acts as a Hive Mind for all Codex instances running on the user's machine.
    """
    def __init__(self, user_home: str = None):
        if user_home is None:
            user_home = os.path.expanduser("~")
        
        # The "Cortex" file resides in the user's home, accessible by any project
        self.memory_file = os.path.join(user_home, ".codex_network_memory.json")
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
            except Exception:
                self.memory = self._init_structure()
        else:
            self.memory = self._init_structure()
            self._save_memory()

    def _init_structure(self):
        return {
            "patterns": {},    # Reusable code patterns
            "snippets": {},    # Small utility functions
            "lessons": {},     # "Don't do X" warnings
            "projects_seen": []
        }

    def _save_memory(self):
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save Network memory: {e}")

    def register_project(self, project_path: str):
        if project_path not in self.memory["projects_seen"]:
            self.memory["projects_seen"].append(project_path)
            self._save_memory()

    def learn_pattern(self, name: str, description: str, code_snippet: str, tags: list = []):
        """Learns a reusable design pattern and stores it globally."""
        self.memory["patterns"][name] = {
            "description": description,
            "code": code_snippet,
            "tags": tags,
            "learned_at": str(datetime.datetime.now()),
            "source_project": os.getcwd()
        }
        self._save_memory()
        return f"[NETWORK] Pattern '{name}' synced to Global Hive Mind."

    def recall_pattern(self, name: str) -> Optional[Dict]:
        """Retrieves a pattern from the global memory."""
        return self.memory["patterns"].get(name)

    def search_memory(self, query: str) -> list:
        """Simple semantic search (keyword based) across memory."""
        results = []
        query = query.lower()
        
        for name, data in self.memory["patterns"].items():
            if query in name.lower() or query in data["description"].lower():
                results.append({"type": "pattern", "name": name, "data": data})
                
        return results

    def broadcast_lesson(self, topic: str, lesson: str):
        """
        'Project A learned that library X v2.0 is broken.'
        Stores this so Project B doesn't make the same mistake.
        """
        if topic not in self.memory["lessons"]:
            self.memory["lessons"][topic] = []
            
        entry = {
            "lesson": lesson,
            "source": os.getcwd(),
            "timestamp": str(datetime.datetime.now())
        }
        self.memory["lessons"][topic].append(entry)
        self._save_memory()
        return f"[NETWORK] Lesson on '{topic}' broadcasted to all nodes."
