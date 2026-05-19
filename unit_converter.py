"""unit_converter.py – Custom Tool 1: converts values between units."""

from base_tool import BaseTool


class UnitConverterTool(BaseTool):

    _CONVERSIONS = {
        ("km", "m"): 1000,       ("m", "km"): 0.001,
        ("m", "cm"): 100,        ("cm", "m"): 0.01,
        ("m", "ft"): 3.28084,    ("ft", "m"): 0.3048,
        ("km", "miles"): 0.621371, ("miles", "km"): 1.60934,
        ("kg", "g"): 1000,       ("g", "kg"): 0.001,
        ("kg", "lb"): 2.20462,   ("lb", "kg"): 0.453592,
    }

    @property
    def name(self) -> str:
        return "unit_converter"

    @property
    def description(self) -> str:
        return "Converts a numeric value between units (length, weight, temperature)."

    def execute(self, value: float = 0, from_unit: str = "", to_unit: str = "") -> str:
        try:
            value = float(value)
            from_unit = from_unit.lower().strip()
            to_unit = to_unit.lower().strip()
            if from_unit in ("celsius", "fahrenheit", "kelvin"):
                return self._convert_temperature(value, from_unit, to_unit)
            key = (from_unit, to_unit)
            if key in self._CONVERSIONS:
                result = value * self._CONVERSIONS[key]
                return f"{value} {from_unit} = {round(result, 6)} {to_unit}"
            return f"Conversion '{from_unit}' to '{to_unit}' is not supported."
        except Exception as exc:
            return f"Unit converter error: {exc}"

    def _convert_temperature(self, value, from_unit, to_unit):
        if from_unit == to_unit:
            return f"{value} {from_unit}"
        if from_unit == "celsius":
            result = (value * 9/5 + 32) if to_unit == "fahrenheit" else (value + 273.15)
        elif from_unit == "fahrenheit":
            result = (value - 32) * 5/9 if to_unit == "celsius" else ((value - 32) * 5/9 + 273.15)
        else:
            result = (value - 273.15) if to_unit == "celsius" else ((value - 273.15) * 9/5 + 32)
        return f"{value} {from_unit} = {round(result, 2)} {to_unit}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "value":     {"type": "number", "description": "Value to convert."},
                    "from_unit": {"type": "string", "description": "Source unit."},
                    "to_unit":   {"type": "string", "description": "Target unit."},
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        }