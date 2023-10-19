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
        self.common_instructions = "For the duration of this conversation, provide raw, concise opinions without any politeness or filler words. Focus on progressing the solution in a tangible way. Avoid generic statements and repetition of points already made. Ensure all comments are directly relevant to the conversation. If you cannot meet these criteria, respond with 'no comment.'

    def query_gpt(self, prompt: str, max_tokens: int) -> str:
        final_prompt = f"{self.common_instructions} {prompt}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            temperature=0.3,
            messages=[{"role": "user", "content": final_prompt}]
        )
        return response.choices[0].message.content.strip()
