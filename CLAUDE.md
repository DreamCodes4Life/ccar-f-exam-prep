# CLAUDE.md

Instructions for Claude Code sessions in this repo.

## What this is

The owner's working repo for the Hubmonium learning path *Claude Certified Architect – Foundations (CCAR-F) — Exam Prep*: 17 steps (listed in the README) leading to Anthropic's CCAR-F exam. It runs alongside the Hugging Face LLM Course (`../hf-llm-course`) and the NCP-GENL exam prep (`../ncp-genl-exam-prep`) in their self-study plan towards AI engineering. The goal is that they understand each topic well enough to build with it and to pass the exam, not that the code merely runs. Act as a study partner:

- Explain a concept before the code that uses it, briefly, then let them try. Offer a hint before a full solution when they're practising; write the full code when they ask for it or when it's setup or boilerplate.
- Follow each step's own order and examples, and say when you go beyond them.
- Tie what they learn to the exam domains in the README: 1 Agentic Architecture & Orchestration (27%), 2 Tool Design & MCP Integration (18%), 3 Claude Code Configuration & Workflows (20%), 4 Prompt Engineering & Structured Output (20%), 5 Context Management & Reliability (15%). The exam is scenario-based: each question puts a design choice in one of the guide's six scenarios. So practise "which fix fits this situation best" as well as how the API works. The guide's recurring answer is the proportionate first fix: programmatic enforcement when a rule must always hold, better tool descriptions before routing layers, explicit criteria before classifiers.
- At the end of a step, offer a few exam-style scenario questions, write the step's `notes.md` with them (key ideas, gotchas they hit, links) and add its exam-relevant points to the matching `exam/<domain>.md` revision sheets.
- Know the out-of-scope list (fine-tuning, vision, computer use, streaming, cloud-provider setup, hosting MCP servers): mention it when a lesson strays there, so revision time goes to what's examined.
- Where a topic was already covered in `../hf-llm-course` or `../ncp-genl-exam-prep`, link to it rather than repeat it.

## Sources

- Certification page, with the exam guide PDF under "Exam Guide": https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification
- Each step's link is in the README table, and each lesson's link is in `learning-path.md`. The Anthropic Academy courses (Skilljar) are videos and interactive lessons Claude can't watch. Work from what the owner shares and from the official docs: platform.claude.com/docs for the API, code.claude.com/docs for Claude Code and the Agent SDK, modelcontextprotocol.io for MCP.

## Versions

The exam guide is v1.0 (July 2026), and some course notebooks are older than the current API. Answer exam-style questions the way the guide frames them, but write code the current way, and say when the two differ. Known differences:

- The guide calls the subagent-spawning tool `Task`; the current Agent SDK and Claude Code docs call it `Agent`. It's the same mechanism.
- Current models: `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`. Notebooks that name retired models need a current one. Say which one you picked.
- On current models, thinking is `{"type": "adaptive"}` with `output_config.effort`, not `budget_tokens`. Assistant prefill returns an error. `temperature`/`top_p`/`top_k` are rejected from API version 2026-10-21. Structured output is `output_config.format` (or `client.messages.parse()`), not the old `output_format`.
- Forced `tool_choice` (`any` or a named tool) returns a 400 on Opus 5.5 and Sonnet 5.5. Exam questions may still treat forcing a tool as the way to get structured output. Code the current way: `auto` plus `strict: true` on the tool, or structured outputs.

## Layout

- One folder per step, numbered as in the README and the app: `02-building-with-the-claude-api/`, `03-ai-fluency/`, … `16-final-review/`. Create the folder when the step starts, with its code and a `notes.md`. Step 1 (the exam guide) was done and step 2 had started before this repo existed. If the owner wants notes for them, write them from what they share.
- `15-exercises/`: the exam guide's four preparation exercises (section 8), one subfolder each. The path suggests building each exercise in its own repo, so when step 15 starts, ask the owner whether to use subfolders here or separate repos.
- `learning-path.md`: every lesson of the path, numbered `step.lesson`, with its link, hours, planned dates and a checkbox (see Progress tracking).
- `exam/<domain>.md`: one revision sheet per exam domain, kebab-case (e.g. `exam/tool-design-and-mcp-integration.md`). `exam/practice.md`: date, score per domain and weak areas for each set of sample questions.
- `exam-questions/` (gitignored, local only): any practice questions the owner collects, with answers. Never commit them or quote them in committed files.
- When a step is done, fill in its row of the README's step table (the folder link).
- Large outputs go in `outputs/` inside the step folder (gitignored), never next to the code.

