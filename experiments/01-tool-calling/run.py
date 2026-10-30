"""Experiment 01: an agent that answers questions using a calculator and a web-search stub."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from common.ollama_client import chat, model_name  # noqa: E402
from common.tools import TOOL_SCHEMAS, run_tool  # noqa: E402

MAX_ROUNDS = 5
SYSTEM = (
    "You have tools. For any arithmetic you must call calculator. For any question about facts you "
    "must call web_search. Never answer from memory before calling a tool. After a tool returns, "
    "answer in one or two sentences using its output."
)
QUESTIONS = [
    "What is 1234 * 5678 + 91?",
    "Search the web for what Ollama does, then tell me the port number it uses.",
]


def run_agent(question: str) -> tuple[str, list[tuple[str, dict, str]]]:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    calls: list[tuple[str, dict, str]] = []
    for _ in range(MAX_ROUNDS):
        reply = chat(messages, tools=TOOL_SCHEMAS)
        messages.append(reply)
        if not reply.tool_calls:
            return reply.content.strip(), calls
        for call in reply.tool_calls:
            name, arguments = call.function.name, dict(call.function.arguments)
            output = run_tool(name, arguments)
            calls.append((name, arguments, output))
            messages.append({"role": "tool", "name": name, "content": output})
    return "(stopped: too many tool rounds)", calls


def main() -> None:
    print(f"model: {model_name()}")
    for question in QUESTIONS:
        print(f"\nQ: {question}")
        answer, calls = run_agent(question)
        for name, arguments, output in calls:
            print(f"  tool {name}({arguments}) -> {output}")
        print(f"A: {answer}")


if __name__ == "__main__":
    main()
