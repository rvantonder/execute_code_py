#!/bin/bash
# Wrapper script to run the MCP server from the plugin directory
# This ensures the virtual environment is found regardless of CWD

# Get the directory where this script lives (the plugin directory)
PLUGIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to plugin directory and run the server
cd "$PLUGIN_DIR"
exec .venv/bin/python3 mcp-server/server.py
