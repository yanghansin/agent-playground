"""Experiment 02: an agent that plans, calls tools for each step, and writes a summary."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from common.ollama_client import chat, model_name  # noqa: E402
from common.tools import TOOL_FUNCTIONS, run_tool  # noqa: E402

TOPIC = "How do guardrails and ReAct loops make local LLM agents more reliable?"
MAX_STEPS = 4
PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tool": {"type": "string", "enum": list(TOOL_FUNCTIONS)},
                    "input": {"type": "string"},
                },
                "required": ["tool", "input"],
            },
        }
    },
    "required": ["steps"],
}
INPUT_NAMES = {"calculator": "expression", "web_search": "query"}


def parse_plan(text: str) -> list[dict]:
    """Keep only well-formed steps with known tools, up to MAX_STEPS."""
    try:
        steps = json.loads(text).get("steps", [])
    except (json.JSONDecodeError, AttributeError):
        return []
    return [
        step
        for step in steps
        if isinstance(step, dict) and step.get("tool") in TOOL_FUNCTIONS and isinstance(step.get("input"), str)
    ][:MAX_STEPS]


def make_plan(topic: str) -> list[dict]:
    prompt = (
        f"Research topic: {topic}\n"
        f"Plan 2 to {MAX_STEPS} tool calls that gather the facts you need. "
        "web_search takes a short query. calculator takes an arithmetic expression. "
        'Reply as JSON: {"steps": [{"tool": "web_search", "input": "..."}]}'
    )
    return parse_plan(chat([{"role": "user", "content": prompt}], json_schema=PLAN_SCHEMA).content)


def summarize(topic: str, notes: list[str]) -> str:
    prompt = (
        f"Research topic: {topic}\n\nNotes:\n" + "\n".join(notes) + "\n\n"
        "Write a three-sentence summary using only these notes. "
        "If the notes don't cover something, say so instead of guessing."
    )
    return chat([{"role": "user", "content": prompt}]).content.strip()


def main() -> None:
    print(f"model: {model_name()}\ntopic: {TOPIC}\n")
    plan = make_plan(TOPIC)
    print(f"plan ({len(plan)} steps):")
    notes = []
    for step in plan:
        output = run_tool(step["tool"], {INPUT_NAMES[step["tool"]]: step["input"]})
        print(f"  {step['tool']}({step['input']!r}) -> {output}")
        notes.append(output)
    print(f"\nsummary:\n{summarize(TOPIC, notes)}")


if __name__ == "__main__":
    main()
