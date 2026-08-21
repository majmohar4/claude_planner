# CLAUDE.md

Guidance for Claude Code in this repo. Compact by design: every line is an instruction or a pointer.

## Session start (always, in this order)
1. Read `mode.md` → obey mode gate. 2. Read `progress.md`. 3. Read `decisions.md`. 4. Docs changed → `/graphify . --update`; query graph before raw files. 5. Missing tools → `setup.md` §Bootstrap.

## Mode gate
`mode.md` = phase; only user edits. `planning` → no application code, no spikes; only `*.md`, settings, tool files. Exit: planning deliverables exist + user flips file.

## Working rules
See `rules/process.md` (rules 1–15). Summary: terse chat + compact docs · graphify · council for decisions · progress.md every task · verify per testing.md · ask-don't-guess + decisions.md · secrets in one file · setup/testing/debugging append-only · user commits · parallel agent crew · design gate · milestone gates.

## What <PROJECT> is
<one paragraph>

## Doc map (root)
- `mode.md` · `progress.md` · `decisions.md` · `open-risks.md`
- `brief.md` · `product.md` · `data-model.md` · `sync-contract.md` · `milestones.md` · `launch-checklist.md`
- `setup.md` · `testing.md` · `debugging.md` · `design-rules.md` · `design.md` · `secrets.md`
- `council/` transcripts · `rules/` reusable process

## Cautions
- No build/lint/test tooling exists yet → add real commands here when code exists; never guess.
