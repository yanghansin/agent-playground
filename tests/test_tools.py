import importlib.util
from pathlib import Path

import pytest

from common.tools import calculator, run_tool, web_search_stub


def load_research_agent():
    path = Path(__file__).resolve().parents[1] / "experiments/02-research-agent/run.py"
    spec = importlib.util.spec_from_file_location("research_agent", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("expression", "expected"),
    [("1 + 2", "3"), ("12 * (3 + 4)", "84"), ("2 ** 10", "1024"), ("-3 + 1", "-2"), ("7 / 2", "3.5")],
)
def test_calculator(expression, expected):
    assert calculator(expression) == expected


@pytest.mark.parametrize("expression", ["1 / 0", "__import__('os')", "open('x')", "2 ** 1000", "1 +", "True + 1"])
def test_calculator_rejects_bad_input(expression):
    assert calculator(expression).startswith("error:")


def test_search_stub_is_labeled():
    assert web_search_stub("what does Ollama do").startswith("STUB RESULT")
    assert web_search_stub("unknown topic") == "STUB RESULT: no results for this query."


def test_run_tool_reports_errors_as_text():
    assert run_tool("calculator", {"expression": "2 + 2"}) == "4"
    assert run_tool("nope", {}).startswith("error:")
    assert run_tool("calculator", {"wrong": "2"}).startswith("error:")


def test_parse_plan_filters_bad_steps():
    agent = load_research_agent()
    text = '{"steps": [{"tool": "web_search", "input": "x"}, {"tool": "rm", "input": "y"}, {"tool": "calculator"}]}'
    assert agent.parse_plan(text) == [{"tool": "web_search", "input": "x"}]
    assert agent.parse_plan("not json") == []
    assert agent.parse_plan("[]") == []
