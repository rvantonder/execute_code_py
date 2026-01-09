# Code-Only Environment - Detailed Explanation

## Architecture

The code-only environment is created through three key components:

### 1. PreToolUse Hook (`hooks/scripts/enforce-tool.sh`)

**Purpose**: Intercepts ALL tool calls before they execute

**Mechanism**:
```bash
# Reads tool name from stdin
tool_name=$(echo "$input" | jq -r '.tool_name')

# Checks against allowed list
ALLOWED_TOOL="mcp__code-executor__execute_code"

if [[ "$tool_name" == "$ALLOWED_TOOL" ]]; then
  # Allow - returns permission decision
  echo '{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}'
else
  # Deny - blocks the tool
  echo '{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", ...}}'
fi
```

**Result**: Any tool that isn't `execute_code` is blocked before execution

### 2. MCP Server (`mcp-server/server.py`)

**Purpose**: Exposes the execute_code tool via Model Context Protocol

**Implementation**:
- Python-based MCP server using official MCP SDK
- Registers single tool: `execute_code`
- Executes code in isolated namespace
- Captures stdout, stderr, and result variable
- Handles large outputs by writing to temp files

**Tool Schema**:
```json
{
  "name": "execute_code",
  "parameters": {
    "code": {
      "type": "string",
      "description": "Python code to execute"
    },
    "working_dir": {
      "type": "string",
      "description": "Working directory (default: current)",
      "optional": true
    }
  }
}
```

### 3. Virtual Environment (`.venv/`)

**Purpose**: Isolated Python execution environment

**Contains**:
- Python 3.8+ interpreter
- MCP SDK package
- Standard library
- No access to host system packages (unless explicitly installed)

**Setup**: Created by `setup-uv.sh` using `uv` package manager

## How Tool Blocking Works

### Request Flow

```
User asks Claude to do something
        ↓
Claude decides which tool to use
        ↓
Tool call is initiated
        ↓
PreToolUse hook intercepts ← ENFORCEMENT POINT
        ↓
Hook checks tool name
        ↓
    ┌───────────────────────────┐
    │ Is it execute_code?       │
    └─────┬─────────────┬───────┘
         YES           NO
          ↓             ↓
        ALLOW         DENY
          ↓             ↓
    Execute tool    Block with message
          ↓             ↓
    Return result   Return denial reason
```

### What Claude Sees

**When allowed (execute_code)**:
```json
{
  "success": true,
  "result": 4,
  "stdout": "",
  "stderr": ""
}
```

**When blocked (any other tool)**:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Only the execute_code tool is allowed in this plugin. Claude can ONLY execute Python code. Tool attempted: Read"
  }
}
```

## Python Execution Details

### Code Execution Sandbox

**Namespace isolation**:
```python
namespace = {
    "__builtins__": __builtins__,
    "__name__": "__main__",
}
exec(code, namespace)
```

**What this means**:
- Each execution starts with clean namespace
- Variables don't persist between calls
- No access to server internals
- Standard library available via imports

### Working Directory

**Default**: Current directory when plugin was loaded
**Configurable**: Pass `working_dir` parameter

```python
# Execute in specific directory
execute_code(
    code="import os; result = os.listdir('.')",
    working_dir="/tmp"
)
```

### Result Variable Convention

**How it works**:
```python
# In your code:
result = 42

# What happens:
if 'result' in namespace:
    result = namespace['result']
    # Returned to Claude
```

**If no result variable**:
- Code still executes
- stdout/stderr captured
- No result value returned (only side effects visible)

### Output Capture

**stdout** - Print statements:
```python
print("Hello")  # Captured in stdout field
result = 42
```

**stderr** - Errors and warnings:
```python
import sys
sys.stderr.write("Warning!")  # Captured in stderr field
result = 42
```

**result** - Return value:
```python
result = {"answer": 42}  # Captured in result field
```

### Large Output Handling

**Threshold**: 5000 characters

**When result > 5000 chars**:
```python
result = "x" * 10000  # Too large

