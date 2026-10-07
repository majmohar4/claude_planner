# CLAUDE.md

Guidance for Claude Code in this repo. Compact by design: every line is an instruction or a pointer.

## Session start (always, in this order)
1. Read `mode.md` → obey mode gate. 2. Read `progress.md`. 3. Read `decisions.md`. 4. Docs changed → `/graphify . --update`; query graph before raw files. 5. Missing tools → `setup.md` §Bootstrap.

## Mode gate
`mode.md` = phase; only user edits. `planning` → no application code, no spikes; only `*.md`, settings, tool files. Exit: planning deliverables exist + user flips file.

## Working rules
See `rules/process.md` (rules 1–21). Summary: terse chat + compact docs · graphify · council for decisions · progress.md every task · verify per testing.md · ask-don't-guess + decisions.md · secrets in one file · setup/testing/debugging append-only · user commits · agent crew · design gate · milestone gates · security gate · legal gate · permissions up front · disk discipline · purge · fresh context by default.

## Orchestration (read `rules/orchestration.md` before dispatching any agent)
- Main thread = Opus: plans, writes briefs (`docs/gates/<task>/brief-<n>.md`), merges. Agents in `.claude/agents/` execute: investigator · deployer (haiku) · builder · tester · edge-tester · reviewer (sonnet) · debugger · security-reviewer (opus).
- **Delegate when the result is needed but the reading is not** (multi-file search, logs, test output, web/doc fetch, research, council). Only a ≤12-line stub returns. Use `investigator`, not built-in Explore.
- Independent agents in ONE message. Disjoint file ownership. Agents never commit, never dispatch agents.
- Unknown bug cause → debugger first; builders only get diagnosed briefs.
- Phase done (council round, milestone gate, mode flip, topic switch) → progress.md current → end reply with `🧹 Phase done — progress.md current. /clear, then: <next prompt>`. Model/effort changes only right after `/clear` (cache).

## Output
Caveman full (main + agents). Tool calls silent: no narration between steps. Chat text only for questions, warnings, end-of-task summary (changed · verified/not · user's next step). Code/commits/security in normal prose (process 1/1a).

## Pushback + overrides
Bad/risky idea → one-line verdict + why + cost if wrong + better option, before acting. User decides otherwise → log `override` in decisions.md, do it fully, never re-ask (process 6a/6b).

## Security + legal gates
Per diff: security-reviewer agent. Whole app: Cloudflare `security-audit` skill before first public build + launch (sandbox, no secrets). Every app: `legal.md` (privacy, ToS disclaimer, cookies/consent, GDPR flows, imprint, store forms) ticked before public build (process 16/17).

## Context warnings
`.claude/hooks/context-warn.py` warns at ~100k (soft) / ~160k (hard) main-context tokens (env `CTX_SOFT`/`CTX_HARD`). Soft → delegate all reading, `/clear` at next phase end. Hard → make progress.md current, finish current step, tell user `/clear` (or `/compact <focus>` mid-task). Built-in auto-compact stays on as last-resort safety net only.

## Compact instructions
On `/compact` keep: current task + brief path, files being edited, unresolved errors, user rulings not yet in decisions.md. Drop: file dumps, search results, agent transcripts, resolved errors.

## What <PROJECT> is
<one paragraph>

## Doc map (root)
- `mode.md` · `progress.md` · `decisions.md` · `open-risks.md`
- `brief.md` · `product.md` · `data-model.md` · `sync-contract.md` · `milestones.md` · `launch-checklist.md`
- `setup.md` · `testing.md` · `debugging.md` · `design-rules.md` · `design.md` · `legal.md` · `secrets.md`
- `council/` transcripts · `docs/gates/` briefs + agent reports · `rules/` reusable process

## Commands (fill at M0; agents copy into briefs; also add to `.claude/settings.local.json` allow list)
- test (single file): `<cmd> <file>` · test (full, gates only): `<cmd>`
- build (debug/incremental): `<cmd>` · build (release, gates only): `<cmd>`
- output dirs (gitignored): `build/ coverage/ screenshots/ logs/ …`
- purge (milestone end): `<cmd removing release artifacts, coverage, old screenshots, dangling docker>`
- No tooling yet → never guess commands.

## Fresh context (process 21)
Every summary ends with either `🧹 Next step doesn't need this context — /clear (or new session), then: <self-contained prompt>` or `Continue here (needs: <what>)`. Unrelated new request + context above soft warning → give the prompt + `/clear` instead of starting.

## Permissions, disk, purge (process 18–20)
Task start: list all needed permissions (installs, network, deletes, docker, long builds) → ask ONCE → approved recurring ones into settings.local.json. Agents can't ask mid-run → pre-approve. Minimum test/build per change; full suite + release only at gates; no `clean` between iterations. Task end: purge own scratch/worktrees/screenshots. Gate end: `purge` + `du -sh` before/after; only regenerable gitignored output.
