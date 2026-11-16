# Domain 3: Claude Code Configuration & Workflows (20%)

Configuring Claude Code for a project and a team. Points are tagged with the step and lesson they come from; steps 9–12 cover this domain in depth.

## Memory and setup

- Claude Code runs in the terminal: it reads the project, runs commands and edits files, asking for permission along the way. (2.10)
- `CLAUDE.md` is project memory: how the project works and the rules to follow, loaded at the start of each session. `/init` drafts one from the codebase; `/memory` opens the files. (2.10)
- Four levels, **combined** from broadest to most specific (not overridden): managed (organisation-wide), user (`~/.claude/CLAUDE.md`), project (`./CLAUDE.md` or `./.claude/CLAUDE.md`, committed) and local (`CLAUDE.local.md`, personal). Files in parent folders load at launch; files in subfolders load when Claude works there. `@path` imports nest up to four levels. `.claude/rules/` files with `paths:` load only for matching files. (2.10)
- CLAUDE.md is context, not enforcement.

## Permissions and settings

- Rules are checked **deny → ask → allow**; the first match wins, and a deny in any settings file wins. Examples: `Bash(npm run *)`, `Read(./.env)`, `mcp__docs__*`. (2.10)
- Settings precedence: managed > command-line (`--settings`) > `.claude/settings.local.json` (personal) > `.claude/settings.json` (team, committed) > `~/.claude/settings.json` (user). List settings such as `permissions.allow` merge across files. (2.10)
- Permission modes include default (ask), acceptEdits, plan, auto, dontAsk and bypassPermissions. (2.10)
- A rule that must always hold (never run migrations, never read `.env`): a deny rule or a PreToolUse hook, not stronger wording in CLAUDE.md. (2.10)

## MCP servers in Claude Code

- Add a server with `claude mcp add [--scope] [--env] <name> -- <command> [args]` (or `--transport http` for remote servers); `claude mcp list/get/remove`, and `/mcp` inside a session. (2.10)
- Three scopes: **local** (default: you, this project), **project** (a `.mcp.json` committed to the repo, shared with the team; each person approves it on first use) and **user** (you, every project). On a name clash: local > project > user. (2.10)
- Credentials never go in `.mcp.json`: use `${VAR}` (or `${VAR:-default}`) in `command`, `args`, `env`, `url` and `headers`; each machine supplies its own value. Personal servers belong in user scope, not in the repo. (2.10)
- In a session, MCP tools are named `mcp__<server>__<tool>`, resources are attached with `@server:uri`, and server prompts appear as slash commands (`/mcp__<server>__<prompt>`). Large tool results trigger a warning (10k tokens) and are cut at 25k by default (`MAX_MCP_OUTPUT_TOKENS`). (2.10)

## Scenario patterns

- "The whole team needs the same server, each with a personal token": project scope, `.mcp.json` in the repo, secrets as `${VAR}`.
- "Only I use this server, across projects": user scope.
- "Claude ignored a rule in CLAUDE.md": enforce it with a deny rule or a hook.
- Subagents: the exam guide's `Task` tool is `Agent` in current Claude Code.
