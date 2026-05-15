"""CLI entry point for the RAG system.

Usage:
    python -m src.cli ask "What is machine learning?"
    python -m src.cli ask --model meta/llama-3.1-405b-instruct "Explain RAG" --system "You are a teacher"
"""

import click

from src.chat import ChatSession
from src.config import get_settings
from src.generator import Generator


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("prompt")
@click.option("--system", "-s", default=None, help="System prompt")
@click.option("--model", "-m", default=None, help="Override the default model")
@click.option(
    "--temperature", "-t", default=None, type=float, help="Sampling temperature"
)
@click.option(
    "--max-tokens", default=None, type=int, help="Maximum response tokens"
)
def ask(
    prompt: str,
    system: str | None,
    model: str | None,
    temperature: float | None,
    max_tokens: int | None,
) -> None:
    settings = get_settings()

    if model:
        settings.model = model

    generator = Generator(settings)
    response = generator.generate(
        prompt=prompt,
        system_prompt=system,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    click.echo()
    click.echo(response)
    click.echo()


@cli.command()
@click.option("--system", "-s", default=None, help="System prompt")
@click.option("--model", "-m", default=None, help="Override the default model")
def chat(system: str | None, model: str | None) -> None:
    settings = get_settings()
    if model:
        settings.model = model

    generator = Generator(settings)
    session = ChatSession(generator, system_prompt=system)

    click.echo("Chat started. Commands: /exit  /clear")
    click.echo()

    while True:
        user_input = click.prompt("You", prompt_suffix="> ")

        if user_input == "/exit":
            click.echo("Goodbye.")
            break
        elif user_input == "/clear":
            session.clear()
            click.echo("History cleared.")
            click.echo()
            continue

        response = session.chat(user_input)
        click.echo(f"Bot> {response}")
        click.echo()


if __name__ == "__main__":
    cli()
