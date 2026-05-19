"""calculator.py – Evaluates safe mathematical expressions."""

import math
from base_tool import BaseTool


class CalculatorTool(BaseTool):

    @property
    def name(self) -> str:
        return "calculator"

    @property
    def description(self) -> str:
        return "Evaluates a mathematical expression and returns the numeric result."

    def execute(self, expression: str = "") -> str:
        try:
            allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
            allowed.update({"abs": abs, "round": round})
            result = eval(expression, {"__builtins__": {}}, allowed)
            return f"Result: {result}"
        except Exception as exc:
            return f"Calculator error: {exc}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate.",
                    }
                },
                "required": ["expression"],
            },
        }