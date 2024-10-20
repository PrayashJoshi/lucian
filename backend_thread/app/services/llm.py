import httpx
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def query_llm(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 100,
            },
        )
        return response.json()["choices"][0]["message"]["content"]
