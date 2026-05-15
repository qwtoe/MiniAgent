# My First Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a command-line Agent using smolagents and DeepSeek API, with incremental tool capabilities (chat, file I/O, shell commands, web search).

**Architecture:** A minimal Python CLI app using smolagents' CodeAgent with OpenAIServerModel for DeepSeek. Tools are implemented as decorated Python functions and registered incrementally. Each step is a self-contained milestone with its own commit.

**Tech Stack:** Python 3.10+, smolagents, python-dotenv, duckduckgo-search

**Repository:** `my-first-agent-cli`
**Conda Environment:** `my-first-agent`

---

## File Structure

```
my-first-agent-cli/
├── agent.py              # Main entry: CLI loop, agent initialization
├── tools/
│   ├── __init__.py       # Exports all tools
│   ├── file_tool.py      # Step 2: read_file, write_file
│   ├── shell_tool.py     # Step 3: run_command with safety guard
│   └── search_tool.py    # Step 4: web_search (DuckDuckGo wrapper)
├── config.py             # Centralized config: API keys, model params
├── .env                  # Environment secrets (gitignored)
├── .env.example          # Template for .env
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignore .env, __pycache__, etc.
└── README.md             # Project description and usage
```

---

## Task 0: Project Bootstrap

**Goal:** Initialize git repo, conda env, and project skeleton.

**Files:**
- Create: `.gitignore`, `README.md`, `requirements.txt`, `.env.example`
- Create: `config.py`, `tools/__init__.py`
- Modify: none

- [ ] **Step 1: Initialize git repository**

```bash
cd /home/usin/myagent
git init
git checkout -b main
```

Expected: Initialized empty Git repository.

- [ ] **Step 2: Create conda environment**

```bash
conda create -n my-first-agent python=3.11 -y
conda activate my-first-agent
```

Expected: Environment created and activated.

- [ ] **Step 3: Create project files**

Create `.gitignore`:
```
.env
__pycache__/
*.pyc
.conda/
```

Create `.env.example`:
```
DEEPSEEK_API_KEY=your-api-key-here
```

Create `requirements.txt`:
```
smolagents>=1.0.0
python-dotenv>=1.0.0
duckduckgo-search>=5.0.0
```

Create `config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
MODEL_ID = "deepseek-chat"
API_BASE = "https://api.deepseek.com/v1"
TEMPERATURE = 0.7
MAX_STEPS = 10
```

Create `tools/__init__.py`:
```python
# Tools will be imported here incrementally
```

Create `README.md`:
```markdown
# My First Agent CLI

A minimal command-line Agent built with [smolagents](https://github.com/huggingface/smolagents) and DeepSeek API.

## Setup

```bash
conda activate my-first-agent
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your DEEPSEEK_API_KEY
```

## Usage

```bash
python agent.py
```

## Learning Path

1. Step 1: Basic chat (understand Agent loop)
2. Step 2: File I/O tools (understand Function Calling)
3. Step 3: Shell command tool (understand safety boundaries)
4. Step 4: Web search tool (understand tool chaining)
```

- [ ] **Step 4: Install dependencies**

```bash
conda activate my-first-agent
pip install -r requirements.txt
```

- [ ] **Step 5: Commit bootstrap**

```bash
git add .
git commit -m "chore: bootstrap project with conda env and deps"
```

---

## Task 1: Step 1 - Basic Chat

**Goal:** Create a working CLI that can chat with DeepSeek via smolagents.

**Files:**
- Create: `agent.py`
- Modify: none

- [ ] **Step 1: Write agent.py**

