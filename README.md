# MiniAgent

A minimal command-line Agent built with [smolagents](https://github.com/huggingface/smolagents). Supports multiple LLM providers via OpenAI-compatible API.

## Setup

```bash
# If using conda:
conda activate my-first-agent
# If using venv:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DEEPSEEK_API_KEY
```

## Usage

```bash
python agent.py
```

## Learning Path

1. **Step 1**: Basic chat (understand Agent loop)
2. **Step 2**: File I/O tools (understand Function Calling)
3. **Step 3**: Shell command tool (understand safety boundaries)
4. **Step 4**: Web search tool (understand tool chaining)
