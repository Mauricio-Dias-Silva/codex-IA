
import os
from pathlib import Path
from typing import List, Dict

class ContextManager:
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        # Default ignores
        self.ignore_dirs = {'.git', 'venv', '.venv', '__pycache__', '.idea', '.vscode', 'node_modules', 'dist', 'build'}
        self.ignore_exts = {'.pyc', '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.exe', '.dll', '.bin', '.svg', '.ico'}
        self.gitignore_rules = self._load_gitignore()
        
        # [OPTIMIZATION] Local Memory Integration 🧠
        try:
            from codex_ia.core.vector_store import CodexVectorStore
            from codex_ia.core.global_store import GlobalVectorStore
            self.vector_store = CodexVectorStore(persistence_path=str(self.root / ".codex_memory"))
            self.global_store = GlobalVectorStore()
        except Exception:
            self.vector_store = None
            self.global_store = None

    def _load_gitignore(self) -> List[str]:
        """Loads patterns from .gitignore if it exists."""
        gitignore_path = self.root / '.gitignore'
        patterns = []
        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            patterns.append(line)
            except Exception:
                pass
        return patterns

    def _is_ignored(self, path: Path) -> bool:
        """Simple check for ignored files/dirs. 
        Note: A robust implementation would use `pathspec` or `gitpython`.
        For now, we check basic names and extensions."""
        
        # Check against basic sets
        if path.name in self.ignore_dirs:
            return True
        if path.suffix in self.ignore_exts:
            return True
            
        # Check if path contains any ignored directory part relative to root
        try:
            rel_path = path.relative_to(self.root)
            for part in rel_path.parts:
                if part in self.ignore_dirs:
                    return True
        except ValueError:
            pass
            
        return False

    def list_files(self) -> List[str]:
        """
        Returns a list of all non-ignored files in the repository.
        """
        file_list = []
        for root, dirs, files in os.walk(self.root):
            # Modify dirs in-place to skip ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if not self._is_ignored(file_path):
                    try:
                        rel_path = file_path.relative_to(self.root)
                        file_list.append(str(rel_path).replace('\\', '/'))
                    except ValueError:
                        pass
        return sorted(file_list)


    def build_graph(self) -> str:
        """
        [LEVEL 4] Scans all Python files to understand imports and classes.
        Returns a high-level description of the project architecture.
        """
        import ast
        from codex_ia.core.knowledge_base import KnowledgeBase
        
        kb = KnowledgeBase(str(self.root / ".codex_memory.json"))
        graph_desc = ["PROJECT ARCHITECTURE GRAPH:"]
        
        all_files = self.list_files()
        graph_desc.append(f"Total files: {len(all_files)}")
        
        modules = {} # filename -> {imports: [], classes: [], functions: []}
        
        for rel_path in all_files:
            if not rel_path.endswith('.py'):
                continue
                
            file_path = self.root / rel_path
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                tree = ast.parse(content)
                
                info = {"imports": [], "classes": [], "functions": []}
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for n in node.names:
                            info["imports"].append(n.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            info["imports"].append(node.module)
                    elif isinstance(node, ast.ClassDef):
                        info["classes"].append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        if not node.name.startswith('_'): # Skip private
                            info["functions"].append(node.name)
                            
                modules[rel_path] = info
                
                # Store lightweight summary in KB
                summary = f"Module {rel_path} defines classes {info['classes']} and functions {info['functions']}"
                kb.update_file_summary(rel_path, summary, "HASH_TODO")
                
            except Exception:
                pass
        
        # Save KB
        kb.save()
        
        # Build Text Description
        for f, data in modules.items():
            if data['classes'] or data['functions']:
                graph_desc.append(f"\nFILE: {f}")
                if data['classes']:
                    graph_desc.append(f"  Classes: {', '.join(data['classes'])}")
                if data['functions']:
                    graph_desc.append(f"  Functions: {', '.join(data['functions'][:5])}...")
                if data['imports']:
                    # Only show internal imports (simplified heuristic)
                    internal = [i for i in data['imports'] if i.startswith('dashboard') or i.startswith('codex_ia')]
                    if internal:
                        graph_desc.append(f"  Internal Imports: {', '.join(internal)}")

        return "\n".join(graph_desc)

    def get_context(self, specific_files: List[str] = None) -> str:
        """
        Enhanced get_context that includes the Graph summary if no specific files requested.
        """
        buffer = []
        
        # If specific list is provided, only read those
        if specific_files is not None:
            for file_path_str in specific_files:
                file_path = self.root / file_path_str
                if file_path.exists() and not self._is_ignored(file_path):
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        buffer.append(f"--- FILE: {file_path_str} ---\n{content}\n")
                    except Exception:
                        pass
            return "\n".join(buffer)

        # Legacy behavior + Graph
        graph = self.build_graph()
        buffer.append(graph)
        buffer.append("\n\n--- DETAILED SOURCE CODE BELOW ---\n")
        
        # Read files (limited size)
        for root, dirs, files in os.walk(self.root):
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs]
            
            for file in files:
                file_path = Path(root) / file
                if self._is_ignored(file_path):
                    continue
                
                try:
                    if file_path.stat().st_size > 50 * 1024: # Smaller limit for auto-context
                        buffer.append(f"--- FILE: {file_path.relative_to(self.root)} (SKIPPED - TOO LARGE) ---\n")
                        continue

                    # Only read relevant source files for auto-context
                    if file_path.suffix not in ['.py', '.js', '.html', '.css', '.md']:
                        continue

                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if '\0' in content: 
                            continue
                            
                        relative_path = file_path.relative_to(self.root)
                        buffer.append(f"--- FILE: {relative_path} ---\n{content}\n")
                except Exception:
                    continue
                    
        return "\n".join(buffer)

    def get_semantic_context(self, query: str, n_results: int = 15) -> str:
        """
        [PHASE 5] Semantic Context Retrieval.
        Uses the local vector store to find the most relevant snippets for a query.
        This drastically reduces token usage and costs.
        """
        if not self.vector_store:
            # If no index, fallback to high-level graph
            return "Neural Memory not found. Falling back to Architecture Map:\n" + self.build_graph()
            
        try:
            hits = self.vector_store.semantic_search(query, n_results=n_results)
            
            if not hits:
                return "No relevant context found in neural memory. Using Architecture Map:\n" + self.build_graph()
                
            context_parts = ["--- SEMANTIC CONTEXT (Neural Retrieval) ---"]
            context_parts.append(f"Query: {query}\n")
            
            for hit in hits:
                path = hit.get('path', 'unknown')
                score = hit.get('score', 0)
                snippet = hit.get('snippet', '')
                
                context_parts.append(f"\n[Snippet from: {path}] (Relevance: {1-score:.2f})")
                context_parts.append(snippet)
                
            # [PHASE 6] Add Global Knowledge 🌍
            if self.global_store:
                global_hits = self.global_store.search_universal(query, n_results=3)
                if global_hits:
                    context_parts.append("\n--- UNIVERSAL KNOWLEDGE (Cross-Project Memory) ---")
                    for ghit in global_hits:
                        context_parts.append(f"\n[Source: {ghit['source']} | Topic: {ghit['topic']}]")
                        context_parts.append(ghit['snippet'])

            return "\n".join(context_parts)
            
        except Exception as e:
            return f"Error during semantic retrieval: {e}"

    def get_file_context(self, file_path: str) -> str:
        """
        Reads a specific file with line numbers for better referencing.
        """
        # Resolve path relative to root if it looks relative
        target_path = Path(file_path)
        if not target_path.is_absolute():
            target_path = (self.root / file_path).resolve()
            
        if not target_path.exists():
            return f"Error: File {file_path} not found."
        
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            numbered_lines = []
            for i, line in enumerate(lines, 1):
                numbered_lines.append(f"{i}: {line}")
                
            content = "".join(numbered_lines)
            
            try:
                rel_path = target_path.relative_to(self.root)
            except ValueError:
                rel_path = target_path.name
                
            return f"--- FILE: {rel_path} ---\n{content}\n"
        except Exception as e:
            return f"Error reading file: {e}"
