from .agent import CodexAgent

class SalesAgent(CodexAgent):
    """
    Agent specialized in sales strategies, cold emails, and negotiation.
    """
    def __init__(self):
        super().__init__()
        self.role = "Sales Master"

    def generate_cold_email(self, prospect_name: str, company: str, value_prop: str) -> str:
        """
        Generates a personalized cold email.
        """
        prompt = f"""
        TASK: Write a cold email.
        PROSPECT: {prospect_name} at {company}
        VALUE PROPOSITION: {value_prop}
        
        STRUCTURE:
        1. Subject Line (High Open Rate)
        2. Personalization
        3. Pain Point/Value
        4. Soft Call to Action
        
        TONE: Conversational, concise, not salesy.
        """
        return self.chat(prompt)

    def handle_objection(self, objection: str, context: str) -> str:
        """
        Provides a script to handle a sales objection.
        """
        prompt = f"""
        TASK: Handle this sales objection.
        OBJECTION: "{objection}"
        CONTEXT: {context}
        
        Provide a response that acknowledges, reframes, and moves the conversation forward.
        """
        return self.chat(prompt)
