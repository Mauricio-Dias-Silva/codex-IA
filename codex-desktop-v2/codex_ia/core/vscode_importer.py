import os
import json
import logging

class VSCodeImporter:
    """
    Imports settings from the user's local VS Code installation.
    Target: %APPDATA%/Code/User/settings.json
    """
    def __init__(self):
        self.settings_path = os.path.join(os.environ.get('APPDATA', ''), 'Code', 'User', 'settings.json')
        self.keybindings_path = os.path.join(os.environ.get('APPDATA', ''), 'Code', 'User', 'keybindings.json')

    def get_settings(self):
        """
        Reads and parses the VS Code settings.json file.
        Returns a simplified dict with semantic keys for Codex.
        """
        if not os.path.exists(self.settings_path):
            return {"error": "VS Code settings not found"}

        try:
            # VS Code JSON allows comments, standard json lib might fail if comments exist.
            # We'll use a simple approach: Read and strip comments if possible, or try raw.
            # Ideally we'd use 'json5' or 'jsmin', but let's try to handle basic // comments
            content = ""
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith('//'):
                        continue
                    content += line
            
            # Simple fallback for comments inside lines (naive)
            # content = re.sub(r'//.*', '', content) 
            
            # Try parsing
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                # Fallback: try to return default compatible settings if parse fails
                logging.error("Failed to parse VS Code settings (Comments?)")
                return {"fontFamily": "Consolas", "fontSize": 14, "theme": "vs-dark"}

            # Extract relevant fields
            return {
                "fontFamily": data.get("editor.fontFamily", "Consolas"),
                "fontSize": data.get("editor.fontSize", 14),
                "isLigatures": data.get("editor.fontLigatures", False),
                "cursorStyle": data.get("editor.cursorStyle", "line"),
                "tabSize": data.get("editor.tabSize", 4),
                "theme": data.get("workbench.colorTheme", "Default Dark+")
            }
        except Exception as e:
            logging.error(f"Error reading VS Code settings: {e}")
            return {"error": str(e)}
