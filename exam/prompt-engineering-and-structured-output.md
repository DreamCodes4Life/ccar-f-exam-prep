# Domain 4: Prompt Engineering & Structured Output (20%)

Writing prompts that work, measuring them, and getting output a program can use. Points are tagged with the step and lesson they come from.

## Prompts

- The **system prompt** sets role, tone and rules for the whole conversation. It's guidance followed very reliably, not a guarantee: rules that must always hold are enforced in code. (2.1)
- Techniques, in the course's order: be **clear and direct** (the task in the first line), be **specific** (qualities or steps to follow), use **XML tags** to separate instructions from data, give **examples** (one or a few good answers). (2.4)
- Explicit criteria are the first fix for vague or inconsistent output, before classifiers or extra calls. (2.4)

## Evals

- Don't judge a prompt by one try. Build a dataset of test cases (Claude can generate them), run the prompt on each, grade, and average. Change one thing, re-run, compare. (2.3)
- **Code-based graders** check what code can check (valid JSON, Python that parses, a regex that compiles). **Model-based graders** score the rest against clear criteria, with a score and a reason, returned as structured output. (2.3)

## Structured output

- When a program reads the answer, use a schema: `output_config.format` with a JSON schema on `messages.create`, or `client.messages.parse()` with a Pydantic model. The reply is guaranteed to match. (2.2)
- A tool with `strict: true` is the other route: the tool's input is the structured data. (2.6)
- **Guide vs current API.** The course got JSON by prefilling the assistant turn with `{` and a stop sequence; prefill returns a 400 on current models. The exam may describe forcing a tool (`tool_choice` = the tool) to get structured output; on Opus 5.5 and Sonnet 5.5 forced `tool_choice` returns a 400, so code uses `auto` + `strict: true` or structured outputs. Answer exam questions the way the guide frames them.
- Citations can't be combined with `output_config.format`. (2.8)
- A schema guarantees **shape, not truth**: every record parses, but numbers can still disagree (line items that don't add up to the total). Check such rules in code; if the model got it wrong, retry with the specific error; if the source itself is inconsistent, flag it for a human. (2.2)
- Make fields **nullable** when the information may be missing, and say "null if absent": a required field pushes the model to invent a value. An `"other"` enum value plus a detail field handles unexpected categories. (2.2, 2.6)
- Write explicit criteria instead of "be thorough" or "be conservative": say which issues to report and which to skip, with an example of each. (2.4)
- A model checking its own work in the same request shares its blind spots. Calculations and must-hold rules go to code or a tool; judgement calls can go to an independent reviewer call. (2.4)
- With few test cases, small score differences are noise. In the 2.4 run, being specific helped most; XML tags and an example changed little on short inputs, and a plausible "check your arithmetic" instruction lowered the score. Measure, don't assume. (2.4)

## Scenario patterns

- "Output must always parse": schema (structured outputs or a strict tool), not "please return JSON".
- "Quality varies and nobody knows if a prompt change helped": build an eval first.
