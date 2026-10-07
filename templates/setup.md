# setup.md — installs & config. Append-only, dated.

## Bootstrap new session / machine (in order)
1. Read CLAUDE.md → progress.md → decisions.md.
2. Claude Code plugins/skills expected: caveman (then `/caveman full`; cavecrew agents optional), superpowers, graphify, llm-council, taste-skill, impeccable, image-to-code-skill (+ project-specific).
3. Design tools at build start: `npx impeccable install`; `npx typeui.sh pull <slug>` (awesome-design-skills); Playwright CLI.
4. Toolchain (fill when chosen): 
5. Agents + model/effort: `.claude/agents/*.md` + `.claude/settings.json` from rules/templates (orchestration.md). Non-Anthropic provider → pin `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`.
6. Security audit skill (official Cloudflare, MIT): `npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit`. Read its SKILL.md + scripts before first run; needs Node; run sandboxed, clean checkout, no secrets. Also: owasp-security skill for security-reviewer agent.
7. Explain/visualize tools (process 22; install on first use, ask first):
   - CodeWiki (MIT, Python 3.12+, git, Node): `pip install git+https://github.com/FSoft-AI4Code/CodeWiki.git` · `codewiki config set --provider <provider> --api-key <key>` · `codewiki generate` / `--update`. Also `codewiki mcp`.
   - visualize (MIT, Claude Code plugin): `claude plugin marketplace add careerhackeralex/visualize` · `claude plugin install visualize@careerhackeralex`. Trigger: "visualize …", "make a flowchart/dashboard/infographic of …".
   - Verify commands against the repos' READMEs before first install (researched secondhand 2026-10).
8. Context + code tools (user scope, once per machine):
   - Context7 (current library docs): `claude plugin install context7@claude-plugins-official`
   - hookify (plain-English → hooks): `claude plugin install hookify@claude-plugins-official`
   - LSP: `claude plugin install typescript-lsp@claude-plugins-official` · `pyright-lsp@…` · `swift-lsp@…` (+ binaries: `npm i -g typescript-language-server typescript pyright`; npm global bin on PATH; sourcekit-lsp ships with Xcode). Dart/Flutter → dart-flutter MCP.
   - ccusage (token/cost history, local): `npx -y ccusage@latest daily` · `npx ccusage blocks --live`
   - context-mode (TRIAL, ELv2, local): `claude plugin marketplace add mksglu/context-mode` · `claude plugin install context-mode@context-mode` · check `/context-mode:ctx-doctor`. Keep only if ccusage shows savings after a week.
9. Secrets: `secrets.md` (private repo) or `.env` (gitignored).

## Log
- <date> · 
