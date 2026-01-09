#!/bin/bash
set -euo pipefail

# Read the tool info from stdin
input=$(cat)
tool_name=$(echo "$input" | jq -r '.tool_name')

# Define the ONLY allowed tool (MCP tools use format: mcp__servername__toolname)
# Our MCP server is named "code-executor" and the tool is "execute_code"
ALLOWED_TOOL="mcp__code-executor__execute_code"

# Check if this is our allowed tool
if [[ "$tool_name" == "$ALLOWED_TOOL" ]]; then
  # Allow the tool - output JSON to approve
  echo '{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}'
  exit 0
fi

# Block everything else
echo '{"hookSpecificOutput": {
  "hookEventName": "PreToolUse",
  "permissionDecision": "deny",
  "permissionDecisionReason": "Only the execute_code tool is allowed in this plugin. Claude can ONLY execute Python code. Tool attempted: '"$tool_name"'"
}}'
exit 0
