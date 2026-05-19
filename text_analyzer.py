"""text_analyzer.py – Custom Tool 2: analyzes text statistics."""

import re
from base_tool import BaseTool


class TextAnalyzerTool(BaseTool):

    @property
    def name(self) -> str:
        return "text_analyzer"

    @property
    def description(self) -> str:
        return "Analyzes a text: word count, sentences, characters, reading time."

    def execute(self, text: str = "") -> str:
        try:
            if not text.strip():
                return "No text provided for analysis."
            words = text.split()
            word_count = len(words)
            sentences = re.split(r"[.!?]+", text)
            sentence_count = len([s for s in sentences if s.strip()])
            char_count = len(text)
            avg_word_len = round(sum(len(w.strip(".,!?;:")) for w in words) / max(word_count, 1), 2)
            reading_time_sec = round(word_count / 200 * 60)
            return (
                f"Text Analysis:\n"
                f"  Words          : {word_count}\n"
                f"  Sentences      : {sentence_count}\n"
                f"  Characters     : {char_count}\n"
                f"  Avg word length: {avg_word_len} chars\n"
                f"  Reading time   : ~{reading_time_sec} seconds"
            )
        except Exception as exc:
            return f"Text analyzer error: {exc}"

    def get_declaration(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to analyze."}
                },
                "required": ["text"],
            },
        }