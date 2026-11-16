# mcp_docs_server

A small MCP server for lesson 2.9 ([notebook](../09-model-context-protocol.ipynb)): six in-memory documents exposed as

- tools: `read_doc_contents`, `edit_document` (model-controlled)
- resources: `docs://documents` and the template `docs://documents/{doc_id}` (application-controlled)
- prompts: `format`, `summarize` (user-controlled)

Built with the `mcp` Python SDK 2.x (`MCPServer`, formerly `FastMCP`). Edits live only as long as the server process.

```bash
# from the repo root: try it in the MCP Inspector
PATH="$HOME/.local/node/bin:$PATH" npx @modelcontextprotocol/inspector \
    .venv/bin/python 02-building-with-the-claude-api/mcp_docs_server/server.py

# or add it to Claude Code for yourself only (local scope)
claude mcp add docs -- "$PWD/.venv/bin/python" "$PWD/02-building-with-the-claude-api/mcp_docs_server/server.py"
```
