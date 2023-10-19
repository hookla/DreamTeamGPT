from gpt.gpt_client import GPTClient



class Agent:
    def __init__(self, name: str):
        self.name = name
        self.common_instructions = "For the duration of this conversation, provide raw, concise opinions without any politeness or filler words. Focus on progressing the solution in a tangible way. Avoid generic statements and repetition of points already made. Ensure all comments are directly relevant to the conversation. If you cannot meet these criteria, respond with 'no comment.'"
        self.gpt_client = GPTClient(self.common_instructions)

    def query_gpt(self, prompt: str, max_tokens: int) -> str:
        final_prompt = f"{self.common_instructions} {prompt}"
        return self.gpt_client.query(final_prompt, max_tokens)
