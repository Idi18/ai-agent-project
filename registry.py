"""registry.py – Factory/Registry pattern for tool management."""

from base_tool import BaseTool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        self._tools[tool.name] = tool

    def execute(self, tool_name: str, arguments: dict) -> str:
        tool = self._tools.get(tool_name)
        if tool is None:
            return f"Error: unknown tool '{tool_name}'."
        try:
            return tool.execute(**arguments)
        except TypeError as exc:
            return f"Error calling '{tool_name}': invalid arguments – {exc}"

    def get_declarations(self) -> list[dict]:
        return [t.get_declaration() for t in self._tools.values()]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())