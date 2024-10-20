from .agent_handler import GPTAgent


class Orchestrator:
    def __init__(self):
        self.gpt_agent = GPTAgent()

    def process_user_message(self, message: str) -> str:
        # Use the GPTAgent to generate a response
        return self.gpt_agent.generate_response(message)
