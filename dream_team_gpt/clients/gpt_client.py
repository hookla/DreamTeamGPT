from enum import Enum
import json
import time

from loguru import logger
import backoff
import openai

from .base import AIClient

MAX_RETRIES = 6  # Number of retries
RETRY_DELAY = 10  # Delay between retries in seconds


class Models(str, Enum):
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


class GPTClient(AIClient):
    def __init__(self, api_key: str, model: str = Models.GPT3):
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
    def system_instructions(self) -> str:
        return self._system_instructions

    @system_instructions.setter
    def system_instructions(self, value) -> None:
        logger.debug(f"Setting system instructions: {self._system_instructions}")
        self._system_instructions = value

    @property
    def user_prompt(self) -> str:
        return self._user_prompt

    @user_prompt.setter
    def user_prompt(self, value: str) -> None:
        logger.debug(f"Setting user prompt: {self._user_prompt}")
        self._user_prompt = value

    def query(self, transcript: str) -> str:
        if not self._system_instructions:
            logger.error("self._system_instructions is None. Aborting the query.")
            raise RuntimeError("self._system_instructions is None, cannot proceed with query.")
        if not self._user_prompt:
            logger.error("self._user_prompt is None. Aborting the query.")
            raise RuntimeError("self._user_prompt is None, cannot proceed with query.")

        return self._query(transcript)

    @backoff.on_exception(
        backoff.constant, openai.error.RateLimitError, max_tries=MAX_RETRIES, interval=RETRY_DELAY
    )
    def _query(self, transcript: str) -> str:
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
