from src.config import Settings
from src.generator import Generator


class ChatSession:
    def __init__(
        self, generator: Generator, system_prompt: str | None = None
    ) -> None:
        self.generator = generator
        self.messages: list = []
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        response = self.generator.generate(messages=self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response

    def clear(self) -> None:
        system_prompts = [m for m in self.messages if m["role"] == "system"]
        self.messages = system_prompts
