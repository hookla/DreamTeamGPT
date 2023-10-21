import json
import os
from time import time

import openai
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("openai.api_key")

if not api_key:
    raise ValueError("API key not found in environment variables")

openai.api_key = api_key

GPT3 = "gpt-3.5-turbo"
GPT4 = "gpt-4"


class GPTClient:
    def __init__(
            self, system_instructions: str, user_prompt: str, model: str = GPT4
    ):
        self.system_instructions = system_instructions
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
        max_retries = 6  # Number of retries
        retry_delay = 10  # Delay between retries in seconds

        for i in range(max_retries):
            try:
                start_time = time()
                messages = [
                    {"role": "system", "content": self.system_instructions},
                    {"role": "user", "content": self.user_prompt},
                    {"role": "assistant", "content": transcript},
                ]
                logger.info(json.dumps(messages, indent=4).replace("\\n", "\n"))

                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    messages=messages,
                )

                end_time = time()
                elapsed_time = end_time - start_time

                # Log the time taken and token usage
                logger.info(f"GPT query took {elapsed_time:.2f} seconds")
                logger.info(f"Tokens used in the request: {response['usage']}")

                return response.choices[0].message.content.strip()
            except openai.error.RateLimitError as e:
                logger.warning(f"Rate limit reached. Retrying in {retry_delay} seconds. Details: {e}")
                time.sleep(retry_delay)

        logger.error(f"Max retries reached. Could not complete the GPT query.")
        return "Rate limit reached. Could not complete the request."
