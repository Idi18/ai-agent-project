# Project Journal – Adaptive AI Personal Assistant
**Course:** DIP392 – Lietisko datorsistemu programmatура
**Student:** Mesdi Idi Amzati
**RTU, 2025/2026**

---

## Step 1 – System Plan (24.04)

### System Goal
The goal of this project is to build an interactive command-line AI personal assistant
that uses the Google Gemini API as its reasoning engine. The assistant understands user
requests in natural language, maintains conversation history, and autonomously decides
when to call external tools to answer correctly.

### AI / Agent-Based Approach
The system implements a single intelligent agent following the ReAct pattern
(Reason → Act → Observe). The agent receives a user message, reasons about whether
a tool is needed, calls the appropriate tool, observes the result, and continues
reasoning until a final answer is produced.

### Planned Tools
- calculator : Evaluate mathematical expressions
- get_current_time : Return current date and time with timezone
- unit_converter (custom) : Convert between length, weight, and temperature units
- text_analyzer (custom) : Analyze text statistics (word count, reading time)

### Preliminary Programming Concepts Required
- Object-Oriented Programming (abstract classes, inheritance, polymorphism)
- Strategy, Factory/Registry, Observer design patterns
- SOLID principles (SRP, OCP, DIP)
- Google Gemini API – function calling
- Python type hints and exception handling

---

## Step 2 – Implementation Progress (08.05)

### Updated System Description
The system has been implemented as a flat Python module structure with clear separation
between the Agent, MemoryManager, ToolRegistry, Observer, and individual Tool classes.
The CLI interface (main.py) acts as the Composition Root, wiring all components together.

### Programming Concepts Actually Used
- Abstract Base Class (ABC) : BaseTool enforces the tool interface contract
- Strategy Pattern : Each BaseTool subclass is an interchangeable strategy
- Factory/Registry Pattern : ToolRegistry maps tool names to instances dynamically
- Observer Pattern : EventBus + ConsoleLogger log all agent events without coupling
- Dependency Inversion : Agent receives ToolRegistry, MemoryManager, EventBus via constructor
- Single Responsibility : Each class has one clear purpose
- Exception handling : All tool execute() methods wrap logic in try/except
- Type hints : All function signatures annotated throughout

### Tool Integration
Tools are registered in main.py using ToolRegistry.register(). The registry passes all
tool JSON schemas to the Gemini model at initialization. When Gemini decides to call a
tool, it returns a function_call in its response. The Agent extracts this, dispatches
via ToolRegistry.execute(), and sends the result back to the model as a function_response.

---

## Step 3 – Testing and Deployment (15.05)

### Testing Process
Tests are written using pytest in test_tools.py. Each tool was tested before being
integrated into the registry.

### Test Scenarios
- calculator: simple addition 2+2 → Result: 4 ✅
- calculator: sqrt(144) → contains 12 ✅
- calculator: invalid expression → contains error ✅
- unit_converter: km to m → contains 1000 ✅
- unit_converter: 0 celsius to fahrenheit → contains 32 ✅
- unit_converter: unsupported conversion → contains not supported ✅
- text_analyzer: word count → contains 6 ✅
- text_analyzer: empty text → contains no text ✅
- registry: unknown tool → contains unknown tool ✅
- memory: add and clear → count == 0 ✅

### Deployment Preparation
pip install -r requirements.txt
set GEMINI_API_KEY=your_key
python main.py

No database, no server required. Only dependency is the Gemini API key.

### Data Conversion
All tool inputs and outputs use plain Python strings. The Gemini API sends tool
arguments as a dict which is unpacked into each tool's execute() method.

---

## Final Submission – 22.05

### Final System Description
The Adaptive AI Personal Assistant is a fully functional command-line application
combining the Google Gemini LLM with a structured tool-use architecture. It supports
multi-turn conversations, autonomous tool selection, and robust error handling.

### Final Tool Descriptions
- Calculator: Safely evaluates math expressions using Python's math module
- Time Tool: Uses Python's datetime module with timezone-aware output
- Unit Converter (custom): Covers length, weight, and temperature conversions
- Text Analyzer (custom): Word count, sentence detection, reading time estimation

### Final Testing Results
All tests pass. Error handling validated for: invalid expressions, unsupported unit
pairs, empty inputs, unknown tool names, and bad argument types.

### Final Deployment Description
The system runs locally as a CLI tool. The user sets GEMINI_API_KEY and runs main.py.
No external infrastructure needed.

### Deployment Strategy
1. Local (current): developer use only
2. Internal beta: packaged as CLI tool distributed within a team
3. Web service: wrapped in FastAPI REST API, containerized with Docker
4. Production: add authentication, rate limiting, and monitoring
