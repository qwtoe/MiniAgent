# MiniAgent

A minimal command-line Agent built with [smolagents](https://github.com/huggingface/smolagents). Supports any LLM provider with an OpenAI-compatible API.

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.example .env
# Edit .env with your LLM provider details
```

### LLM Configuration

MiniAgent uses OpenAI-compatible APIs by default. Configure your provider in `.env`:

**OpenAI:**
```
LLM_API_KEY=sk-your-openai-key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini
```

**DeepSeek:**
```
LLM_API_KEY=sk-your-deepseek-key
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat
```

**Other providers** (Moonshot, Zhipu, local Ollama, etc.): just set the corresponding `BASE_URL` and `MODEL`.

## Usage

```bash
source venv/bin/activate
python agent.py
```

## Tools

- `read_file(path)` — Read file contents
- `write_file(path, content)` — Write content to file (system paths blocked)
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
│   ├── file_tool.py      # File read/write with path guard
│   ├── shell_tool.py     # Command execution with safety guard
│   └── search_tool.py    # Web search
├── .env                  # API keys (gitignored)
├── .env.example          # Environment template
└── requirements.txt      # Dependencies
```