```python
import os
from smolagents import CodeAgent, OpenAIServerModel
from config import DEEPSEEK_API_KEY, MODEL_ID, API_BASE, TEMPERATURE, MAX_STEPS


def main():
    if not DEEPSEEK_API_KEY:
        print("Error: DEEPSEEK_API_KEY not found. Please set it in .env")
        return

    model = OpenAIServerModel(
        model_id=MODEL_ID,
        api_base=API_BASE,
        api_key=DEEPSEEK_API_KEY,
    )

    # Step 1: No tools yet
    agent = CodeAgent(tools=[], model=model, verbosity_level=2)

    print("🤖 Agent ready! Type 'exit' or 'quit' to leave.")
    print("-" * 40)

    while True:
        try:
            user_input = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user_input.strip().lower() in ("exit", "quit"):
            print("Bye!")
            break

        if not user_input.strip():
            continue

        try:
            response = agent.run(user_input)
            print(response)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test the agent**

```bash
conda activate my-first-agent
python agent.py
```

Test inputs:
- `你好`
- `1 + 1 等于几`
- `exit`

Expected: Agent responds conversationally.

- [ ] **Step 3: Commit Step 1**

```bash
git add agent.py
git commit -m "feat(step1): basic chat with deepseek via smolagents"
```

---

## Task 2: Step 2 - File I/O Tools

**Goal:** Add read_file and write_file tools so Agent can interact with the filesystem.

**Files:**
- Create: `tools/file_tool.py`
- Modify: `tools/__init__.py`
- Modify: `agent.py`

- [ ] **Step 1: Write tools/file_tool.py**

```python
from smolagents import tool


@tool
def read_file(path: str) -> str:
    """
    Read and return the contents of a file at the given path.
    
    Args:
        path: Absolute or relative path to the file.
    
    Returns:
        The file contents as a string.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


@tool
def write_file(path: str, content: str) -> str:
    """
    Write content to a file at the given path. Overwrites if exists.
    
    Args:
        path: Absolute or relative path to the file.
        content: The content to write.
    
    Returns:
        Confirmation message.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {path}"
```

- [ ] **Step 2: Update tools/__init__.py**

```python
from .file_tool import read_file, write_file

__all__ = ["read_file", "write_file"]
```

- [ ] **Step 3: Update agent.py to register file tools**

In `agent.py`, replace:
```python
    agent = CodeAgent(tools=[], model=model, verbosity_level=2)
```
with:
```python
    from tools import read_file, write_file
    agent = CodeAgent(tools=[read_file, write_file], model=model, verbosity_level=2)
```

- [ ] **Step 4: Test file tools**

```bash
conda activate my-first-agent
python agent.py
```

Test inputs:
- `请帮我读取 /home/usin/myagent/README.md`
- `请帮我创建一个文件 /home/usin/myagent/test.txt，内容是 "Hello from Agent!"`
- `请帮我读取刚才创建的文件`

Expected: Agent calls read_file/write_file, shows Thought → Action → Observation.

- [ ] **Step 5: Commit Step 2**

```bash
git add tools/ agent.py
git commit -m "feat(step2): add file read/write tools"
```

---

## Task 3: Step 3 - Shell Command Tool

**Goal:** Add run_command tool with safety guard for dangerous commands.

**Files:**
- Create: `tools/shell_tool.py`
- Modify: `tools/__init__.py`
- Modify: `agent.py`

- [ ] **Step 1: Write tools/shell_tool.py**

```python
import subprocess
from smolagents import tool

DANGEROUS_COMMANDS = ["rm", "mv", "dd", ">", "|", "curl", "wget"]


@tool
def run_command(command: str) -> str:
    """
    Run a shell command and return its output.
    If the command contains potentially dangerous operations,
    the user will be asked for confirmation before execution.
    
    Args:
        command: The shell command to execute.
    
    Returns:
        stdout and stderr of the command.
    """
    # Safety check
    is_dangerous = any(cmd in command for cmd in DANGEROUS_COMMANDS)
    
    if is_dangerous:
        user_ok = input(f"⚠️  Potentially dangerous command: '{command}'. Run? [y/N] ")
        if user_ok.lower() != "y":
            return "Command cancelled by user."
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = []
        if result.stdout:
            output.append(f"stdout:\n{result.stdout}")
        if result.stderr:
            output.append(f"stderr:\n{result.stderr}")
        return "\n".join(output) if output else "Command executed successfully (no output)."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error: {e}"
```

- [ ] **Step 2: Update tools/__init__.py**

```python
from .file_tool import read_file, write_file
from .shell_tool import run_command

