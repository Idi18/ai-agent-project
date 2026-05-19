"""time_tool.py – Returns the current date and time."""

import datetime
from base_tool import BaseTool


class TimeTool(BaseTool):

    @property
    def name(self) -> str:
        return "get_current_time"

    @property
    def description(self) -> str:
        return "Returns the current date and time for a given UTC timezone offset."

    def execute(self, timezone_offset: int = 0) -> str:
        try:
            tz = datetime.timezone(datetime.timedelta(hours=int(timezone_offset)))
            now = datetime.datetime.now(tz)
            return f"Current date and time: {now.strftime('%A, %d %B %Y – %H:%M:%S')} (UTC{timezone_offset:+d})"
        except Exception as exc:
            return f"Time error: {exc}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone_offset": {
                        "type": "integer",
                        "description": "UTC offset in hours. Default 0.",
                    }
                },
                "required": [],
            },
        }