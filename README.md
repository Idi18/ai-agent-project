# Adaptive AI Personal Assistant
**RTU DIP392 – Practical Task: System Implementation, Testing, and Deployment**

A command-line AI agent built with the Google Gemini API. The system follows established
Software Engineering design patterns (Strategy, Factory/Registry, Observer) and SOLID principles.

## Features
- Natural language conversation with contextual memory
- Autonomous tool selection (ReAct loop: Reason → Act → Observe)
- 4 built-in tools: Calculator, Time, Unit Converter, Text Analyzer
- Graceful error handling for API failures and invalid tool calls

## Project Structure
- main.py – CLI entry point
- agent.py – Core Agent, ReAct orchestrator
- memory.py – Conversation history
- registry.py – Tool Factory/Registry
- observer.py – Event logging
- base_tool.py – Abstract tool interface
- calculator.py – Math expression evaluator
- time_tool.py – Current date/time
- unit_converter.py – Unit conversion (custom tool 1)
- text_analyzer.py – Text statistics (custom tool 2)
- test_tools.py – Test suite

## Quick Start

### 1. Install dependencies
pip install -r requirements.txt

### 2. Set your Gemini API key
Get a free key at https://aistudio.google.com/

Windows:
set GEMINI_API_KEY=your_key_here

### 3. Run the assistant
python main.py

## Available Tools
- calculator : Evaluates math expressions
- get_current_time : Returns date/time for a UTC timezone
- unit_converter : Converts length, weight, temperature
- text_analyzer : Word count, sentences, reading time

## Example Session
You: What is 15% of 3200?
Assistant: 15% of 3200 is 480.

You: Convert 100 km to miles
Assistant: 100 km = 62.1371 miles.

You: What time is it in Riga? (UTC+3)
Assistant: Current date and time: Tuesday, 20 May 2025 - 14:32:11 (UTC+3)

## Running Tests
pytest test_tools.py -v

## Design Patterns
- Strategy : BaseTool + concrete tools
- Factory/Registry : ToolRegistry
- Observer : EventBus + ConsoleLogger
- ReAct : Agent._react_loop()

## Deployment Strategy
Local CLI tool. Can be extended as a REST API with FastAPI or deployed as a web chatbot.
