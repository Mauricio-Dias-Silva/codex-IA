from .agent import CodexAgent

class TutorAgent(CodexAgent):
    """
    Agent specialized in teaching programming concepts.
    """
    def __init__(self):
        super().__init__()
        self.role = "Coding Tutor"
        self.system_prompt_extras = """
        You are a friendly and patient coding tutor. 
        Your goal is to explain complex programming concepts in simple terms.
        Use analogies, examples, and emoji to make learning fun.
        If the user asks for code, provide it with clear explanations.
        """

    def explain_concept(self, concept: str, level: str = "beginner") -> str:
        """
        Explains a specific programming concept tailored to the user's level.
        """
        prompt = f"""
        Explain the concept: "{concept}"
        Target Audience Level: {level}
        
        Structure your response:
        1. Simple Definition (What is it?)
        2. Real-world Analogy (Like a...)
        3. Code Example (Show me!)
        4. Why it's useful.
        """
        return self.chat(prompt)

    def chat(self, message: str) -> str:
        """
        Override chat to enforce the tutor persona more strictly if needed.
        """
        # We can prepend the persona instruction if the base class doesn't persist it strongly enough,
        # but for now, the system_prompt_extras (if supported by base) or just direct prompt engineering works.
        # Assuming base CodexAgent.chat handles history.
        
        # We wrap the message to remind the AI of its role if necessary, or just pass through.
        # Let's pass through but ensure the context knows it's a tutor session.
        return super().chat(message)
