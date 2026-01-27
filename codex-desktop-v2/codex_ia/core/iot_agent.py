from .agent import CodexAgent

class IoTAgent(CodexAgent):
    """
    Agent specialized in embedded systems and firmware generation.
    """
    def __init__(self):
        super().__init__()
        self.role = "IoT Engineer"

    def generate_firmware(self, platform: str, description: str) -> str:
        """
        Generates firmware code for a specific platform (ESP32, Arduino, etc.)
        based on a natural language description.
        """
        prompt = f"""
        ACT AS: Expert Embedded Systems Engineer.
        TASK: Write complete, compile-ready firmware code for {platform}.
        
        REQUIREMENTS:
        - Functionality: {description}
        - Platform: {platform}
        - Comments: Explain key parts of the code.
        - Libraries: Use standard or common libraries for the platform.
        - Error Handling: Include basic error handling where appropriate.
        
        OUTPUT FORMAT:
        Return ONLY the code block (e.g., inside ```cpp or ```python).
        """
        
        return self.chat(prompt)
