"""A small MCP server that exposes an in-memory set of documents (lesson 2.9).

Primitives, in MCP terms:
- tools (model-controlled):     read_doc_contents, edit_document
- resources (app-controlled):   docs://documents (the list of ids), docs://documents/{doc_id} (one document)
- prompts (user-controlled):    format (rewrite a document in Markdown), summarize

The documents live in a Python dict, so edits last only as long as the server process.
Built with the `mcp` Python SDK 2.x, where the v1 `FastMCP` class is now `MCPServer`.

Run it over stdio (what Claude Code and the notebook client do):
    python server.py
"""

from typing import Annotated

from pydantic import Field

from mcp.server.mcpserver import MCPServer, UserMessage
from mcp.server.mcpserver.exceptions import ResourceError, ToolError

mcp = MCPServer(
    "docs",
    instructions="Read and edit a small set of internal documents. Document ids look like file names, e.g. 'roadmap.md'.",
)

docs: dict[str, str] = {
    "roadmap.md": "Q1 roadmap: ship offline mode for the mobile app in February, then migrate billing to the new "
    "payments provider in March. Offline mode depends on the sync service rewrite, which is two weeks late.",
    "incident-0312.txt": "Incident 0312. On 12 March the search API returned errors for 47 minutes. Cause: an "
    "expired TLS certificate on the internal index cluster. Fix: certificate renewed, expiry alerts added at 30 and 7 days.",
    "onboarding.docx": "New engineers get laptop access on day one, a buddy for the first two weeks, and their first "
    "small ticket by day three. Production access needs the security course and a manager's approval.",
    "budget.pdf": "The 2027 infrastructure budget is 1.2 million euros, 8 percent more than 2026. Most of the "
    "increase pays for GPU capacity for the recommendation models.",
    "retro-notes.txt": "Sprint 41 retro. Went well: releases on time, fewer flaky tests. To improve: code reviews wait "
    "too long, average 26 hours. Action: two reviewers on rotation each day.",
    "api-guidelines.md": "Public APIs use nouns for resources, plural collection names, ISO 8601 dates and cursor "
    "pagination. Breaking changes need a new version prefix and six months of overlap.",
}


# ---------- tools: Claude decides when to call these ----------

@mcp.tool(
    name="read_doc_contents",
    description="Read the full text of one document. Use it before answering a question about a document's "
    "content or before editing it. Fails if the id is unknown.",
)
def read_document(doc_id: Annotated[str, Field(description="Id of the document to read, e.g. 'roadmap.md'")]) -> str:
    if doc_id not in docs:
        # ToolError: the message reaches the model (is_error=True), so it can recover.
        # A plain exception would only say "Error executing tool ..." and keep the details on the server.
        raise ToolError(f"Document '{doc_id}' not found. Known ids: {', '.join(sorted(docs))}")
    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing an exact piece of text with new text. Read the document first so "
    "old_str matches exactly (case and punctuation included). Fails if the text is not found.",
)
def edit_document(
    doc_id: Annotated[str, Field(description="Id of the document to edit")],
    old_str: Annotated[str, Field(description="Exact text to replace, copied from the document")],
    new_str: Annotated[str, Field(description="Text to put in its place")],
) -> str:
    if doc_id not in docs:
        raise ToolError(f"Document '{doc_id}' not found. Known ids: {', '.join(sorted(docs))}")
    if old_str not in docs[doc_id]:
        raise ToolError(f"Text not found in '{doc_id}'. Read the document and copy old_str exactly.")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    return f"Edited '{doc_id}'."


# ---------- resources: the application decides when to read these ----------

@mcp.resource("docs://documents", mime_type="application/json", description="The ids of all documents")
def list_docs() -> list[str]:
    return list(docs)


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain", description="The text of one document")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ResourceError(f"Document '{doc_id}' not found")
    return docs[doc_id]


# ---------- prompts: the user picks these, e.g. as a slash command ----------

@mcp.prompt(name="format", description="Rewrite a document in Markdown and save it with the edit tool.")
def format_document(doc_id: Annotated[str, Field(description="Id of the document to format")]) -> list[UserMessage]:
    return [
        UserMessage(
            f"""Reformat the document <document_id>{doc_id}</document_id> as Markdown.

Use headings, bullet lists and bold text where they make it easier to scan. Keep every fact; don't add new ones.
Read the document with the read_doc_contents tool, then save the new version with the edit_document tool
(replace the whole old text with the Markdown text). Finally, reply with the Markdown version only."""
        )
    ]


@mcp.prompt(name="summarize", description="Summarise a document in one sentence.")
def summarize_document(doc_id: Annotated[str, Field(description="Id of the document to summarise")]) -> list[UserMessage]:
    return [UserMessage(f"Read the document '{doc_id}' with the read_doc_contents tool and summarise it in one sentence.")]


if __name__ == "__main__":
    mcp.run()  # stdio transport by default
