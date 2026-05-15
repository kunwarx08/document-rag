from unittest.mock import patch

from src.config import Settings
from src.generator import Generator


def test_defaults_to_ollama():
    settings = Settings()
    assert "localhost:11434" in settings.base_url
    assert settings.model == "llama3.2"


def test_generator_initializes_with_settings():
    settings = Settings(api_key="test-key")
    gen = Generator(settings)
    assert str(gen.client.base_url) == "http://localhost:11434/v1/"
    assert gen.settings.model == "llama3.2"


def test_generate_formats_messages_correctly():
    settings = Settings(api_key="test-key")

    with patch.object(settings, "model", "test-model"):
        gen = Generator(settings)
        with patch.object(gen.client.chat.completions, "create") as mock_create:
            mock_create.return_value.choices = [
                type("obj", (object,), {"message": type("msg", (object,), {"content": "Hello!"})})()
            ]

            result = gen.generate("Hi there", system_prompt="Be friendly")
            assert result == "Hello!"

            call_kwargs = mock_create.call_args[1]
            assert call_kwargs["model"] == "test-model"
            assert call_kwargs["messages"] == [
                {"role": "system", "content": "Be friendly"},
                {"role": "user", "content": "Hi there"},
            ]


def test_generate_handles_null_content():
    settings = Settings(api_key="test-key")
    gen = Generator(settings)

    with patch.object(gen.client.chat.completions, "create") as mock_create:
        mock_create.return_value.choices = [
            type("obj", (object,), {"message": type("msg", (object,), {"content": None})})()
        ]

        result = gen.generate("test")
        assert result == ""
