
import logging
import uuid
import datetime

class SwarmAgent:
    """Base class for all Swarm Agents (Architect, Dev, QA)."""
    def __init__(self, name, role, color="white"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = role
        self.color = color
        self.memory = []
        
    def receive_message(self, sender, content):
        """Receives a message from the orchestrator or another agent."""
        msg = {
            "from": sender,
            "content": content,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.memory.append(msg)
        return self.process_message(msg)

    def process_message(self, message):
        """Override this in subclasses."""
        return f"{self.name} acknowledged: {message['content'][:20]}..."

    def log(self, msg):
        print(f"[{self.role.upper()}] {self.name}: {msg}")
