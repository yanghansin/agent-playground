# agent-playground

Small, logged experiments with AI agents running on local LLMs. Each experiment has its own folder and a record of what actually happened, including what went wrong.

## Tech stack

Python 3.11+ and [Ollama](https://ollama.com/), with `ollama` as the only runtime dependency.

| Path | What it holds |
| --- | --- |
| `experiments/` | One folder per experiment, each with a README covering its goal, approach, and result |
| `common/` | Shared Ollama client and tools |
| `EXPERIMENTS.md` | Running log of every experiment |
| `tests/` | Tests for the tools and parsing, with no Ollama needed |

## How to run

Install [Ollama](https://ollama.com/download), then:

```bash
ollama pull mistral
git clone https://github.com/yanghansin/agent-playground.git
cd agent-playground
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python experiments/01-tool-calling/run.py
python experiments/02-research-agent/run.py
pytest
```

Set `PLAYGROUND_MODEL` to try a different model. It needs to support tool calling for experiment 01.

## Project status

Two starter experiments run end to end against a local model. See [EXPERIMENTS.md](EXPERIMENTS.md).

The `web_search` tool is a stub that returns canned text labeled `STUB RESULT`. It doesn't touch the network, so these experiments test agent behavior, not research quality.

## Roadmap

- Replace the search stub with a real search tool.
- Make the research agent avoid repeating near-identical searches.
- Compare results across more local models.

## License

[MIT](LICENSE)
