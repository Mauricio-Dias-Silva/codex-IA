import os
import logging
from .brain_router import BrainRouter

class GhostAgent:
    def __init__(self, project_root):
        self.project_root = project_root
        self.brain = BrainRouter()

    def haunting(self, file_path, content):
        """
        The Ghost Agent 'haunts' the file. 
        If it detects a pattern (like a Django Model), it invisibly manifests the companion files.
        """
        filename = os.path.basename(file_path)
        
        # 👻 Trigger: Saving models.py (Django)
        if filename == "models.py":
            self._manifest_django_admin(file_path, content)
            self._manifest_django_serializer(file_path, content)

    def _manifest_django_admin(self, models_path, models_content):
        """
        Auto-generates admin.py based on models.
        """
        admin_path = models_path.replace("models.py", "admin.py")
        
        # Only haunt if the spot is empty or doesn't exist
        if os.path.exists(admin_path) and os.path.getsize(admin_path) > 50:
            return # Already occupied

        prompt = f"""
        You are a Ghost Writer. The user just wrote this Django `models.py`.
        Generate a complete `admin.py` file to register these models.
        Use `@admin.register` decorators.
        Make it production-ready (list_display, search_fields).

        MODELS CONTENT:
        {models_content}

        Output ONLY the python code for admin.py.
        """
        
        try:
            logging.info(f"👻 Ghost Mode: Manifesting admin.py for {models_path}...")
            ghost_code = self.brain.send_message(prompt, task_type="coding")
            
            # Clean md blocks
            ghost_code = ghost_code.replace("```python", "").replace("```", "").strip()
            
            with open(admin_path, "w", encoding="utf-8") as f:
                f.write(ghost_code)
            
            logging.info(f"👻 Ghost Mode: Created {admin_path}")
            return True
        except Exception as e:
            logging.error(f"Ghost failed to manifest admin: {e}")

    def _manifest_django_serializer(self, models_path, models_content):
        """
        Auto-generates serializers.py based on models.
        """
        serializers_path = models_path.replace("models.py", "serializers.py")
        
        if os.path.exists(serializers_path) and os.path.getsize(serializers_path) > 50:
            return 

        prompt = f"""
        You are a Ghost Writer. The user just wrote this Django `models.py`.
        Generate a complete `serializers.py` using Django Rest Framework.
        Create a ModelSerializer for each model.

        MODELS CONTENT:
        {models_content}

        Output ONLY the python code for serializers.py.
        """
        
        try:
            logging.info(f"👻 Ghost Mode: Manifesting serializers.py for {models_path}...")
            ghost_code = self.brain.send_message(prompt, task_type="coding")
             # Clean md blocks
            ghost_code = ghost_code.replace("```python", "").replace("```", "").strip()
            
            with open(serializers_path, "w", encoding="utf-8") as f:
                f.write(ghost_code)
                
            logging.info(f"👻 Ghost Mode: Created {serializers_path}")
            return True
        except Exception as e:
            logging.error(f"Ghost failed to manifest serializers: {e}")
