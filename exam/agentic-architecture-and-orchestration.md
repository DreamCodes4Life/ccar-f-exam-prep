# Domain 1: Agentic Architecture & Orchestration (27%)

The biggest domain. How agents loop, how work is split between a coordinator and subagents, when a fixed workflow beats an agent, and where checks belong in code. Points are tagged with the step and lesson they come from.

## The agent loop

- An agent is a loop: send the conversation and tools, and while `stop_reason == "tool_use"`, run the requested tools, append the assistant turn and the results, and call again. Stop on `end_turn`. (2.6)
- Append the **whole** `response.content` as the assistant turn (text, `tool_use` and any `thinking` blocks), not just the text. (2.5, 2.6)
- Several `tool_use` blocks in one turn are parallel calls: run them, and return **all** `tool_result` blocks in **one** user message. (2.6)
- A failing tool returns a `tool_result` with `is_error: true` and a useful message, so the model can retry or change course. Silent failures or dropped results break the loop. (2.6)
- Give every loop a stopping point beyond the model's own `end_turn`: a maximum number of turns, a budget, or a check in code. (2.11)
- The loop's signal is `stop_reason`. Anti-patterns: stopping when the reply text says "done", or using the iteration cap as the main stop (it cuts long tasks short). The cap is only a safety net. (2.6)
- Every `tool_result` carries the `tool_use_id` of the call it answers; a mismatched or missing result breaks the conversation. (2.5)

## Workflows vs agents

- **Workflow**: your code fixes the steps. **Agent**: the model picks the next step, in a loop with tools. (2.11)
- Workflow patterns: **chaining** (one call's output feeds the next, often a draft then a check against explicit rules), **routing** (classify first, then send to a specialised prompt), **parallelization** (independent sub-tasks at once, then aggregate), **evaluator–optimizer** (one call grades, another revises, for a bounded number of rounds). (2.11)
- Start with the simplest thing that works: one call, then a workflow, and an agent only when the steps can't be known in advance. Agents cost more, take longer and are harder to predict. (2.11)
- Agents work best when they can inspect their environment: read the state before acting, and check the result after. (2.11)
- Guards live in code: limit what the agent may write, cap the turns, and verify the outcome independently after the agent says it's done. In the 2.11 evaluator–optimizer run, the text still failed after the last allowed round and was handed to a person: the stop condition working as intended. (2.11)
- Parallelization is the shape of a coordinator with parallel subagents: independent sub-tasks at once, then one call combines them. (2.11)
- A subagent doesn't inherit the coordinator's conversation: the delegation must state every constraint (region, dates, format) and the results come back summarised. (2.11)
- Agentic search is an agent loop too: give Claude the retriever as a tool, with a description that says to search again for anything a result depends on, and a turn limit in code. (2.7)

## Scenario patterns

- A rule that must **always** hold (a refund limit, an approval before a payment): enforce it in code before the tool runs, not with stronger prompt wording. (2.1, 2.11)
- A task with fixed, known steps: a workflow, not an autonomous agent.
- Subagent tool: the exam guide calls it `Task`; current Claude Code and Agent SDK docs call it `Agent`. Same mechanism.
