# 02: Multi-step research agent

## Goal

See whether a small local model can plan its own research, then summarize only what it found.

## Approach

The agent works in three stages:

1. **Plan.** The model returns up to 4 tool calls as JSON, constrained by a schema. Malformed steps and unknown tools are dropped.
2. **Act.** Each step runs through a tool, and the output is saved as a note.
3. **Summarize.** The model writes three sentences using only the notes.

The search tool is a stub that returns canned text labeled `STUB RESULT`.

```bash
python experiments/02-research-agent/run.py
```

## Result

Tested once with `mistral` on 2026-10-30, on the topic "How do guardrails and ReAct loops make local LLM agents more reliable?"

It ran end to end, with these results:

- **Planning was weak.** All 4 steps were `web_search` calls with long, near-identical queries that returned the same two snippets.
- **The summary mostly stayed within the notes.** It also said what the notes didn't cover, as instructed. It went slightly beyond them by adding "safety mechanism" and "preventing potential errors", which aren't in the notes.

Summary from the run:

```text
The summary is as follows: ReAct agents, which alternate between reasoning steps and tool actions, work in conjunction with guardrails to enhance the reliability of local LLM agents. Guardrails serve as a safety mechanism, validating model output before it is allowed to take effect, thereby preventing potential errors or undesirable actions. However, the notes do not provide information on how these mechanisms improve the learning or adaptability of the agents, which might be an important aspect to consider in a more comprehensive discussion.
```
