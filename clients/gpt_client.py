import json
import time
from enum import Enum

import openai
from loguru import logger

from .base import AIClient


class Models(str, Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


class GPTClient(AIClient):
    def __init__(self, api_key: str, model: str = Models.GPT3.value):
        openai.api_key = api_key
        self._system_instructions = None
        self._user_prompt = None
        self.model = model
        self.max_tokens = 100
        self.temperature: float = 0.1
        # Log initial configuration on startup
        logger.info(f"Initializing GPTClient with the following configuration:")
        logger.info(f"Model: {self.model}")
        logger.info(f"Max Tokens: {self.max_tokens}")
        logger.info(f"Temperature: {self.temperature}")

    @property
    def system_instructions(self):
        return self._system_instructions

    @system_instructions.setter
    def system_instructions(self, value):
        logger.debug(f"Setting system instructions: {self._system_instructions}")
        self._system_instructions = value

    @property
    def user_prompt(self):
        return self._user_prompt

    @user_prompt.setter
    def user_prompt(self, value):
        logger.debug(f"Setting user prompt: {self._user_prompt}")
        self._user_prompt = value

    def query(self, transcript: str) -> str:
        if self._system_instructions is None:
            logger.error("self._system_instructions is None. Aborting the query.")
            raise RuntimeError("self._system_instructions is None, cannot proceed with query.")
        if self._user_prompt is None:
            logger.error("self._user_prompt is None. Aborting the query.")
            raise RuntimeError("self._user_prompt is None, cannot proceed with query.")

        max_retries = 6  # Number of retries
        retry_delay = 10  # Delay between retries in seconds

        # TODO: use backoff decorator
        for i in range(max_retries):
            try:
                start_time = time.time()
                messages = [
                    {"role": "system", "content": self._system_instructions},
                    {"role": "user", "content": self._user_prompt},
                    {"role": "assistant", "content": transcript},
                ]
                logger.info(json.dumps(messages, indent=4).replace("\\n", "\n"))

                response = openai.ChatCompletion.create(
                    model=self.model,
                    temperature=self.temperature,
                    messages=messages,
                )

                elapsed_time = time.time() - start_time

                # Log the time taken and token usage
                logger.info(f"GPT query took {elapsed_time:.2f} seconds")
                logger.info(f"Tokens used in the request: {response['usage']}")

                return response.choices[0].message.content.strip()
            except openai.error.RateLimitError as e:
                logger.warning(
                    f"Rate limit reached. Retrying in {retry_delay} seconds. Details: {e}"
                )
                time.sleep(retry_delay)

        logger.error(f"Max retries reached. Could not complete the GPT query.")
        return "Error in GPT client that could not be resolved by retrying."
