import os

import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("openai.api_key")
openai.api_key = api_key


class GPTClient:
    def __init__(self, common_instructions: str, user_prompt: str, model: str = "gpt-3.5-turbo"):
        self.system_instructions = common_instructions
        self.user_prompt = user_prompt
        self.model = model
        self.max_tokens = 100
        self.temperature: float = 0.3

    def query(self, transcript: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=[{"role": "system", "content": self.system_instructions},
                      {"role": "assistant", "content": transcript},
                      {"role": "user", "content": self.user_prompt}]
        )
        return response.choices[0].message.content.strip()
