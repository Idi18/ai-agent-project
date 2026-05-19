"""base_tool.py – Abstract interface for all tools."""

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> str:
        pass

    @abstractmethod
    def get_declaration(self) -> dict:
        pass