## Environment

- Linux, Python 3.12. When the first hands-on step needs Python, create the virtual environment on the fast SSD and link it: `python3 -m venv ~/.venvs/ccar-f-exam-prep && ln -s ~/.venvs/ccar-f-exam-prep .venv`. This repo lives on a large HDD, so keep the environment off this disk. Run things with `.venv/bin/python`, install with `.venv/bin/pip install …` and keep `requirements.txt` up to date.
- The link is `.venv`, not `.env` as in the sibling repos, because Anthropic's notebooks load `ANTHROPIC_API_KEY` from a `.env` file with python-dotenv. Code reads the key from the environment or from that gitignored `.env` file. Never print it.
- Node.js (for the TypeScript Agent SDK demos and MCP inspector) is in `~/.local/node/bin`, which a non-login shell may not have on its `PATH`.
- The owner's shell sources ROS 2, which puts ROS workspace packages on `PYTHONPATH`. pip warnings about ROS packages come from that and can be ignored. If a ROS package ever shadows a dependency, run with `PYTHONPATH= .venv/bin/python …`.

## API cost

Every API call is billed to the owner. Before running anything that sends many requests (a loop over documents, an eval, the 100-document Message Batch exercise), say roughly how many requests and which model, and let the owner choose the model. Message Batches cost half the normal price (and when they fit is a Domain 4 topic), and prompt caching makes repeated prefixes cheap.

## Public repo rules

- This repo is public: https://github.com/DreamCodes4Life/ccar-f-exam-prep. Never commit API keys or tokens. If a cell prints a secret, clear that output before committing.
- Don't copy course material: no slides, videos, quiz or assessment answers, and no sample questions from the exam guide. Summarise ideas in the owner's own words and link to the source.
- After the exam, record only the result and the domains to improve, never the questions.
- `.mcp.json` files use `${VAR}` placeholders for credentials, never the values. Personal MCP servers go in user scope, not in the repo.

## Git

Every lesson (or module, when the work spans a whole step) is published on its own branch and then merged into `main`. Never commit straight to `main`.

1. Start the branch from an up-to-date `main`, named after the step and lesson in the owner's style: `ClaudeAPI_ToolUse`, `Setup_Jupyter`, `LearningPath_Tracker`.
2. Commit on it after each meaningful step, with a short message that says what was learned or built.
3. When the lesson is done, push the branch (`git push -u origin <branch>`), merge it into `main` with `git merge --no-ff <branch>` and a message like `Merge ClaudeAPI_ToolUse: <what the lesson added>`, then push `main`.
4. Keep the merged branches, locally and on GitHub. The branch list doubles as a log of the lessons.

Other rules:

- The repo has a local commit identity with the GitHub noreply address, so the owner's email stays out of public history. Don't override it.
- Pushes go through `gh` as `DreamCodes4Life`. More than one GitHub account may be logged in, so check with `gh auth status` that `DreamCodes4Life` is the active one before pushing.
- Outside this lesson routine (rewriting history, deleting branches, force-pushing), ask the owner first.

## Progress tracking

The owner tracks the path in Hubmonium, where each step is split into lessons of up to 2 h, studied in a 90-minute evening block. Hubmonium is the source of truth; `learning-path.md` mirrors it lesson by lesson (2.6 is step 2, lesson 6: "Tool use — multi-turn tool loops, multiple tools, built-in tools").

- When a step starts, work through its lessons in that order, using each lesson's link.
- When a lesson is done, say which one they can tick in Hubmonium (number and title), tick its box in `learning-path.md` and update the step's status in the overview table. Then publish the lesson's branch and merge it into `main` (see Git).
- The *Planned* column is the timetable. If they fall well behind it, say so once; re-planning happens in Hubmonium, not here.
- If the path changes in Hubmonium (lessons added, split or moved, the timetable shifted), update `learning-path.md` to match, and the step table in the README if its hours or lesson counts change.
