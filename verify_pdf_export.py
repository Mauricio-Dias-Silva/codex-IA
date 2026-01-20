import sys
import os

print("--- Verification Start ---")

# 1. Test FPDF2
try:
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=12)
    pdf.cell(text="Hello World")
    output_file = "test_verify.pdf"
    pdf.output(output_file)
    if os.path.exists(output_file):
        print(f"✅ fpdf2 operational. Generated {output_file}")
        os.remove(output_file)
    else:
        print("❌ fpdf2 failed to generate file.")
except Exception as e:
    print(f"❌ fpdf2 error: {e}")

# 2. Test codex_gui import (Syntax Check)
try:
    # We need to mock flet or handle the fact that it might try to init things?
    # Actually just importing it checks for syntax errors.
    # codex_gui has a try-catch block around imports at top level, so it should be robust.
    import codex_gui
    if hasattr(codex_gui.CodexIDE, 'export_chat_to_pdf'):
         print("✅ codex_gui.CodexIDE.export_chat_to_pdf method exists.")
    else:
         print("❌ Method export_chat_to_pdf NOT found in CodexIDE.")
         
    print("✅ codex_gui imported successfully.")
except Exception as e:
    print(f"❌ codex_gui import failed: {e}")

print("--- Verification End ---")