__all__ = ["read_file", "write_file", "run_command"]
```

- [ ] **Step 3: Update agent.py**

In `agent.py`, update import:
```python
    from tools import read_file, write_file, run_command
    agent = CodeAgent(tools=[read_file, write_file, run_command], model=model, verbosity_level=2)
```

- [ ] **Step 4: Test shell tool**

```bash
conda activate my-first-agent
python agent.py
```

Test inputs:
- `请帮我列出当前目录的文件`
- `请帮我运行 echo "Hello World"`
- `请帮我运行 rm -rf /` (should trigger confirmation)

Expected: Safe commands execute directly. Dangerous commands prompt for confirmation.

- [ ] **Step 5: Commit Step 3**

```bash
git add tools/ agent.py
git commit -m "feat(step3): add shell command tool with safety guard"
```

---

## Task 4: Step 4 - Web Search Tool

**Goal:** Add DuckDuckGo web search tool.

**Files:**
- Create: `tools/search_tool.py`
- Modify: `tools/__init__.py`
- Modify: `agent.py`

- [ ] **Step 1: Write tools/search_tool.py**

```python
from smolagents import tool
from duckduckgo_search import DDGS


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web using DuckDuckGo and return a summary of results.
    
    Args:
        query: The search query string.
        max_results: Maximum number of results to return (default 5).
    
    Returns:
        A formatted string of search results with titles, URLs, and snippets.
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=max_results)
            if not results:
                return "No results found."
            
            formatted = []
            for i, r in enumerate(results, 1):
                formatted.append(f"{i}. {r['title']}\n   URL: {r['href']}\n   {r['body']}\n")
            return "\n".join(formatted)
    except Exception as e:
        return f"Search error: {e}"
```

- [ ] **Step 2: Update tools/__init__.py**

```python
from .file_tool import read_file, write_file
from .shell_tool import run_command
from .search_tool import web_search

__all__ = ["read_file", "write_file", "run_command", "web_search"]
```

- [ ] **Step 3: Update agent.py**

In `agent.py`, update import:
```python
    from tools import read_file, write_file, run_command, web_search
    agent = CodeAgent(
        tools=[read_file, write_file, run_command, web_search],
        model=model,
        verbosity_level=2
    )
```

- [ ] **Step 4: Test search tool**

```bash
conda activate my-first-agent
python agent.py
```

Test inputs:
- `请搜索 "Python smolagents 教程"`
- `今天有什么科技新闻？`

Expected: Agent calls web_search, shows results, summarizes.

- [ ] **Step 5: Commit Step 4**

```bash
git add tools/ agent.py
git commit -m "feat(step4): add duckduckgo web search tool"
```

---

## Task 5: GitHub Remote Setup & Push

**Goal:** Create GitHub repo and push all commits.

- [ ] **Step 1: Create GitHub repository**

```bash
gh repo create my-first-agent-cli --public --source=. --remote=origin --push
```

Or if repo already exists remotely:
```bash
git remote add origin https://github.com/YOUR_USERNAME/my-first-agent-cli.git
git branch -M main
git push -u origin main
```

Expected: Repository created/updated on GitHub with all 5 commits.

- [ ] **Step 2: Verify on GitHub**

Open https://github.com/YOUR_USERNAME/my-first-agent-cli and confirm all files and commits are present.

---

## Spec Coverage Check

| Spec Requirement | Plan Task |
|------------------|-----------|
| Step 1: Basic chat | Task 1 |
| Step 2: File I/O tools | Task 2 |
| Step 3: Shell command tool | Task 3 |
| Step 4: Web search tool | Task 4 |
| Git management per step | Every task ends with commit |
| Conda environment | Task 0 Step 2 |
| GitHub push | Task 5 |
| Demo after each step | Every task ends with test step |

---

## Self-Review

- **Placeholder scan:** No TBD, TODO, or vague steps. All code is complete.
- **Type consistency:** `DEEPSEEK_API_KEY`, `MODEL_ID`, `API_BASE` used consistently across tasks.
- **Import consistency:** Tool imports updated incrementally in `tools/__init__.py` and `agent.py`.
