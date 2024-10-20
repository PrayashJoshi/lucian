# app/services/communicator.py

import json
import httpx
from ..utils.logger import get_logger
from ..utils.config import Config

logger = get_logger(__name__)

class Communicator:
    def __init__(self):
        self.api_key = Config.OPENAI_API_KEY
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.system_prompt = (
            "You are Lucian, an enthusiastic travel assistant. "
            "Generate short, concise responses limited to 30 words. "
            "Write in the style of an enthusiastic travel agent, providing clear and friendly information. "
            "Ensure responses are realistic, context-aware, and based on the data provided."
        )

    async def analyze_message(self, message: str) -> dict:
        """
        Analyze the user's message and return inferred intent.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": message}
            ],
            "max_tokens": 150,
            "temperature": 0.5  # Allow for more natural, flexible responses
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content'].strip()
                logger.info(f"OpenAI Response: {content}")

                # Assume the response contains the identified intent or action directly.
                return {"intent": content}
        except httpx.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decode error: {json_err}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

        # Default to returning an empty intent if the request fails
        return {"intent": ""}


    def is_analysis_complete(self, analysis: dict) -> bool:
        """
        Check if all required fields (context, need, goal) are present.
        """
        required_fields = ["context", "need", "goal"]
        completeness = all(analysis.get(field) for field in required_fields)
        logger.debug(f"Is Analysis Complete: {completeness}")
        return completeness

    async def request_clarification(self, analysis: dict) -> str:
        """
        Generate a clarification prompt based on missing information.
        """
        missing_fields = [field for field in ["context", "need", "goal"] if not analysis.get(field)]
        if not missing_fields:
            return ""
        clarification_prompt = (
            f"I need more information to assist you effectively. Please provide details on: {', '.join(missing_fields)}."
        )
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "Generate a concise clarification question."},
                {"role": "user", "content": clarification_prompt}
            ],
            "max_tokens": 50,
            "temperature": 0.5  # Adds slight variability for naturalness
        }

        try:
           async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, headers=headers, json=payload)
                
                # Log the raw response for debugging
                logger.info(f"OpenAI API raw response: {response.text}")

                response.raise_for_status()
                data = response.json()  # This line might be failing

                clarification = data['choices'][0]['message']['content'].strip()
                logger.info(f"Clarification Prompt: {clarification}")
                return clarification
        except httpx.HTTPError as http_err:
            logger.error(f"HTTP error occurred during clarification request: {http_err}")
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON decode error: {json_err}")
        except Exception as e:
            logger.error(f"Unexpected error during clarification request: {e}")

        return "Could you please provide more details?"
