"""agent.py – Orchestrates the ReAct loop (Reason -> Act -> Observe)."""

import os
from google import genai
from google.genai import types

from registry import ToolRegistry
from memory import MemoryManager
from observer import EventBus

SYSTEM_PROMPT = """You are a helpful personal assistant with access to several tools.
When you need to calculate something, get the current time, convert units, or analyse text,
you MUST use the appropriate tool. Do not guess numeric results.
Be concise, friendly, and professional.
"""


class Agent:

    def __init__(self, registry: ToolRegistry, memory: MemoryManager, event_bus: EventBus, model_name: str = "gemini-2.0-flash") -> None:
        self._registry = registry
        self._memory = memory
        self._bus = event_bus
        self._model_name = model_name

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError("GEMINI_API_KEY is not set. Run: set GEMINI_API_KEY=your_key")

        self._client = genai.Client(api_key=api_key)
        declarations = self._registry.get_declarations()
        gemini_tools = [types.Tool(function_declarations=declarations)] if declarations else []
        self._config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=gemini_tools,
        )

    def chat(self, user_input: str) -> str:
        self._memory.add_user_message(user_input)
        self._bus.publish("USER_INPUT", {"message": user_input})
        contents = self._memory.get_history()
        try:
            response = self._client.models.generate_content(
                model=self._model_name,
                contents=contents,
                config=self._config,
            )
        except Exception as exc:
            self._bus.publish("API_ERROR", {"error": str(exc)})
            return f"API error: {exc}"
        final_text = self._react_loop(contents, response)
        self._memory.add_model_message(final_text)
        self._bus.publish("AGENT_RESPONSE", {"message": final_text})
        return final_text

    def _react_loop(self, contents: list, response) -> str:
        for _ in range(10):
            tool_calls = self._extract_tool_calls(response)
            if not tool_calls:
                return self._extract_text(response)
            fn_responses = []
            for call in tool_calls:
                name, args = call["name"], call["args"]
                self._bus.publish("TOOL_CALL", {"tool": name, "args": args})
                result = self._registry.execute(name, args)
                self._bus.publish("TOOL_RESULT", {"tool": name, "result": result})
                fn_responses.append(
                    types.Part.from_function_response(name=name, response={"result": result})
                )
            contents = list(contents) + [
                types.Content(role="model", parts=response.candidates[0].content.parts),
                types.Content(role="user", parts=fn_responses),
            ]
            try:
                response = self._client.models.generate_content(
                    model=self._model_name,
                    contents=contents,
                    config=self._config,
                )
            except Exception as exc:
                return f"Error after tool execution: {exc}"
        return "Maximum reasoning steps reached."

    @staticmethod
    def _extract_tool_calls(response) -> list[dict]:
        calls = []
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.function_call:
                    calls.append({
                        "name": part.function_call.name,
                        "args": dict(part.function_call.args or {}),
                    })
        return calls

    @staticmethod
    def _extract_text(response) -> str:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if part.text:
                    return part.text.strip()
        return "(No response generated)"