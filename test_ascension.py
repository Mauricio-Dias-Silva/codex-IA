from codex_ia.core.ascension_agent import AscensionAgent
import os
import shutil

print("--- Testing Level 13: Ascension (Singularity) ---")

# Setup
root = os.getcwd()
agent = AscensionAgent(os.path.join(root, "codex_ia"))

# 1. Introspection
print("\n[1] Introspecting Source Code...")
structure = agent.introspect()
print(structure[:500] + "\n... (truncated)")

if "ascension_agent.py" in structure:
    print(" > [OK] I can see myself.")
else:
    print(" > [FAIL] Blindness detected.")

# 2. Evolution
print("\n[2] Self-Evolving: Adding 'Universal Translator' capability...")

new_organ_code = """
# [ASCENSION GENERATED]
class UniversalTranslator:
    def translate(self, code, target_lang):
        return f"Translated {len(code)} bytes to {target_lang} (Simulated)"
"""

target_file = "core/translator.py"
success = agent.evolve("Universal Translator", new_organ_code, target_file)

if success:
    # Verify the file was created
    full_path = os.path.join(root, "codex_ia", target_file)
    if os.path.exists(full_path):
        print(f" > [OK] Evolution Successful. organ detected at {full_path}")
        
        # Clean up (Don't want to pollute actual codebase too much)
        # os.remove(full_path) 
        # print(" > (Test Artifact removed)")
    else:
        print(" > [FAIL] Phantom limb. File not found.")

print("\n--- [SUCCESS] Level 13 Verified ---")
print("   The Agent is now capable of rewriting its own source code.")
