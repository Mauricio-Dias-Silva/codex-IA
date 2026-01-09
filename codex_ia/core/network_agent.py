import json
import os
import logging
import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)

@dataclass
class MemoryEntry:
    timestamp: str
    context_tags: List[str]  # e.g., ["django", "auth", "error_handling"]
    content: str             # The lesson or pattern
    type: str                # "pattern", "anti_pattern", "experience"
    source_project: str
    confidence_score: float = 1.0

class CodexMemory:
    """
    The Hippocampus of Codex.
    Manages Short-Term (Session) and Long-Term (Disk) memory.
    """
    def __init__(self, memory_file: str):
        self.memory_file = memory_file
        self.short_term: List[MemoryEntry] = [] # Cleared on restart/mission end
        self.long_term: Dict[str, List[Dict]] = {
            "patterns": [],
            "anti_patterns": [],
            "experiences": []
        }
        self._load_long_term()

    def _load_long_term(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Migrate old structure if needed
                    if "patterns" in data and isinstance(data["patterns"], dict):
                         # Convert old dict patterns to new list dict
                         new_patterns = []
                         for k, v in data["patterns"].items():
                             new_patterns.append({
                                 "timestamp": v.get("learned_at", str(datetime.datetime.now())),
                                 "context_tags": v.get("tags", []),
                                 "content": json.dumps({k: v}),
                                 "type": "pattern",
                                 "source_project": v.get("source_project", "unknown"),
                                 "confidence_score": 1.0
                             })
                         self.long_term["patterns"] = new_patterns
                    else:
                        self.long_term = data
            except Exception as e:
                logger.error(f"[MEMORY] Corrupt memory file, starting fresh: {e}")
                
    def save(self):
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.long_term, f, indent=2)
        except Exception as e:
            logger.error(f"[MEMORY] Failed to save memory: {e}")

    def add_short_term(self, entry: MemoryEntry):
        self.short_term.append(entry)

    def commit_to_long_term(self, entry: MemoryEntry):
        """Moves an entry to permanent storage."""
        target_list = self.long_term.get(f"{entry.type}s", self.long_term["experiences"])
        target_list.append(asdict(entry))
        self.save()

    def retrieve(self, query_tags: List[str], limit: int = 5) -> List[Dict]:
        """
        Retrieves relevant wisdom based on tags.
        Simple intersection match for now.
        """
        candidates = []
        all_entries = self.long_term["patterns"] + self.long_term["anti_patterns"] + self.long_term["experiences"]
        
        for entry in all_entries:
            # Calculate match score
            score = 0
            entry_tags = entry.get("context_tags", [])
            for tag in query_tags:
                if any(tag.lower() in t.lower() for t in entry_tags):
                    score += 1
            
            if score > 0:
                candidates.append((score, entry))
                
        # Sort by score descending
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [c[1] for c in candidates[:limit]]

class NetworkAgent:
    """
    Level 11: The Network (V2 - Dreaming Monolith)
    """
    def __init__(self, user_home: str = None):
        if user_home is None:
            user_home = os.path.expanduser("~")
        
        self.memory_path = os.path.join(user_home, ".codex_network_memory.json")
        self.memory = CodexMemory(self.memory_path)
        logger.info(f"[NETWORK] Connected to Exocortex at {self.memory_path}")

    def store_experience(self, context: str, action: str, outcome: str, success: bool, tags: List[str] = []):
        """
        Logs a 'Decision Episode'.
        """
        entry_type = "pattern" if success else "anti_pattern"
        content = f"CONTEXT: {context}\nACTION: {action}\nOUTCOME: {outcome}"
        
        entry = MemoryEntry(
            timestamp=str(datetime.datetime.now()),
            context_tags=tags,
            content=content,
            type=entry_type,
            source_project=os.getcwd(),
            confidence_score=1.0 if success else 0.5
        )
        
        self.memory.commit_to_long_term(entry)
        return f"[NETWORK] Wisdom stored: {entry_type} for tags {tags}"

    def retrieve_wisdom(self, context_keywords: List[str]) -> str:
        """
        Fetches relevant advice for the current situation.
        """
        hits = self.memory.retrieve(context_keywords)
        if not hits:
            return "No specific prior wisdom found for this context."
            
        advice = "🧠 **Network Wisdom (Exocortex):**\n"
        for hit in hits:
            icon = "✅" if hit['type'] == 'pattern' else "⚠️"
            advice += f"{icon} [{hit['timestamp']}] {hit['content'][:100]}...\n"
            
        return advice

    # Backwards compatibility for basic calls
    def register_project(self, project_path: str):
        pass 
