import asyncio
import re
import json
from ..utils.logger import get_logger
from .communicator import Communicator
from .pagemaker_agent import PagemakerAgent

# Import flight-related agent handlers
from .agents.flight_order_management.handler import flight_order_management
from .agents.flight_offers_price.handler import flight_offers_price
from .agents.flight_offers_search.handler import flight_offers_search
from .agents.flight_availabilities.handler import check_availability
from .agents.flight_seatmap_display.handler import get_seatmap
from .agents.flight_inspiration_search.handler import flight_inspiration_search
from .agents.flight_cheapest_date_search.handler import flight_cheapest_date_search
from .agents.branded_fares_upsell.handler import get_upsell_offers
from .agents.flight_create_orders.handler import flight_create_orders

logger = get_logger(__name__)

class Orchestrator:
    def __init__(self):
        # Mapping agents to functions and JSON metadata
        self.agents = {
            "flight_order_management": (flight_order_management, self.load_metadata("flight_order_management")),
            "flight_offers_price": (flight_offers_price, self.load_metadata("flight_offers_price")),
            "flight_offers_search": (flight_offers_search, self.load_metadata("flight_offers_search")),
            "flight_availabilities": (check_availability, self.load_metadata("flight_availabilities")),
            "flight_seatmap_display": (get_seatmap, self.load_metadata("flight_seatmap_display")),
            "flight_inspiration_search": (flight_inspiration_search, self.load_metadata("flight_inspiration_search")),
            "flight_cheapest_date_search": (flight_cheapest_date_search, self.load_metadata("flight_cheapest_date_search")),
            "branded_fares_upsell": (get_upsell_offers, self.load_metadata("branded_fares_upsell")),
            "flight_create_orders": (flight_create_orders, self.load_metadata("flight_create_orders")),
        }
        self.communicator = Communicator()
        self.pagemaker = PagemakerAgent()
        self.lock = asyncio.Lock()

    def load_metadata(self, agent_name: str) -> dict:
        """Load and validate JSON metadata for each agent."""
        try:
            with open(f"app/agents/{agent_name}/tool.json", "r") as f:
                data = json.load(f)
                # Validate if 'function' key exists
                if "function" not in data:
                    logger.error(f"Invalid metadata: 'function' key missing in {agent_name} JSON.")
                    return {}
                return data
        except FileNotFoundError:
            logger.error(f"Metadata file not found for {agent_name}.")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON for {agent_name}: {e}")
        return {}


    async def process_user_message(self, message: str) -> str:
        """Process user message and delegate tasks to appropriate agents."""
        logger.info(f"Orchestrator received message: {message}")

        # Analyze message using OpenAI
        analysis = await self.communicator.analyze_message(message)
        intent = analysis.get("intent", "").lower()
        parameters = analysis.get("parameters", {})
        openai_response = analysis.get("response", "")
        logger.debug(f"Inferred intent: {intent}, parameters: {parameters}")

        # Determine the best agent based on message content and metadata
        agent_name = self.decide_agent(message)
        if not agent_name:
            logger.info(f"Using OpenAI fallback response: {openai_response}")
            return openai_response or "Could you provide more details?"

        # Retrieve the agent function and metadata
        agent_function, metadata = self.agents.get(agent_name, (None, None))
        if not agent_function:
            return "The requested service is unavailable."

        # Ensure the lock is available
        if self.lock.locked():
            return "I'm currently handling another request. Please try again shortly."

        async with self.lock:
            try:
                # Execute the agent function with provided parameters
                response = agent_function(**parameters)
                return response
            except TypeError as e:
                logger.error(f"Error in agent '{agent_name}': {e}")
                missing_params = self.extract_missing_params(str(e))
                follow_up_question = self.generate_follow_up(missing_params, metadata)
                return follow_up_question

    def decide_agent(self, message: str) -> str:
        """Use JSON metadata to determine the best agent."""
        best_match = None
        highest_score = 0

        for agent_name, (_, metadata) in self.agents.items():
            if not metadata:
                logger.warning(f"Skipping {agent_name} due to missing metadata.")
                continue  # Skip agents without valid metadata

            score = self.calculate_relevance_score(message, metadata)
            if score > highest_score:
                best_match = agent_name
                highest_score = score

        return best_match


    def calculate_relevance_score(self, message: str, metadata: dict) -> int:
        """Calculate a relevance score based on message and metadata."""
        score = 0

        description = metadata.get("function", {}).get("description", "").lower()
        if not description:
            logger.warning("Skipping scoring due to missing description.")
            return score

        keywords = re.findall(r"\b\w+\b", description)
        for word in keywords:
            if word in message.lower():
                score += 1

        parameters = metadata.get("function", {}).get("parameters", {}).get("properties", {}).keys()
        for param in parameters:
            if param in message.lower():
                score += 2

        return score


    def extract_missing_params(self, error_message: str) -> list:
        """Extract missing parameters from the TypeError message."""
        pattern = r"missing (\d+) required positional arguments?: (.+)"
        match = re.search(pattern, error_message)
        if match:
            params = match.group(2).replace("'", "").split(", ")
            return [param.strip() for param in params]
        return []

    def generate_follow_up(self, missing_params: list, metadata: dict) -> str:
        """Generate a follow-up question based on missing parameters."""
        param_list = ", ".join(missing_params)
        function_name = metadata["function"]["name"].replace("_", " ").title()
        return f"To proceed with {function_name}, I need the following: {param_list}. Could you provide those details?"
