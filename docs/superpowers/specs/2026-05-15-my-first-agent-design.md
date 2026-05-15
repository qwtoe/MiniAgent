# My First Agent - Design Document

**Date:** 2026-05-15
**Status:** Approved
**Framework:** smolagents + DeepSeek API

---

## 1. 项目目标

构建一个基于 `smolagents` 的命令行 Agent，通过 DeepSeek API 驱动，支持对话、文件读写、命令执行、联网搜索四项能力。

核心诉求是**透明、可学习**——每一步都能看到 Agent 在想什么、为什么选这个工具、工具返回了什么。

---

## 2. 增量学习路径

| 步骤 | 能力 | 核心概念 | 预期成果 |
|------|------|----------|----------|
| **Step 1** | 基础对话 | Agent 循环、System Prompt、模型调用 | 一个能聊天的小程序 |
| **Step 2** | 文件读写工具 | Tool / Function Calling、ReAct 推理 | Agent 能读代码、写文件 |
| **Step 3** | 命令执行工具 | 安全边界、权限控制、沙箱思考 | Agent 能运行 `ls`、`git status` 等 |
| **Step 4** | 联网搜索工具 | 外部 API 集成、工具链组合 | Agent 能查文档、搜新闻 |

每步完成后可运行并观察 Agent 的完整思考链（Thought → Action → Observation）。

---

## 3. 技术栈

- **框架**：`smolagents`（HuggingFace，极简 Agent 框架）
- **模型**：DeepSeek V3 / R1（通过 OpenAI 兼容 API 调用）
- **语言**：Python 3.10+
- **依赖管理**：`pip` + `requirements.txt`

---

## 4. 项目结构

```
my-agent/
├── agent.py              # 主入口：初始化 Agent、注册工具、启动 CLI 循环
├── tools/
│   ├── __init__.py
│   ├── file_tool.py      # Step 2：文件读写（读、写、追加）
│   ├── shell_tool.py     # Step 3：命令执行（带白名单/确认机制）
│   └── search_tool.py    # Step 4：联网搜索（DuckDuckGo 或 Serper API）
├── config.py             # 配置集中管理：API key、模型名、安全开关
├── .env                  # 环境变量（API key，不提交到 git）
├── .env.example          # 环境变量模板
└── requirements.txt
```

---

## 5. 核心组件

### 5.1 agent.py（主控）

- 初始化 `CodeAgent` 或 `ToolCallingAgent`
- 注册所有工具
- 启动 REPL 风格 CLI（`>>>` 提示符，支持 `exit`/`quit`）
- 打印 Agent 的思考过程（`smolagents` 的 `verbosity_level` 可调）

### 5.2 tools/*.py（工具层）

- 每个工具是一个被 `@tool` 装饰的普通 Python 函数
- 工具签名和 docstring 会被自动转换为模型可见的 schema
- **关键学习点**：模型通过 schema 了解有哪些工具可用、每个工具的参数和用途

### 5.3 config.py（配置层）

- 从 `.env` 加载 `DEEPSEEK_API_KEY`
- 定义模型参数（`model_id`、`temperature`、`max_steps`）
- 安全开关（如 `SHELL_CONFIRM=true` 要求执行命令前确认）

---

## 6. 数据流

一次用户请求的生命周期：

```
用户输入
  ↓
agent.py 构造 prompt（包含工具描述 + 历史对话）
  ↓
调用 DeepSeek API
  ↓
模型返回：思考过程（Thought）+ 工具调用（Action）
  ↓
agent.py 解析 Action → 执行对应 tool 函数
  ↓
tool 返回结果（Observation）
  ↓
Observation 追加到 prompt，再次调用 API
  ↓
模型决定继续思考 或 输出最终答案
  ↓
打印给用户
```

**这就是 ReAct 循环：Reason（思考）→ Act（行动）→ Observe（观察）→ 循环。**

---

## 7. 四步详细设计

### Step 1：基础对话

**做什么**：创建最简 CLI，接收用户输入，调用 DeepSeek API，返回回答。

**核心代码**：
```python
from smolagents import CodeAgent, OpenAIServerModel

model = OpenAIServerModel(
    model_id="deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=os.environ["DEEPSEEK_API_KEY"]
)
agent = CodeAgent(tools=[], model=model)

while True:
    user_input = input(">>> ")
    if user_input in ("exit", "quit"):
        break
    response = agent.run(user_input)
    print(response)
```

**你会学到**：Agent 的 `run()` 如何与模型交互；System Prompt 的作用；对话历史的维护。

**验证**：问"你好"和"1+1等于几"，确认正常对话。

---

### Step 2：文件读写工具

**新增文件**：`tools/file_tool.py`

```python
from smolagents import tool

@tool
def read_file(path: str) -> str:
    """Read the contents of a file at the given path."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file at the given path."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"Successfully wrote to {path}"
```

**修改**：`agent.py` 中 `tools=[read_file, write_file]`

**你会学到**：工具 schema 如何从 docstring 生成；模型如何决定调用哪个工具；ReAct 循环的完整观察。

**验证**：让它读一个存在的文件，再让它写一个文件。

---

### Step 3：命令执行工具

**新增文件**：`tools/shell_tool.py`

```python
import subprocess
from smolagents import tool

DANGEROUS_COMMANDS = ["rm", "mv", "dd", ">"]

@tool
def run_command(command: str, confirm: bool = True) -> str:
    """
    Run a shell command and return its output.
    If the command looks dangerous and confirm=True, ask user before executing.
    """
    if any(cmd in command for cmd in DANGEROUS_COMMANDS):
        if confirm:
            user_ok = input(f"⚠️  Potentially dangerous command: '{command}'. Run? [y/N] ")
            if user_ok.lower() != "y":
                return "Command cancelled by user."
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    return f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
```

**你会学到**：Agent 的权限边界；人类在环（Human-in-the-loop）设计。

**验证**：让它执行 `ls`，再让它执行 `rm -rf /`（看是否被拦截）。

---

### Step 4：联网搜索工具

**方案**：使用 `smolagents` 内置的 `DuckDuckGoSearchTool`（无需 API key）。

**修改**：`agent.py` 中加入：
```python
from smolagents import DuckDuckGoSearchTool
agent = CodeAgent(
    tools=[read_file, write_file, run_command, DuckDuckGoSearchTool()],
    model=model
)
```

**你会学到**：工具链的组合使用；信息检索 → 综合的完整链路。

**验证**：问一个需要实时信息的问题。

---

## 8. 安全与约束

- 命令执行工具默认启用危险命令检测和人类确认
- `.env` 文件包含 API key，已加入 `.gitignore` 保护
- 所有工具函数设置 `timeout`，避免长时间阻塞

---

## 9. 成功标准

- [ ] Step 1：能进行多轮对话，理解上下文
- [ ] Step 2：能正确读写文件，Agent 能解释它为什么调用 read/write
- [ ] Step 3：能执行安全命令，危险命令被拦截或需确认
- [ ] Step 4：能搜索网络信息并综合回答
- [ ] 每步运行时可观察到完整的 Thought → Action → Observation 链
