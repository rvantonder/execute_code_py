<p align="center">
  <img src="assets/readme-header.svg" alt="Execute Code (Python) - Claude Code Plugin" width="100%" />
</p>

<p align="center">
  <em>A Claude Code plugin that restricts Claude to ONLY use Python code execution. All other tools are blocked, creating a pure computational environment.</em>
</p>

---

## What This Does

- ✅ Allows: `execute_code` - One Tool to Rule Them All. Execute Python code and capture results.
- ❌ Blocks: All other tools (Read, Write, Web Fetch, Edit, Bash, Grep, Glob, etc.)
- 📚 Includes: Built-in skill that educates Claude about the restricted environment

Claude can only run Python code and is forced to write and **execute code** to
do any real work. This creates a constrained environment ideal for
deterministic, computational tasks.

[Blog Post](http://rijnard.com/blog/the-code-only-agent.html)

## Installation

### From Marketplace (Recommended)

```bash
# 1. Add the marketplace
/plugin marketplace add https://github.com/rvantonder/execute_code_py.git

# 2. Install the plugin
/plugin install execute_code_py@execute-code

# 3. Restart Claude Code
```

Now Claude can ONLY execute Python code!

### Python Dependencies

The plugin requires:
- **Python 3.8+**
- **mcp** package (Model Context Protocol SDK)

The MCP package will be installed automatically when you install the plugin. If you need to install it manually:

```bash
pip install mcp>=0.1.0
```

Or using uv (faster):
```bash
uv pip install mcp>=0.1.0
```

## Examples

```
You: randomly generate 1000000 numbers between 0 and 100000 and sort them
```

Claude

```
⏺ code-executor - execute_code (MCP)(code: "...")
  ⎿  PreToolUse:mcp__code-executor__execute_code hook succeeded: Success
  ⎿                                                                                                                                                              
     import numpy as np
     import time

     # Generate 1,000,000 random numbers between 0 and 100,000
     gen_start = time.time()
     numbers = np.random.randint(0, 100001, size=1000000)
     gen_time = time.time() - gen_start

     # Sort the numbers
     sort_start = time.time()
     sorted_numbers = np.sort(numbers)
     sort_time = time.time() - sort_start
```

## Internals and Known Limitations 

This is a concept. Claude Code is not inherently set up to enable what
Code-Only aspires to. For example, calling a custom tool needs to go through an
unnecessary MCP abstraction. Also, we have to use PreHook tooling to restrict
Claude from calling other tools. Native support would provide a much better UX:
elide parameters that the code is called with (currently this is hardcoded to
display in Claude Code) and better highlighting. Nevertheless, the concept
stands!

How it works--

### 1. MCP Server
Exposes the `execute_code` tool with:
- **Input**: Python code string + optional working directory
- **Output**: Execution results, stdout, stderr, and error messages
- **Features**: Captures `result` variable, handles large outputs to temp files

### 2. Tool Enforcement Hook
A PreToolUse hook that:
- Intercepts ALL tool calls before execution
- Allows ONLY `mcp__code-executor__execute_code`
- Denies all other tools with explanation message

### 3. Environment Education Skill
Teaches Claude about:
- The restricted environment and available capabilities
- How to work effectively with only code execution
- Best practices for computational problem-solving

## Tool Definitions

### Schema

```json
{
  "name": "execute_code",
  "description": "Execute Python code. Set a 'result' variable to return data.",
  "parameters": {
    "code": {
      "type": "string",
      "description": "Python code to execute",
      "required": true
    },
    "working_dir": {
      "type": "string",
      "description": "Working directory (default: current directory)",
      "required": false
    }
  }
}
```

### Response Format

```json
{
  "success": true/false,
  "result": "<value of result variable>",
  "stdout": "<captured output>",
  "stderr": "<captured errors>",
  "result_file": "<path if result too large>",
  "error": "<error message if failed>"
}
```
