
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class SentinelHandler(FileSystemEventHandler):
    """
    Handles file system events and triggers callbacks.
    """
    def __init__(self, callback):
        self.callback = callback
        self.last_event_time = 0
        self.debounce_seconds = 1 # Avoid double firing for same save

    def on_modified(self, event):
        if event.is_directory:
            return
        
        # Debounce
        current_time = time.time()
        if current_time - self.last_event_time < self.debounce_seconds:
            return
        self.last_event_time = current_time

        # Filter relevant files
        if event.src_path.endswith(('.py', '.md', '.html', '.css', '.js')):
            self.callback(event.src_path)

class Sentinel:
    """
    [PHASE 6] THE SENTINEL 👁️
    Watchdog that monitors the project for changes and auto-updates memory.
    """
    def __init__(self, project_path, on_change_callback):
        self.project_path = project_path
        self.callback = on_change_callback
        self.observer = Observer()
        self.handler = SentinelHandler(self._internal_callback)
        self.running = False

    def _internal_callback(self, file_path):
        """Internal wrapper to log and call the actual callback."""
        # print(f"👁️ Sentinel saw: {file_path}")
        if self.callback:
            self.callback(file_path)

    def start(self):
        if not self.running:
            self.observer.schedule(self.handler, self.project_path, recursive=True)
            self.observer.start()
            self.running = True

    def stop(self):
        if self.running:
            self.observer.stop()
            self.observer.join()
            self.running = False
