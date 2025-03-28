import os

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from loguru import logger

from .base import AIClient


class Models:
    GPT3 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT4O = "gpt-4o"


class GPTClient(AIClient):
    def __init__(self, api_key: str, model: str = Models.GPT4O) -> None:
        self._system_instructions = None
        self._user_prompt = None
        self.model = model
        self.temperature: float = 0.1
        self.api_key = api_key

        # Azure OpenAI environment variables
        self.azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.azure_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT")

        # Create a class variable to track if we've logged initialization info
        if not hasattr(GPTClient, "_logged_init"):
            # Log initial configuration on startup (only once)
            logger.info("Initializing GPTClient with the following configuration:")
            logger.info(f"Model: {self.model}")
            logger.info(f"Temperature: {self.temperature}")
            if self.azure_endpoint:
                logger.info("Using Azure OpenAI endpoint")
            # Mark that we've logged the initialization
            GPTClient._logged_init = True

    @property
    def system_instructions(self) -> str:
        return self._system_instructions

    @system_instructions.setter
    def system_instructions(self, value: str) -> None:
        logger.debug(f"Setting system instructions: {value}")
        self._system_instructions = value

    @property
    def user_prompt(self) -> str:
        return self._user_prompt

    @user_prompt.setter
    def user_prompt(self, value: str) -> None:
        logger.debug(f"Setting user prompt: {value}")
        self._user_prompt = value

    def query(self, transcript: str) -> str:
        if not self._system_instructions:
            logger.error("self._system_instructions is None. Aborting the query.")
            raise RuntimeError("self._system_instructions is None, cannot proceed with query.")
        if not self._user_prompt:
            logger.error("self._user_prompt is None. Aborting the query.")
            raise RuntimeError("self._user_prompt is None, cannot proceed with query.")

        # Create the appropriate LLM provider
        if self.azure_endpoint and self.azure_deployment:
            # Use Azure OpenAI
            llm = AzureChatOpenAI(
                azure_endpoint=self.azure_endpoint,
                azure_deployment=self.azure_deployment,
                api_key=self.api_key,
                temperature=self.temperature,
                api_version="2024-08-01-preview",
            )
            logger.info(f"Using Azure OpenAI with deployment {self.azure_deployment}")
        else:
            # Use regular OpenAI API
            llm = ChatOpenAI(model=self.model, temperature=self.temperature, api_key=self.api_key)
            logger.info(f"Using OpenAI API with model {self.model}")

        # Create prompt template
        messages = [
            ("system", self._system_instructions),
            ("user", self._user_prompt),
        ]

        # Add transcript as assistant message only if it's not empty
        if transcript:
            messages.append(("assistant", transcript))

        prompt = ChatPromptTemplate.from_messages(messages)

        # Create chain
        chain = prompt | llm | StrOutputParser()

        # Execute chain
        start_time = __import__("time").time()
        response = chain.invoke({})
        elapsed_time = __import__("time").time() - start_time

        # Log time taken
        logger.info(f"GPT query took {elapsed_time:.2f} seconds")

        return response.strip()
