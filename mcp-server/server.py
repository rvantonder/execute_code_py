#!/usr/bin/env python3
"""
MCP Server for execute_code tool.
Exposes Python code execution as an MCP tool.
"""

import asyncio
import json
import sys
import tempfile
import os
import re
from pathlib import Path
from io import StringIO

# MCP SDK imports
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)


def highlight_python(code: str) -> str:
    """Apply ANSI syntax highlighting to Python code."""
    # ANSI color codes
    RESET = "\033[0m"
    BLUE = "\033[34m"      # keywords
    GREEN = "\033[32m"     # strings
    CYAN = "\033[36m"      # numbers
    MAGENTA = "\033[35m"   # function/class names
    YELLOW = "\033[33m"    # comments

    # Keywords
    keywords = r'\b(import|from|as|def|class|if|elif|else|for|while|return|yield|with|try|except|finally|raise|assert|break|continue|pass|lambda|global|nonlocal|True|False|None|and|or|not|in|is)\b'
    code = re.sub(keywords, f'{BLUE}\\1{RESET}', code)

    # Strings (simple pattern - single and double quotes)
    code = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', lambda m: f'{GREEN}{m.group()}{RESET}', code)

    # Numbers
    code = re.sub(r'\b\d+\.?\d*\b', f'{CYAN}\\g<0>{RESET}', code)

    # Comments
    code = re.sub(r'#.*$', lambda m: f'{YELLOW}{m.group()}{RESET}', code, flags=re.MULTILINE)

    return code


class CodeExecutor:
    """Executes Python code and captures results."""

    MAX_RESULT_SIZE = 5000  # characters

    def __init__(self, working_dir="."):
        self.working_dir = Path(working_dir).resolve()

    def execute(self, code: str) -> dict:
        """Execute Python code and return results."""
        original_dir = os.getcwd()
        os.chdir(self.working_dir)

        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture

        response = {
            "success": False,
            "stdout": "",
            "stderr": "",
        }

        try:
            namespace = {
                "__builtins__": __builtins__,
                "__name__": "__main__",
            }

            exec(code, namespace)

            if 'result' in namespace:
                result = namespace['result']
                result_str = str(result)

                if len(result_str) > self.MAX_RESULT_SIZE:
                    with tempfile.NamedTemporaryFile(
                        mode='w',
                        suffix='.txt',
                        delete=False,
                        prefix='execute_code_result_'
                    ) as f:
                        f.write(result_str)
                        response["result_file"] = f.name
                        response["result"] = f"[Result too large ({len(result_str)} chars), written to {f.name}]"
                else:
                    response["result"] = result

            response["success"] = True

        except Exception as e:
            response["error"] = f"{type(e).__name__}: {str(e)}"

        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            response["stdout"] = stdout_capture.getvalue()
            response["stderr"] = stderr_capture.getvalue()
            os.chdir(original_dir)

        return response


# Create MCP server
app = Server("|")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="execute_code",
            description="Execute Python code. Set a 'result' variable to return data. Large results are written to temp files to prevent context overflow.",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "Python code to execute.",
                    },
                    "working_dir": {
                        "type": "string",
                        "description": "Working directory for execution (default: current directory)",
                    },
                },
                "required": ["code"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name != "execute_code":
        raise ValueError(f"Unknown tool: {name}")

    code = arguments.get("code")
    working_dir = arguments.get("working_dir", ".")

    if not code:
        raise ValueError("Missing required parameter: code")

    executor = CodeExecutor(working_dir=working_dir)
    result = executor.execute(code)

    # Format output as text
    output_lines = []

    # Show the executed code with syntax highlighting
    output_lines.append(highlight_python(code))
    output_lines.append("")

    if result["success"]:
        output_lines.append("✓ Execution successful")

        if "result" in result:
            output_lines.append(f"\nResult:\n{json.dumps(result['result'], indent=2, default=str)}")

        if result["stdout"]:
            output_lines.append(f"\nStdout:\n{result['stdout']}")

        if result["stderr"]:
            output_lines.append(f"\nStderr:\n{result['stderr']}")

        if "result_file" in result:
            output_lines.append(f"\n📁 Large result saved to: {result['result_file']}")
    else:
        output_lines.append("✗ Execution failed")
        output_lines.append(f"\nError: {result.get('error', 'Unknown error')}")

        if result["stdout"]:
            output_lines.append(f"\nStdout:\n{result['stdout']}")

        if result["stderr"]:
            output_lines.append(f"\nStderr:\n{result['stderr']}")

    # Check if output is too large and save to file if needed
    full_output = "\n".join(output_lines)
    if len(full_output) > 1000:
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            prefix='execute_code_output_'
        ) as f:
            output_data = {
                "code": code,
                "result": result.get("result") if "result" in result else None,
                "stdout": result.get("stdout", ""),
                "stderr": result.get("stderr", ""),
                "success": result.get("success", False),
                "error": result.get("error") if "error" in result else None
            }
            json.dump(output_data, f, indent=2, default=str)
            json_path = f.name

        # Create a compact summary
        summary_lines = []
        summary_lines.append(highlight_python(code))
        summary_lines.append("")
        summary_lines.append(f"✓ Output saved to: {json_path}")
        summary_lines.append(f"\nThe JSON file contains:")
        summary_lines.append(f"  - code: The executed Python code")
        summary_lines.append(f"  - result: The value of the 'result' variable (if set)")
        summary_lines.append(f"  - stdout: Standard output from the code")
        summary_lines.append(f"  - stderr: Standard error output")
        summary_lines.append(f"  - success: Whether execution succeeded")
        summary_lines.append(f"  - error: Error message (if any)")
        summary_lines.append(f"\nTo access this data, read the file: {json_path}")

        return [TextContent(type="text", text="\n".join(summary_lines))]

    return [TextContent(type="text", text=full_output)]


def main():
    """Run the MCP server."""
    async def _run():
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    asyncio.run(_run())


if __name__ == "__main__":
    # Test highlighting if --test flag is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_code = """import math

result = math.sqrt(91)"""
        print("Testing syntax highlighting:")
        print("=" * 50)
        print(highlight_python(test_code))
        print("=" * 50)
        sys.exit(0)

    main()
