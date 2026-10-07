# setup.md — installs & config. Append-only, dated.

## Bootstrap new session / machine (in order)
1. Read CLAUDE.md → progress.md → decisions.md.
2. Claude Code plugins/skills expected: caveman (then `/caveman full`; cavecrew agents optional), superpowers, graphify, llm-council, taste-skill, impeccable, image-to-code-skill (+ project-specific).
3. Design tools at build start: `npx impeccable install`; `npx typeui.sh pull <slug>` (awesome-design-skills); Playwright CLI.
4. Toolchain (fill when chosen): 
5. Agents + model/effort: `.claude/agents/*.md` + `.claude/settings.json` from rules/templates (orchestration.md). Non-Anthropic provider → pin `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`.
6. Security audit skill (official Cloudflare, MIT): `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit`. Read its SKILL.md + scripts before first run; needs Node; run sandboxed, clean checkout, no secrets. Also: owasp-security skill for security-reviewer agent.
7. Secrets: `secrets.md` (private repo) or `.env` (gitignored).

## Log
- <date> · 
