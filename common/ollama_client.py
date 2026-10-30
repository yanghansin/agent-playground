"""Shared Ollama client settings for the experiments."""

import os

import ollama

DEFAULT_MODEL = "mistral"


def model_name() -> str:
    return os.getenv("PLAYGROUND_MODEL", DEFAULT_MODEL)


def chat(messages: list[dict], tools: list[dict] | None = None, json_schema: dict | None = None):
    """Send one chat request and return the reply message."""
    response = ollama.chat(
        model=model_name(),
        messages=messages,
        tools=tools,
        format=json_schema,
        options={"temperature": 0.1},
    )
    return response.message
