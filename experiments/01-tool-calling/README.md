# 01: Tool-calling agent

## Goal

See whether a small local model can use tools correctly through Ollama's native tool calling.

## Approach

The agent loops through chat requests with two tools: a calculator, and a web-search stub that returns canned text. It runs each tool call the model makes and feeds back the output until the model answers, for at most 5 rounds.

```bash
python experiments/01-tool-calling/run.py
```

## Result

Tested with `mistral` on 2026-10-30, on two questions.

The system prompt made all the difference:

| System prompt | Tool calls | Answer to 1234 * 5678 + 91 (correct: 7,006,743) |
| --- | --- | --- |
| "Use the provided tools when they help." | None | Wrong: 7,430,829 in the full run and 740,682 in a probe |
| "For any arithmetic you must call calculator..." | Used on both questions | Correct in both runs |

Output from a run with the strict prompt:

```text
Q: What is 1234 * 5678 + 91?
  tool calculator({'expression': '1234 * 5678 + 91'}) -> 7006743
A: The result of the multiplication and addition is 7,006,743.

Q: Search the web for what Ollama does, then tell me the port number it uses.
  tool web_search({'query': 'What does Ollama do'}) -> STUB RESULT: Ollama runs LLMs locally and exposes an HTTP API on port 11434.
  tool web_search({'query': 'What is the port number used by Ollama'}) -> STUB RESULT: Ollama runs LLMs locally and exposes an HTTP API on port 11434.
A: According to the search results, Ollama runs Language Models (LLMs) locally and exposes an HTTP API on port 11434.
```

With the soft prompt, the model also claimed "After searching the web" without having searched. That is a small sample, but it shows why a tool call needs checking in the trace, not just in the answer text.
