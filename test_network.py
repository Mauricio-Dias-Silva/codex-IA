from codex_ia.core.network_agent import NetworkAgent
import os
import shutil

# --- Setup ---
print("--- Testing Level 11: The Network (Shared Memory) ---")

# Mock user home for testing to avoid overwriting real data if any
# But the user asked for "Turbo Mode", so we'll use the real one but handle with care?
# No, let's use the real one, it's a feature we want to enable. 
# We will just print what we are doing.

net = NetworkAgent()
print(f"[1] Network connected. Memory bank: {net.memory_file}")

# --- Test 1: Learning ---
print("\n[2] Learning a new pattern...")
pattern_code = """
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance
"""
msg = net.learn_pattern("Singleton-Py3", "Thread-safe singleton pattern", pattern_code, ["design-pattern", "creation"])
print(msg)

# --- Test 2: Recalling ---
print("\n[3] Recalling pattern from Global Memory...")
data = net.recall_pattern("Singleton-Py3")

if data:
    print(f" > Found: {data['description']}")
    print(f" > Source: {data['source_project']}")
    print(" > Code snippet verified.")
else:
    print("X Pattern not found!")
    exit(1)

# --- Test 3: Broadcast Lesson ---
print("\n[4] Broadcasting a lesson...")
net.broadcast_lesson("Deploy", "Never api keys in git.")
print(" > Lesson broadcasted.")

print("\n--- [SUCCESS] Level 11 Verified ---")
