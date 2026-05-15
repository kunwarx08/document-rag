from unittest.mock import patch

from src.chat import ChatSession
from src.config import Settings
from src.generator import Generator


def test_session_builds_message_history():
    settings = Settings(api_key="test-key")
    gen = Generator(settings)
    session = ChatSession(gen, system_prompt="Be helpful")

    assert len(session.messages) == 1
    assert session.messages[0] == {"role": "system", "content": "Be helpful"}


def test_chat_appends_user_and_assistant():
    settings = Settings(api_key="test-key")
    gen = Generator(settings)
    session = ChatSession(gen)

    with patch.object(gen, "generate", return_value="I am fine."):
        response = session.chat("How are you?")

    assert response == "I am fine."
    assert len(session.messages) == 2
    assert session.messages[0] == {"role": "user", "content": "How are you?"}
    assert session.messages[1] == {"role": "assistant", "content": "I am fine."}


def test_chat_passes_full_history():
    settings = Settings(api_key="test-key")
    gen = Generator(settings)
    session = ChatSession(gen)

    with patch.object(gen, "generate", return_value="First reply"):
        session.chat("First message")

    with patch.object(gen, "generate", return_value="Second reply"):
        session.chat("Second message")

    assert len(session.messages) == 4
    assert session.messages == [
        {"role": "user", "content": "First message"},
        {"role": "assistant", "content": "First reply"},
        {"role": "user", "content": "Second message"},
        {"role": "assistant", "content": "Second reply"},
    ]


def test_clear_keeps_system_prompt():
    settings = Settings(api_key="test-key")
    gen = Generator(settings)
    session = ChatSession(gen, system_prompt="You are a bot")

    with patch.object(gen, "generate", return_value="OK"):
        session.chat("Hi")
        session.chat("Again")

    assert len(session.messages) == 5

    session.clear()

    assert len(session.messages) == 1
    assert session.messages[0] == {"role": "system", "content": "You are a bot"}
