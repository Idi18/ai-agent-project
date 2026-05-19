"""observer.py – Observer pattern for decoupled event logging."""

import datetime
from abc import ABC, abstractmethod


class AgentObserver(ABC):
    @abstractmethod
    def on_event(self, event_type: str, data: dict) -> None:
        pass


class ConsoleLogger(AgentObserver):
    def on_event(self, event_type: str, data: dict) -> None:
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"  [{ts}] [{event_type}] {data}")


class EventBus:
    def __init__(self) -> None:
        self._observers: list[AgentObserver] = []

    def subscribe(self, observer: AgentObserver) -> None:
        self._observers.append(observer)

    def publish(self, event_type: str, data: dict) -> None:
        for obs in self._observers:
            obs.on_event(event_type, data)