import os

import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("openai.api_key")
openai.api_key = api_key


class GPTClient:
    def __init__(self, common_instructions: str, model: str = "gpt-4"):
        self.common_instructions = common_instructions
        self.model = model

    def query(self, prompt: str, max_tokens: int, temperature: float = 0.3) -> str:
        final_prompt = f"{self.common_instructions} {prompt}"
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=temperature,
            messages=[{"role": "user", "content": final_prompt}]
        )
        return response.choices[0].message.content.strip()
