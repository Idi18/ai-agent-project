"""memory.py – Manages conversation history (SRP)."""


class MemoryManager:
    """Stores and retrieves multi-turn conversation history for a session."""

    def __init__(self) -> None:
        self._history: list[dict] = []

    def add_user_message(self, content: str) -> None:
        self._history.append({"role": "user", "parts": [{"text": content}]})

    def add_model_message(self, content: str) -> None:
        self._history.append({"role": "model", "parts": [{"text": content}]})

    def get_history(self) -> list[dict]:
        return list(self._history)

    def clear(self) -> None:
        self._history.clear()

    def turn_count(self) -> int:
        return len(self._history)