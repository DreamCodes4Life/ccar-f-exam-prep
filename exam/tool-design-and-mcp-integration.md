# Domain 2: Tool Design & MCP Integration (18%)

Writing tools Claude can use well, and connecting them through the Model Context Protocol. Points are tagged with the step and lesson they come from.

## Tool design

- A tool is a `name`, a `description` and an `input_schema` (JSON Schema). Claude chooses tools by reading the descriptions, so the description is the main lever: what the tool does, when to use it (and when not), what each input means, what it returns. (2.5)
- Wrong-tool choices between similar tools: first make the descriptions clearer and more distinct, before adding a routing layer or a classifier. (2.5)
- Claude never runs a tool. It returns a `tool_use` block (id, name, input); your code runs the function and sends a `tool_result` with the same `tool_use_id`. (2.5)
- Validate inputs in the tool function and return clear errors (`is_error: true`), so the model can correct itself. (2.5, 2.6)
- Keep "the lookup failed" (timeout, permission denied: `is_error: true`, with a category and whether a retry can help) apart from "the lookup worked and found nothing" (a normal result). An empty string on a timeout makes the agent tell users the item doesn't exist. (2.5)
- Three kinds of tools: **your own** (you define and run them), **Anthropic-defined client tools** (text editor, bash: the schema is built in, but you run them, sandbox them and check paths), and **server tools** (web search, web fetch, code execution: Anthropic runs them). (2.6)
- Keep tool sets small, with clearly distinct descriptions; a dedicated tool for an exact lookup ("use when you have an order ID like ORD-12345") beats one vague search tool. (2.5)
- `strict: true` on a tool definition guarantees the input matches the schema (schema needs `additionalProperties: false` and `required`). (2.6)
- Anthropic-defined tools: the **text editor** tool (client side: Claude asks to view, create, replace or insert, your code does it, confined to a safe folder) and **web search** (server side: runs on Anthropic's infrastructure, answers cite sources, billed per search). (2.6)

## MCP

- MCP is a standard way to expose tools and data to any compatible app: an **MCP server** offers them, an **MCP client** inside the app connects, lists what's offered and passes calls through. Transport for local servers: stdio. (2.9)
- Three primitives, by who controls them: **tools** (model-controlled: Claude decides to call them), **resources** (app-controlled: data the app reads, by URI, also as templates like `docs://documents/{id}`), **prompts** (user-controlled: ready-made instructions, like slash commands). (2.9)
- To use MCP tools with the Messages API, the client turns each MCP tool into a tool definition, and forwards each `tool_use` to the server's `call_tool`. (2.9)
- A host runs one client per server. Transports: stdio for a local subprocess, Streamable HTTP for a remote server. (2.9)
- Choosing the primitive: data that must **always** be in context (a style guide) is a resource the host attaches up front; leaving it as a tool lets the model skip it. Actions the model should decide on are tools; workflows the user starts are prompts. (2.9)
- In the current Python SDK (`mcp` 2.x), a plain exception in a tool reaches the model only as a generic error; raise `ToolError` with an actionable message (what was wrong, the expected format), distinct from "nothing found". (2.9)
- Building and running a local server is in scope; hosting MCP servers is out of scope.

## Scenario patterns

- "The agent keeps calling the wrong tool": improve the descriptions first.
- "A tool sometimes gets malformed input": `strict: true` and validation in the function, with an error result the model can act on.
