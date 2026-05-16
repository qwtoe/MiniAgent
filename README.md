# MiniAgent

A minimal command-line Agent built with [smolagents](https://github.com/huggingface/smolagents). Supports multiple LLM providers via OpenAI-compatible API.

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.example .env
# Edit .env with your DEEPSEEK_API_KEY
```

## Usage

```bash
source venv/bin/activate
python agent.py
```

## Tools

- `read_file(path)` — Read file contents
- `write_file(path, content)` — Write content to file
- `run_command(command)` — Execute shell commands (dangerous commands require confirmation)
- `web_search(query)` — Search the web via DuckDuckGo

## Learning Path

1. **Step 1**: Basic chat (understand Agent loop)
2. **Step 2**: File I/O tools (understand Function Calling)
3. **Step 3**: Shell command tool (understand safety boundaries)
4. **Step 4**: Web search tool (understand tool chaining)

## Architecture

```
MiniAgent/
├── agent.py              # Main CLI entry
├── config.py             # Configuration & API keys
├── tools/
│   ├── file_tool.py      # File read/write
│   ├── shell_tool.py     # Command execution with guard
│   └── search_tool.py    # Web search
├── .env                  # API keys (gitignored)
├── .env.example          # Environment template
└── requirements.txt      # Dependencies
```
