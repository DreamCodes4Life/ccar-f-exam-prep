# Claude Certified Architect – Foundations (CCAR-F) — exam prep

This repo is my working record while preparing for Anthropic's [Claude Certified Architect – Foundations](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) exam (CCAR-F). It follows the *Claude Certified Architect – Foundations (CCAR-F) — Exam Prep* learning path in [Hubmonium](https://app.hubmonium.com): the notes and code from each step, the exam guide's four hands-on exercises, and revision sheets per exam domain.

It runs alongside the [Hugging Face LLM Course](https://github.com/DreamCodes4Life/hf-llm-course) and my [NCP-GENL exam prep](https://github.com/DreamCodes4Life/ncp-genl-exam-prep) in my self-study plan towards AI engineering.

## The exam

| | |
|---|---|
| Code | CCAR-F |
| Format | 60 questions in 120 minutes. The exam guide describes 6 scenarios; each exam uses 4 of them, picked at random |
| Pass mark | 720 out of 1,000 |
| Price | $125 |
| Where | Pearson VUE, online or at a test centre |
| Who can take it | People at Claude Partner Network organisations, signing in with their work email |
| Valid for | 12 months; renewing on time is a free online assessment |
| Out of scope | Fine-tuning, vision, computer use, streaming, cloud-provider setup, hosting MCP servers |

Details from the official exam guide (v1.0, July 2026), as noted in November 2026. Check the certification page before booking, as Anthropic updates its exams.

## Exam domains and where the path covers them

The numbers in the last column refer to the [steps](#steps) below.

| # | Domain | Weight | Steps |
|---:|---|---:|---|
| 1 | Agentic Architecture & Orchestration | 27% | 2, 11, 13, 15 |
| 2 | Tool Design & MCP Integration | 18% | 2, 7, 8, 15 |
| 3 | Claude Code Configuration & Workflows | 20% | 9, 10, 11, 12, 15 |
| 4 | Prompt Engineering & Structured Output | 20% | 2, 3, 5, 6, 15 |
| 5 | Context Management & Reliability | 15% | 13, 14, 15 |

Step 1 (the exam guide) and step 16 (the final review) cover every domain. Step 4, Claude 101, is a general warm-up from Anthropic's own prep list.

## Steps

About 81.5 hours in 104 lessons of up to 2 hours each, in the path's order. Everything is free except the exam.

| # | Step | Provider | Hours | Lessons | Folder |
|---:|---|---|---:|---:|---|
| 1 | [Claude Certified Architect – Foundations: Exam Guide](https://anthropic-partners.skilljar.com/claude-certified-architect-foundations-certification) | Anthropic | 1.5 | 1 | |
| 2 | [Building with the Claude API](https://anthropic.skilljar.com/claude-with-the-anthropic-api) | Anthropic Academy | 10 | 12 | |
| 3 | [AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) | Anthropic Academy | 4 | 6 | |
| 4 | [Claude 101](https://anthropic.skilljar.com/claude-101) | Anthropic Academy | 2.5 | 4 | |
| 5 | [Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) | Anthropic | 3 | 5 | |
| 6 | [Prompt Engineering & Structured Output with Claude](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (Domain 4) | Claude docs | 8 | 6 | |
| 7 | [Introduction to Model Context Protocol](https://anthropic.skilljar.com/introduction-to-model-context-protocol) | Anthropic Academy | 3 | 4 | |
| 8 | [Tool Design & MCP Integration](https://www.anthropic.com/research/writing-tools-for-agents) (Domain 2) | Anthropic, MCP spec, Claude Code docs | 4.5 | 5 | |
| 9 | [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) | Anthropic Academy | 4 | 5 | |
| 10 | [Introduction to agent skills](https://anthropic.skilljar.com/introduction-to-agent-skills) | Anthropic Academy | 1.5 | 6 | |
| 11 | [Introduction to subagents](https://anthropic.skilljar.com/introduction-to-subagents) | Anthropic Academy | 1.5 | 4 | |
| 12 | [Claude Code Configuration & Workflows](https://code.claude.com/docs/en/memory) (Domain 3) | Claude Code docs | 6 | 6 | |
| 13 | [Agentic Architecture with the Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) (Domain 1) | Agent SDK docs and demos | 10 | 11 | |
| 14 | [Context Management & Reliability](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) (Domain 5) | Anthropic, Claude docs | 4 | 4 | |
| 15 | Hands-on: the exam guide's four preparation exercises | Exam guide, section 8 | 15 | 20 | |
| 16 | Final review: sample questions and weak domains | Exam guide | 3 | 5 | |
| 17 | The exam | Pearson VUE | | | |

The *Folder* column is filled in as each step is done.

## Layout

```
NN-<step>/            one folder per step, numbered as in the path, added as I go
  notes.md            key ideas tied to the exam domains, gotchas, links
  *.ipynb, *.py       hands-on work, when the step has any
  outputs/            large outputs (gitignored)
exam/
  <domain>.md         revision sheet per exam domain, built up from the steps
  practice.md         sample-question scores and weak areas
```

## Notes

- [`CLAUDE.md`](CLAUDE.md) tells Claude Code how to help in this repo. I use it as a study partner.
- Notes and code here are my own work. Course material, quiz answers and the exam guide's sample questions are not copied into this repo.
- API keys stay out of the repo. Code reads `ANTHROPIC_API_KEY` from the environment.
