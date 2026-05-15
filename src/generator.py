from openai import OpenAI

from src.config import Settings


class Generator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = OpenAI(
            api_key=settings.api_key or "no-key-required",
            base_url=settings.base_url,
        )

    def generate(
        self,
        prompt: str | None = None,
        system_prompt: str | None = None,
        messages: list | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        if messages is not None:
            final_messages = messages
        else:
            final_messages = []
            if system_prompt:
                final_messages.append({"role": "system", "content": system_prompt})
            if prompt:
                final_messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.settings.model,
            messages=final_messages,
            temperature=temperature or self.settings.temperature,
            max_tokens=max_tokens or self.settings.max_tokens,
        )

        content = response.choices[0].message.content
        if content is None:
            return ""
        return content.strip()
