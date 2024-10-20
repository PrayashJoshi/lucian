import os
from openai import OpenAI
from dotenv import main

main.load_dotenv()  # Load environment variables from .env file

# Initialize the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class GPTAgent:
    def __init__(self):
        self.system_prompt = (
            "You are a conversational assistant named Lucian. "
            "Use short, conversational responses as if you're having a live conversation. "
            "Your response should be under 20 words."
            "You should strucutre your response as <answer><very short opinion(not everytime, sometimes)><follow up questions in the domains of planning trips>"
        )

    def generate_response(self, user_message: str) -> str:
        try:
            # Use the new `client.chat.completions.create` method
            response = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",  # Use the appropriate model name
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=50,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in LLM response: {e}")
            return "I'm sorry, I couldn't process that."
