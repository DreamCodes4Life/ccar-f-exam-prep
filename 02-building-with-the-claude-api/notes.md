# Step 2: Building with the Claude API

[Anthropic Academy course](https://anthropic.skilljar.com/claude-with-the-anthropic-api) · 12 lessons · about 10 hours · exam domains 1, 2, 4 (and a first look at 3 and 5)

Every lesson has a notebook here, run on `claude-sonnet-5-5` with its outputs saved. The notebooks follow the course's order and examples, explain each idea before the code, and mark what has changed since the course (`Changed since the course`), what goes beyond it (`Beyond the course`) and what matters for the exam (`Exam angle`). The exam points are collected per domain in [`../exam/`](../exam/).

| Lesson | Notebook | Exam domains |
|---|---|---|
| 2.1 Intro and API basics: requests, multi-turn chat, system prompts | [01-api-basics.ipynb](01-api-basics.ipynb) | 4, 5 |
| 2.2 Streaming and structured data | [02-streaming-and-structured-data.ipynb](02-streaming-and-structured-data.ipynb) | 4 |
| 2.3 Prompt evaluation: test datasets, running evals, grading | [03-prompt-evaluation.ipynb](03-prompt-evaluation.ipynb) | 4, 5 |
| 2.4 Prompt engineering: clear, specific, XML tags, examples | [04-prompt-engineering.ipynb](04-prompt-engineering.ipynb) | 4 |
| 2.5 Tool use: tool functions, schemas, message blocks, tool results | [05-tool-use-basics.ipynb](05-tool-use-basics.ipynb) | 1, 2 |
| 2.6 Tool use: multi-turn loops, multiple tools, built-in tools | [06-tool-use-loops-and-built-in-tools.ipynb](06-tool-use-loops-and-built-in-tools.ipynb) | 1, 2, 4 |
| 2.7 RAG and agentic search: chunking, embeddings, BM25 | [07-rag-and-agentic-search.ipynb](07-rag-and-agentic-search.ipynb) | 5, 2 |
| 2.8 Features of Claude: thinking, images, PDFs, citations, caching | [08-features-of-claude.ipynb](08-features-of-claude.ipynb) | 5, 4 |
| 2.9 Model Context Protocol: servers, tools, resources, prompts, client | [09-model-context-protocol.ipynb](09-model-context-protocol.ipynb) and [mcp_docs_server/](mcp_docs_server/) | 2 |
| 2.10 Claude Code setup and MCP | [10-claude-code-and-mcp.ipynb](10-claude-code-and-mcp.ipynb) | 3, 2 |
| 2.11 Agents and workflows | [11-agents-and-workflows.ipynb](11-agents-and-workflows.ipynb) | 1 |
| 2.12 Final assessment | (the course's own quiz, not reproduced here) | |

## Setup

- Python 3.12 virtual environment, packages in [`../requirements.txt`](../requirements.txt): `anthropic`, `python-dotenv`, `mcp`, `fastembed`, `matplotlib`, `notebook`, `ipykernel`. In VS Code: the Python and Jupyter extensions, then *Select Kernel* → `.venv`.
- API key: [Claude Console](https://platform.claude.com) → Keys → Create key. The Console now first asks where the code runs; "Somewhere else" gives an API key (on your own machine you can also sign in with the `ant` CLI and skip the key). The key goes in `.env` at the repo root (`ANTHROPIC_API_KEY=...`), which is gitignored; `load_dotenv()` + `Anthropic()` pick it up.
- Cost of running all eleven notebooks once: about 110 requests on Sonnet 5.5, roughly $1.50.
- Practice: notebooks 2.1 and 2.2 have exercises (four and three), each with a task, a *Your turn* cell, a hint, a solution and a *Check* cell that prints ✅ when it works. Write your own code, run it, then run the check.

## Key ideas, lesson by lesson

**2.1** Claude is a family of models: Haiku 5.5 (fast, cheap), Sonnet 5.5 (the everyday balance), Opus 5.5 (long, complex work), Fable 5.2 (most capable); start with the smallest that passes your evals. One endpoint, `messages.create`, with `model`, `max_tokens` and `messages`. The answer is a list of content blocks; read the `text` ones and check `stop_reason` and `usage`. The API is stateless: your code keeps the conversation and resends all of it each turn. The system prompt sets role and rules, but it is guidance: rules that must always hold go in code. `max_tokens` cuts an answer off silently: only `stop_reason == "max_tokens"` tells you. Without `temperature`, ask for variety in the prompt (several options in one call).

**2.2** Streaming sends the answer as events while it's written (out of exam scope). For data a program reads, use structured outputs (`output_config.format` with a JSON schema, or `client.messages.parse()` with a Pydantic model). A schema guarantees shape, not truth: check business rules in code, and make fields nullable when the information may be missing.

**2.3** Evaluate prompts with a dataset, not a single try: generate cases, run the prompt on each, grade with code where the check is mechanical (JSON, Python, regex) and with a model grader against explicit criteria, then average. Read the grader's reasons, and look at segments, not just the overall score.

**2.4** Clear and direct, specific, XML tags, examples: each change measured with the 2.3 pipeline. In this run, being specific helped most (4.3 → 6.7 out of 10); tags and an example changed little on short inputs, and a plausible "check your arithmetic" instruction made things worse. Measure; don't assume.

**2.5** Tools: a name, a description and an input schema. Claude returns a `tool_use` block; your code runs the function and sends a `tool_result` with the same id. Descriptions drive tool choice. Errors go back with `is_error: true` and a message the model can act on, kept apart from "found nothing".

**2.6** The tool loop runs while `stop_reason == "tool_use"` and ends on `end_turn`; a turn cap is only a safety net. Parallel calls come back in one user message. Structured data through a tool now uses `auto` + `strict: true` (forced `tool_choice` returns a 400 on Sonnet 5.5). Built-in tools: the text editor (you run it, sandboxed) and web search (Anthropic runs it).

**2.7** RAG retrieves a few relevant chunks instead of sending everything. Embeddings find meaning; BM25 finds exact terms like error codes; reciprocal rank fusion combines them. Agentic search gives Claude the retriever as a tool, so it can search again for what a first result depends on.

**2.8** Adaptive thinking with an effort setting (`budget_tokens` returns a 400 now). PDFs as `document` blocks; images are vision (out of scope). Citations point each claim to the source passage. Prompt caching stores a long, stable prefix: it's an exact prefix match, 5-minute default lifetime, at least 512 tokens on Sonnet 5.5.

**2.9** MCP: a host runs one client per server; local servers talk over stdio. Tools are model-controlled, resources app-controlled, prompts user-controlled. The course's document server is in [`mcp_docs_server/`](mcp_docs_server/), built with the current `mcp` package.

**2.10** Claude Code: CLAUDE.md files at four levels (combined, not overridden), permissions checked deny → ask → allow, and MCP servers in local, project (`.mcp.json`, committed) or user scope, with `${VAR}` placeholders for secrets. CLAUDE.md guides; deny rules and hooks enforce.

**2.11** Workflows put the steps in code (chaining, routing, parallelization, evaluator–optimizer); agents let Claude choose them. Start with the simplest option. Guards, stop conditions and an independent final check live in code. A subagent doesn't inherit the coordinator's conversation, so the hand-off must carry the full context.

## Changed since the course

| The course | Now (Sonnet 5.5, Opus 5.5, Python SDK 2.x) |
|---|---|
| `message.content[0].text` | The first block can be `thinking`: pick the first block of type `text` |
| `temperature=...` | The SDK rejects the argument; the API returns a 400. Use `output_config={"effort": ...}` |
| Prefill the assistant turn (e.g. with `{`) to get JSON | 400; use structured outputs or a strict tool |
| Force a tool with `tool_choice` to get structured data | 400 on Sonnet/Opus 5.5; `auto` + `strict: true` + an instruction, or structured outputs. Exam questions may still describe forcing a tool |
| `thinking={"type": "enabled", "budget_tokens": N}` | 400; `{"type": "adaptive"}` + `output_config.effort` |
| Voyage AI embeddings | Local `fastembed` model (`BAAI/bge-small-en-v1.5`), no extra key |
| `FastMCP` and a hand-written client class | `mcp` 2.x: `MCPServer`, and the built-in `mcp.Client`; raise `ToolError` to pass a useful message to the model |
| Files API under `client.beta` | `client.files`, no beta header |

## Gotchas hit while running

- Prompt v1 in 2.3 scored 9.75/10: an eval near the ceiling can't measure improvements; it needs harder cases.
- The 2.3 grader marked down a missing docstring that the prompt itself had forbidden: grading criteria and prompt must agree.
- With `max_tokens=400`, parallel reviews in 2.11 were cut mid-sentence and nothing noticed: check `stop_reason == "max_tokens"`, and state a length the step can meet.
- BM25 in 2.7 ranked a common word above an error code until stopwords were removed; zero-score results polluted the fused ranking.
- Web search (`web_search_20260209`) ran its search through code execution and returned no citation blocks in that run; the notebook prints the returned pages instead.
- In mcp 2.x, a plain exception in a tool reaches the model only as a generic error; `ToolError` carries the message.
- Each `async with` connection to a stdio MCP server starts a fresh server process, so in-memory state doesn't survive between connections.

## Exam-style questions

My own scenarios, one or two per lesson. Answers are at the end of each.

1. **(2.2, D4)** An invoice pipeline uses structured outputs; every record parses, but about 3% have line items that don't add up to the stated total. Best next step? A) "Make sure totals add up" in capitals. B) Check totals in code; retry with the specific error, and send records whose source is inconsistent to a human. C) Go back to prefill. D) Max effort everywhere. **B**: a schema guarantees syntax, not semantics.
2. **(2.2, D4)** An extractor invents order numbers when an email has none. A) Make `order_id` nullable and say "null if absent". B) Few-shot examples that all have IDs. C) Drop records with a regex. D) A larger model. **A**: a required field pushes the model to fabricate.
3. **(2.3, D4)** You must know that generated SQL is valid and answers the question. A) Model grader only. B) Human review of everything. C) Code check that it parses, plus a model grader with per-case criteria. D) Code for both. **C**.
4. **(2.3, D5)** 97% overall extraction accuracy; the team wants to cut human review. A) Cut it now. B) Measure per document type and field, keep sampling, cut only where each segment meets the bar. C) Trust a self-reported confidence above 0.9. D) Re-run the eval. **B**.
5. **(2.4, D4)** A code-review prompt reports so many style nits that developers ignore it. A) "Only report important issues". B) List what to report (bugs, security) and what to skip (style), with an example of each. C) A second model to classify importance. D) Fine-tune. **B**: explicit criteria before classifiers.
6. **(2.5, D2)** An agent calls `search_orders` even when it has an exact order ID for `lookup_order`; both have one-line descriptions. A) A routing classifier. B) Rewrite both descriptions: what, when (e.g. "use when you have an ID like ORD-12345"), input format, how they differ. C) Merge them. D) Force `tool_choice`. **B**.
7. **(2.5, D2)** An inventory tool returns an empty string on a timeout, and the agent says the item is out of stock. A) Return `is_error: true` with a structured, retryable error, and keep "no stock" a normal result. B) A longer timeout. C) A prompt line saying empty may mean error. D) Retry forever. **A**.
8. **(2.6, D1)** An agent loop stops when the reply says "Done" or after 5 turns; it sometimes stops with calls pending or cuts long tasks short. A) Cap 50. B) Continue while `stop_reason == "tool_use"`, end on `end_turn`, cap only as a safety net. C) Match "TASK COMPLETE". D) Stop at the first text block. **B**.
9. **(2.7, D5)** Vector-only retrieval over a big manual fails when users paste exact error codes. A) A bigger embedding model. B) Add BM25 and fuse the rankings. C) The whole manual in the prompt. D) Fine-tune. **B**.
10. **(2.8, D5)** The same 30k-token contract is sent with each of ~20 questions a user asks within minutes. A) Message Batches. B) Prompt caching, contract first with `cache_control`, question after. C) Summarise the contract. D) A smaller model. **B**: a user is waiting, so batches don't fit.
11. **(2.8, D5)** After adding caching, `cache_read_input_tokens` stays 0; the system prompt starts with "Current time: {now}". **The timestamp changes the prefix every time: move it after the cache marker.**
12. **(2.9, D2)** A company style guide must be in context at the start of every session, but as a `get_style_guide` tool Claude sometimes skips it. A) A more emphatic description. B) Expose it as a resource the host attaches up front. C) A user-invoked prompt. D) Paste it into every tool description. **B**: data that must always be present is app-controlled.
13. **(2.10, D3)** A team needs the same ticketing MCP server; each developer has a personal token; the repo is public. A) Each runs `claude mcp add` locally. B) A committed `.mcp.json` with `${TICKETS_TOKEN}`, each developer exports their own. C) A committed shared token. D) A wiki page for user scope. **B**.
14. **(2.10, D3)** CLAUDE.md says "never run migrations", yet Claude Code ran one. A) Capitals and IMPORTANT. B) A deny rule (`Bash(alembic upgrade *)`) in the committed settings, or a PreToolUse hook. C) Move the line to `CLAUDE.local.md`. D) Always plan mode. **B**: CLAUDE.md guides, rules and hooks enforce.
15. **(2.11, D1)** Invoices go through fixed, auditable steps (extract, check against the PO system, file). A) An autonomous agent. B) A workflow with checks in code between steps. C) A coordinator with parallel subagents. D) An evaluator–optimizer loop. **B**.
16. **(2.11, D1)** A subagent's summaries ignore the EU-only constraint the user gave the coordinator earlier. **State the constraint in the delegation: subagents don't inherit the coordinator's conversation.**

## Links

- Course: https://anthropic.skilljar.com/claude-with-the-anthropic-api (lesson links in [`../learning-path.md`](../learning-path.md))
- Claude API docs: https://platform.claude.com/docs · Claude Code docs: https://code.claude.com/docs · MCP: https://modelcontextprotocol.io
- Exam revision sheets: [`../exam/`](../exam/)
