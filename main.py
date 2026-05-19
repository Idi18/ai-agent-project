"""main.py – CLI entry point for the Adaptive AI Personal Assistant."""

from agent import Agent
from memory import MemoryManager
from registry import ToolRegistry
from observer import EventBus, ConsoleLogger
from calculator import CalculatorTool
from time_tool import TimeTool
from unit_converter import UnitConverterTool
from text_analyzer import TextAnalyzerTool


def build_agent() -> Agent:
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(UnitConverterTool())
    registry.register(TextAnalyzerTool())

    memory = MemoryManager()
    bus = EventBus()
    bus.subscribe(ConsoleLogger())

    return Agent(registry=registry, memory=memory, event_bus=bus)


def main() -> None:
    print("=" * 60)
    print("  Adaptive AI Personal Assistant  -  RTU DIP392")
    print("=" * 60)
    print("Commands: 'quit' | 'clear' (reset memory) | 'tools'\n")

    try:
        agent = build_agent()
    except EnvironmentError as exc:
        print(f"[STARTUP ERROR] {exc}")
        return

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if user_input.lower() == "clear":
            agent._memory.clear()
            print("Memory cleared.")
            continue
        if user_input.lower() == "tools":
            print("Available tools:", ", ".join(agent._registry.list_tools()))
            continue

        print("\nAssistant:", end=" ", flush=True)
        print(agent.chat(user_input))


if __name__ == "__main__":
    main()