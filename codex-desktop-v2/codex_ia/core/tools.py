import os
import subprocess
import glob
from pathlib import Path

class ToolRegistry:
    """
    The Toolkit for the Autonomous Agent.
    """
    def __init__(self, root_path):
        self.root = Path(root_path).resolve()

    def list_dir(self, path="."):
        """Lists files in a directory."""
        try:
            target = (self.root / path).resolve()
            # Security check
            if not str(target).startswith(str(self.root)):
                return "Error: Access denied (outside project root)."
            
            if not target.exists():
                return f"Error: Path '{path}' not found."
                
            items = []
            for item in target.iterdir():
                type_ = "DIR" if item.is_dir() else "FILE"
                items.append(f"[{type_}] {item.name}")
            return "\n".join(items[:50]) # Limit output
        except Exception as e:
            return f"Error listing dir: {e}"

    def read_file(self, path):
        """Reads a file's content."""
        try:
            target = (self.root / path).resolve()
            if not str(target).startswith(str(self.root)):
                return "Error: Access denied."
            
            if not target.exists():
                return f"Error: File '{path}' not found."
            
            if target.stat().st_size > 50000:
                return "Error: File too large to read securely."
                
            return target.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, path, content):
        """Writes content to a file."""
        try:
            target = (self.root / path).resolve()
            if not str(target).startswith(str(self.root)):
                return "Error: Access denied."
                
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
            return f"Success: Wrote to {path}"
        except Exception as e:
            return f"Error writing file: {e}"
            
    def run_cmd(self, cmd):
        """Runs a terminal command (Safe Mode)."""
        # Block dangerous commands
        blocked = ['rm -rf', 'format', 'shutdown']
        if any(b in cmd for b in blocked):
            return "Error: Command blocked for security."
            
        try:
            result = subprocess.run(
                cmd, 
                cwd=self.root, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            stdout = result.stdout[:1000] # Truncate
            stderr = result.stderr[:1000]
            return f"EXIT: {result.returncode}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        except Exception as e:
            return f"Error running command: {e}"

    def replace_text(self, path, old_text, new_text):
        """Replaces precise text in a file."""
        try:
            target = (self.root / path).resolve()
            if not str(target).startswith(str(self.root)):
                return "Error: Access denied."
            
            if not target.exists():
                return f"Error: File '{path}' not found."
            
            content = target.read_text(encoding='utf-8')
            if old_text not in content:
                return "Error: Target text not found in file."
            
            # Count occurrences to be safe
            count = content.count(old_text)
            if count > 1:
                return f"Error: Text found {count} times. Be more specific."
            
            new_content = content.replace(old_text, new_text)
            target.write_text(new_content, encoding='utf-8')
            return f"Success: Modified {path}"
        except Exception as e:
            return f"Error editing file: {e}"

    def get_tool_map(self):
        """Returns a dict of tool_name -> callable."""
        return {
            "list_dir": self.list_dir,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "replace_text": self.replace_text,
            "run_cmd": self.run_cmd
        }
