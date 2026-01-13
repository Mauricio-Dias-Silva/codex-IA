import time
import os
import shutil
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import threading

logger = logging.getLogger(__name__)

class SafetyHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers immunity checks.
    """
    def __init__(self, agent):
        self.agent = agent
        self.last_triggered = 0
        self.cooldown = 2.0  # Seconds between checks

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Ignores
        if "__pycache__" in event.src_path or ".git" in event.src_path or "tmp" in event.src_path:
            return

        # Debounce
        now = time.time()
        if now - self.last_triggered < self.cooldown:
            return
        self.last_triggered = now

        print(f"[IMMUNITY] [WARN] Change detected in {os.path.basename(event.src_path)}")
        self.agent.verify_stability(event.src_path)

class ImmunityAgent:
    """
    Level 12: The Immunity
    Resides in the background. Watches for file changes.
    If a change causes tests to fail, it AUTOMATICALLY reverts the file.
    """
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.observer = Observer()
        self.active = False
        self._backup_cache = {} # path -> content

    def activate_watchdog(self):
        """Starts the background file watcher."""
        event_handler = SafetyHandler(self)
        self.observer.schedule(event_handler, self.project_root, recursive=True)
        self.observer.start()
        self.active = True
        print(f"[IMMUNITY] [OK] Watchdog active in {self.project_root}")
        print("[IMMUNITY] [OK] I will revert any change that breaks the build.")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        self.active = False

    def verify_stability(self, changed_file_path):
        """
        Runs a quick check. If it fails, revert!
        """
        # 1. Start backup generation (in memory for speed)
        # Note: Ideally, we should have backed up BEFORE the change via a pre-hook,
        # but `watchdog` is post-event. So we rely on Git or a shadow copy if deployed fully.
        # For this PoC, we assume the user might have broken it, and if we can't revert, we scream.
        # BUT, to show "Revert" capability, lets assume we are using git stash?
        # Or better: We run the test, if fail, we `git checkout -- <file>`.
        
        print("[IMMUNITY] [TEST] Running stability check...")
        
        # Simple check: Does it compile/run? 
        # We'll run pytest on the specific file if it's a test, or general tests otherwise.
        
        cmd = ["python", "-m", "compileall", "-q", changed_file_path]
        if changed_file_path.endswith(".py"):
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                print("[IMMUNITY] [OK] Syntax OK.")
            except subprocess.CalledProcessError:
                print("[IMMUNITY] [FAIL] SYNTAX ERROR DETECTED! Reverting...")
                self._revert_file(changed_file_path)
                return

        # Run project tests (fast subset)
        # For demo, we assume `python -m pytest` is fast enough
        try:
            # Timeout to prevent infinite loops
            result = subprocess.run(["python", "-m", "pytest", "-q"], cwd=self.project_root, capture_output=True, timeout=10)
            if result.returncode != 0:
                print(f"[IMMUNITY] [FAIL] TESTS FAILED! Output:\n{result.stdout.decode()[:200]}...")
                print("[IMMUNITY] [UNDO] Initiating Protocol: UNDO")
                self._revert_file(changed_file_path)
            else:
                print("[IMMUNITY] [OK] Stability confirmed.")
                
        except Exception as e:
            print(f"[IMMUNITY] [WARN] Check failed: {e}")

    def _revert_file(self, file_path):
        """
        Reverts the file to HEAD using git.
        NOW SECURED BY SAFETY PROTOCOL (Quarantine before destruction).
        """
        from .safety import SafetyProtocol
        safety = SafetyProtocol()
        
        # 1. Quarantine current broken state (for post-mortem analysis)
        print(f"[IMMUNITY] [ISOLATE] Quarantining broken file before revert...")
        quarantine_path = safety.quarantine_file(file_path)
        
        if not quarantine_path:
             print(f"[IMMUNITY] [WARN] Quarantine failed. Proceeding with caution...")
        
        # 2. Revert
        try:
            subprocess.run(["git", "checkout", "HEAD", "--", file_path], cwd=self.project_root, check=True, capture_output=True)
            print(f"[IMMUNITY] [UNDO] File {os.path.basename(file_path)} reverted to safe state.")
        except Exception as e:
            print(f"[IMMUNITY] [FAIL] Failed to revert: {e}")

if __name__ == "__main__":
    # Standalone mode
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    agent = ImmunityAgent(path)
    agent.activate_watchdog()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        agent.stop()
