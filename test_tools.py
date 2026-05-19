from calculator import CalculatorTool
from time_tool import TimeTool
from unit_converter import UnitConverterTool
from text_analyzer import TextAnalyzerTool
from registry import ToolRegistry
from memory import MemoryManager


class TestCalculatorTool:

    def setup_method(self):
        self.tool = CalculatorTool()

    def test_simple_addition(self):
        result = self.tool.execute(expression="2 + 2")
        assert "4" in result

    def test_multiplication(self):
        result = self.tool.execute(expression="7 * 8")
        assert "56" in result

    def test_invalid_expression(self):
        result = self.tool.execute(expression="import os")
        assert "error" in result.lower()

    def test_empty_expression(self):
        result = self.tool.execute(expression="")
        assert "error" in result.lower()


class TestUnitConverterTool:

    def setup_method(self):
        self.tool = UnitConverterTool()

    def test_km_to_m(self):
        result = self.tool.execute(value=1, from_unit="km", to_unit="m")
        assert "1000" in result

    def test_celsius_to_fahrenheit(self):
        result = self.tool.execute(value=0, from_unit="celsius", to_unit="fahrenheit")
        assert "32" in result

    def test_unsupported_conversion(self):
        result = self.tool.execute(value=1, from_unit="parsec", to_unit="km")
        assert "not supported" in result.lower()


class TestTextAnalyzerTool:

    def setup_method(self):
        self.tool = TextAnalyzerTool()

    def test_word_count(self):
        result = self.tool.execute(text="Hello world this is a test")
        assert "6" in result

    def test_empty_text(self):
        result = self.tool.execute(text="")
        assert "no text" in result.lower()


class TestToolRegistry:

    def setup_method(self):
        self.registry = ToolRegistry()
        self.registry.register(CalculatorTool())

    def test_execute_known_tool(self):
        result = self.registry.execute("calculator", {"expression": "3 + 3"})
        assert "6" in result

    def test_execute_unknown_tool(self):
        result = self.registry.execute("nonexistent_tool", {})
        assert "unknown tool" in result.lower()


class TestMemoryManager:

    def setup_method(self):
        self.memory = MemoryManager()

    def test_add_user_message(self):
        self.memory.add_user_message("Hello")
        assert self.memory.turn_count() == 1

    def test_clear_memory(self):
        self.memory.add_user_message("Hello")
        self.memory.clear()
        assert self.memory.turn_count() == 0
