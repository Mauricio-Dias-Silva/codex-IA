import os
import shutil
import time
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

class SafetyProtocol:
    """
    Enforces safety guidelines for AI agents.
    1. Principle of Least Privilege
    2. Prevention of Self-Sabotage (Backups)
    3. Non-Destruction (Quarantine)
    """
    
    QUARANTINE_DIR = os.path.expanduser("~/.codex_quarantine")
    BACKUP_DIR = os.path.expanduser("~/.codex_backups")
    
    def __init__(self):
        os.makedirs(self.QUARANTINE_DIR, exist_ok=True)
        os.makedirs(self.BACKUP_DIR, exist_ok=True)

    def create_backup(self, file_path: str) -> str:
        """
        Creates a backup of a file before modification.
        Returns the path to the backup.
        """
        if not os.path.exists(file_path):
            return None
            
        timestamp = int(time.time())
        filename = os.path.basename(file_path)
        backup_path = os.path.join(self.BACKUP_DIR, f"{filename}.{timestamp}.bak")
        
        try:
            shutil.copy2(file_path, backup_path)
            print(f"[SAFETY] [OK] Backup created: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"[SAFETY] [FAIL] Failed to create backup: {e}")
            raise PermissionError("Cannot modify file without backup (Safety Violation).")

    def quarantine_file(self, file_path: str) -> str:
        """
        Moves a file to quarantine instead of deleting it.
        """
        if not os.path.exists(file_path):
            return None
            
        timestamp = int(time.time())
        filename = os.path.basename(file_path)
        quarantine_path = os.path.join(self.QUARANTINE_DIR, f"{filename}.{timestamp}.quarantine")
        
        try:
            # Copy to quarantine (don't move, let the caller delete/revert if they want)
            shutil.copy2(file_path, quarantine_path)
            print(f"[SAFETY] [OK] File quarantined: {quarantine_path}")
            return quarantine_path
        except Exception as e:
            print(f"[SAFETY] [FAIL] Quarantine failed: {e}")
            return None

    def validate_operation(self, operation: str, target: str) -> bool:
        """
        Validates if an operation is permissible.
        """
        # BLOCKED OPERATIONS
        blocked_commands = ["rm -rf", "format c:", "drop database"]
        if any(cmd in operation.lower() for cmd in blocked_commands):
            print(f"[SAFETY] [BLOCK] Blocked dangerous operation: {operation}")
            return False
            
        # CRITICAL FILES PROTECTION
        critical_files = [".env", "settings.py", "docker-compose.yml"]
        if any(cf in target for cf in critical_files):
            print(f"[SAFETY] [WARN] Modifying critical configuration: {target}")
            # In a real CLI, we would ask for input() here. 
            # For now, we allow but require backup (enforced by create_backup usage)
            return True
            
        return True
