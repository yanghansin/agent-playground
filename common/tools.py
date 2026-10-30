"""Tools the experiments give to their agents."""

import ast
import operator

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
MAX_EXPONENT = 100


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left, right = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > MAX_EXPONENT:
            raise ValueError("exponent too large")
        return _OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("only numbers and + - * / % ** are allowed")


def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression without using eval()."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as exc:
        return f"error: {exc}"


# Canned, made-up snippets. The stub keeps experiments offline and repeatable.
_STUB_RESULTS = {
    "ollama": "STUB RESULT: Ollama runs LLMs locally and exposes an HTTP API on port 11434.",
    "rabbitmq": "STUB RESULT: RabbitMQ is a message broker that queues messages between services.",
    "react": "STUB RESULT: ReAct agents alternate between reasoning steps and tool actions.",
    "guardrail": "STUB RESULT: Guardrails validate model output before it is allowed to take effect.",
}


def web_search_stub(query: str) -> str:
    """Pretend to search the web. Returns canned text and never touches the network."""
    query = query.lower()
    hits = [text for key, text in _STUB_RESULTS.items() if key in query]
    return "\n".join(hits) if hits else "STUB RESULT: no results for this query."


TOOL_FUNCTIONS = {"calculator": calculator, "web_search": web_search_stub}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Evaluate an arithmetic expression, such as 12 * (3 + 4).",
            "parameters": {
                "type": "object",
                "properties": {"expression": {"type": "string"}},
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web and return short text snippets.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
]


def run_tool(name: str, arguments: dict) -> str:
    """Run a tool the model asked for. Bad names and arguments become error text it can read."""
    function = TOOL_FUNCTIONS.get(name)
    if function is None:
        return f"error: unknown tool {name}"
    try:
        return function(**arguments)
    except TypeError as exc:
        return f"error: {exc}"
