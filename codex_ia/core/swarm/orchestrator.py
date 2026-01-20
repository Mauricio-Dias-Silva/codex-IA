
import threading
import time
from .agent_base import SwarmAgent

class SwarmOrchestrator:
    """Manages the lifecycle and communication of the Swarm."""
    def __init__(self):
        self.agents = {}
        self.message_bus = []
        self.is_active = False

    def register_agent(self, agent: SwarmAgent):
        self.agents[agent.name] = agent
        print(f"🐝 Agent Registered: {agent.name} ({agent.role})")

    def broadcast(self, sender, content):
        """Sends a message to all agents."""
        self.message_bus.append(f"[{sender} -> ALL]: {content}")
        results = {}
        for name, agent in self.agents.items():
            if name != sender:
                results[name] = agent.receive_message(sender, content)
        return results

    def direct_message(self, sender, target, content):
        """Sends a message to a specific agent."""
        self.message_bus.append(f"[{sender} -> {target}]: {content}")
        if target in self.agents:
            return self.agents[target].receive_message(sender, content)
        return None

    def start_mission(self, mission_goal):
        """Initiates a collaborative workflow."""
        print(f"🚀 Mission Started: {mission_goal}")
        self.is_active = True
        
        # 1. Architect analyzes first
        if "Architect" in self.agents:
            plan = self.agents["Architect"].receive_message("USER", f"Mission: {mission_goal}. Create a plan.")
            
            # 2. Architect instructs Developer
            if "Developer" in self.agents and plan:
                code_result = self.agents["Developer"].receive_message("Architect", f"Execute this plan: {plan}")
                
                # 3. QA tests the result
                if "QA" in self.agents and code_result:
                    report = self.agents["QA"].receive_message("Developer", f"Test this code: {code_result}")
                    return report
        
        return "Mission Complete (Simulated Flow)"
