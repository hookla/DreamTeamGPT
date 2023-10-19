import os
from time import time

import openai
from dotenv import load_dotenv
from loguru import logger

logger.disable(__name__)

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("openai.api_key")
openai.api_key = api_key


class GPTClient:
    def __init__(self, common_instructions: str, user_prompt: str, model: str = "gpt-4"):
        self.system_instructions = common_instructions
        self.user_prompt = user_prompt
        self.model = model
        self.max_tokens = 100
        self.temperature: float = 0.6
        # Log initial configuration on startup
        logger.info(f"Initializing GPTClient with the following configuration:")
        logger.info(f"System Instructions: {self.system_instructions}")
        logger.info(f"User Prompt: {self.user_prompt}")
        logger.info(f"Model: {self.model}")
        logger.info(f"Max Tokens: {self.max_tokens}")
        logger.info(f"Temperature: {self.temperature}")


    def query(self, transcript: str) -> str:
        start_time = time()

        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": self.system_instructions},
                {"role": "assistant", "content": transcript},
                {"role": "user", "content": self.user_prompt}
            ]
        )

        end_time = time()
        elapsed_time = end_time - start_time

        # Log the time taken and token usage
        logger.info(f"GPT query took {elapsed_time:.2f} seconds")
        logger.info(f"Tokens used in the request: {response['usage']['total_tokens']}")

        return response.choices[0].message.content.strip()
