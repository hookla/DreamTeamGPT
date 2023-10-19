import os

import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("openai.api_key")
openai.api_key = api_key


class Agent:
    def __init__(self, name: str):
        self.name = name
        self.common_instructions = "You are an assistant programmed to provide raw, concise opinions without any politeness or filler words.  Focus on progressing the solution in a tangible way.  Do not make generic statements.  Ensure that you comments are directly relevant to the conversation."

    def query_gpt(self, prompt: str, max_tokens: int) -> str:
        final_prompt = f"{self.common_instructions} {prompt}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.3,
            messages=[{"role": "user", "content": final_prompt}]
        )
        return response.choices[0].message.content.strip()