# Response includes:
{
  "success": true,
  "result_file": "/tmp/execute_code_result_abc123.txt",
  "result": "[Result too large (10000 chars), written to /tmp/execute_code_result_abc123.txt]"
}
```

**Why**: Prevents context overflow in Claude's working memory

## Security Model

### What's Protected

✅ **Filesystem access controlled**: Code runs as current user, standard file permissions apply
✅ **Network access controlled**: Standard OS network restrictions apply
✅ **No tool escalation**: Cannot bypass to use other Claude tools
✅ **Hook enforcement**: Tool blocking happens at protocol level, cannot be bypassed

### What's NOT Protected

⚠️ **Code execution is real**: Runs on actual hardware with user permissions
⚠️ **No timeout**: Long-running code will block
⚠️ **No memory limits**: Can consume available memory
⚠️ **No CPU limits**: Can use available CPU
⚠️ **No sandboxing**: Not running in container/VM by default

### Best Practices for Safe Use

1. **Review code before execution** - Understand what it does
2. **Use in trusted environments** - Don't run untrusted code
3. **Consider containerization** - Run plugin in Docker for isolation
4. **Set resource limits** - Use OS-level restrictions if needed
5. **Monitor execution** - Watch for runaway processes

## Why This Design?

### Focus and Clarity

**Problem**: Claude has many tools - sometimes overwhelming or distracting

**Solution**: Reduce to single tool - forces focus on pure computation

**Benefit**:
- Clear mental model for Claude
- Predictable behavior
- No tool selection confusion
- Pure code execution environment

### Educational Value

**Use Case**: Teaching environments where you want students to work through problems computationally rather than reading solutions

**Benefit**:
- Forces algorithmic thinking
- No shortcuts via file reading
- Must construct solutions from scratch
- Builds problem-solving skills

### Safety Through Restriction

**Use Case**: Environments where file system access is dangerous or undesired

**Benefit**:
- Cannot accidentally read sensitive files
- Cannot write unwanted files
- Computational only - safe for public demos
- Reduced attack surface

### Specialized Workflows

**Use Case**: Pure calculation/computation tasks where file I/O is noise

**Benefit**:
- Claude focuses on math/logic/computation
- No distraction from file operations
- Faster, more direct responses
- Clean separation of concerns

## Comparison with Standard Claude

| Capability | Standard Claude | Code-Only Claude |
|-----------|----------------|------------------|
| Read files | ✅ | ❌ |
| Write files | ✅ | ❌ |
| Edit files | ✅ | ❌ |
| Run bash | ✅ | ❌ |
| Search files | ✅ | ❌ |
| Execute code | ✅ | ✅ |
| Web access | ✅ | ❌ |
| Spawn agents | ✅ | ❌ |

**Result**: Code-only Claude = "Pure Python REPL" mode

## Technical Limitations

### Current Constraints

1. **No persistent state** - Each execution starts fresh
2. **No package installation** - Only pre-installed packages (unless you modify .venv)
3. **No async execution** - Code runs synchronously
4. **Single thread** - No concurrent executions
5. **No streaming** - Results returned after completion

### Workarounds

**Want to persist state?**
→ Return data as result, have user provide it back

**Want more packages?**
→ Install them in `.venv/` manually

**Want async code?**
→ Can use `asyncio` but execution itself is sync

**Want concurrent execution?**
→ Use `threading` or `multiprocessing` in your code

**Want streaming?**
→ Not supported, print statements captured at end

## Extension Points

### Adding More Tools

Edit `hooks/scripts/enforce-tool.sh`:

```bash
ALLOWED_TOOLS=(
  "mcp__code-executor__execute_code"
  "mcp__another-server__another_tool"
)

if [[ " ${ALLOWED_TOOLS[@]} " =~ " ${tool_name} " ]]; then
  echo '{"hookSpecificOutput": {"permissionDecision": "allow"}}'
fi
```

### Adding MCP Tools

Create new MCP server in `mcp-server/`, register in `.mcp.json`, update hook

### Modifying Execution

Edit `mcp-server/server.py`:
- Change max result size
- Add timeout enforcement
- Add memory limits
- Add package imports
- Modify output formatting

## Summary

The code-only environment is:
- **Enforced** by PreToolUse hooks at protocol level
- **Powered** by MCP server exposing execute_code
- **Isolated** via Python virtual environment
- **Focused** on pure computation without file I/O
- **Extensible** through hook and MCP modifications

This creates a unique execution environment where Claude operates as a pure computational assistant without filesystem or system access.
