# CLAUDE.md

Guidance for Claude Code in this repo. Compact by design: every line is an instruction or a pointer.

## Session start (always, in this order)
1. Read `mode.md` → obey mode gate. 2. Read `progress.md`. 3. Read `decisions.md`. 4. Docs changed → `/graphify . --update`; query graph before raw files. 5. Missing tools → `setup.md` §Bootstrap.

## Mode gate
`mode.md` = phase; only user edits. `planning` → no application code, no spikes; only `*.md`, settings, tool files. Exit: planning deliverables exist + user flips file.

## Working rules
See `rules/process.md` (rules 1–15). Summary: terse chat + compact docs · graphify · council for decisions · progress.md every task · verify per testing.md · ask-don't-guess + decisions.md · secrets in one file · setup/testing/debugging append-only · user commits · agent crew · design gate · milestone gates.

## Orchestration (read `rules/orchestration.md` before dispatching any agent)
- Main thread = Opus: plans, writes briefs (`docs/gates/<task>/brief-<n>.md`), merges. Agents in `.claude/agents/` execute: investigator · deployer (haiku) · builder · tester · edge-tester · reviewer (sonnet) · debugger · security-reviewer (opus).
- **Delegate when the result is needed but the reading is not** (multi-file search, logs, test output, web/doc fetch, research, council). Only a ≤12-line stub returns. Use `investigator`, not built-in Explore.
- Independent agents in ONE message. Disjoint file ownership. Agents never commit, never dispatch agents.
- Unknown bug cause → debugger first; builders only get diagnosed briefs.
- Phase done (council round, milestone gate, mode flip, topic switch) → progress.md current → end reply with `🧹 Phase done — progress.md current. /clear, then: <next prompt>`. Model/effort changes only right after `/clear` (cache).

## Compact instructions
On `/compact` keep: current task + brief path, files being edited, unresolved errors, user rulings not yet in decisions.md. Drop: file dumps, search results, agent transcripts, resolved errors.

## What <PROJECT> is
<one paragraph>

## Doc map (root)
- `mode.md` · `progress.md` · `decisions.md` · `open-risks.md`
- `brief.md` · `product.md` · `data-model.md` · `sync-contract.md` · `milestones.md` · `launch-checklist.md`
- `setup.md` · `testing.md` · `debugging.md` · `design-rules.md` · `design.md` · `secrets.md`
- `council/` transcripts · `docs/gates/` briefs + agent reports · `rules/` reusable process

## Commands
- No build/lint/test tooling exists yet → add real commands here when code exists (agents copy them into briefs); never guess.
