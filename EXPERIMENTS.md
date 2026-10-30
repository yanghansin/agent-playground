# Experiments

| Date | Experiment | Outcome |
| --- | --- | --- |
| 2026-10-30 | [01-tool-calling](experiments/01-tool-calling/README.md) | `mistral` skipped its tools under a soft system prompt and got the math wrong. With a strict prompt it called them and answered correctly in both runs. |
| 2026-10-30 | [02-research-agent](experiments/02-research-agent/README.md) | The plan, tool calls, and summary ran end to end, but all 4 planned steps were near-identical searches. |
