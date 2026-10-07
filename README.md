# claude_planner

A plan-before-you-code process for building apps with [Claude Code](https://claude.com/claude-code). It turns a vague idea into a reviewed, decision-complete plan (product, data model, sync/architecture contract, milestones with test gates, design spec) **before any application code exists**, and keeps every later session resumable from files alone.

It was extracted from a real project (a Flutter planner with Apple Pencil notes and Outlook sync) after the planning phase shipped; nothing here is theoretical.

## Why

- AI coding sessions lose context. Every decision lives in files (`decisions.md`, `progress.md`), so a fresh session or a different account resumes cold.
- Wrong early decisions are expensive. Irreversible choices (identity, data model, sync, security) are made deliberately, pressure-tested by a multi-agent "council", and logged with the reason.
- Plans drift. A `mode.md` gate physically forbids application code until the plan is complete and the human flips the switch.
- Quality needs gates. Every milestone ends with an automated + manual test gate; no gate, no next milestone.

## What's inside

| File | Purpose |
|---|---|
| `process.md` | The 21 working rules: mode gate, session-start order, handoff file, decisions log, verification, secrets, parallel agent crew, design gate, milestone gates, security + legal gates, permissions up front, disk discipline, purge, fresh context by default. |
| `orchestration.md` | Model + effort matrix (Opus 5.5 / Sonnet 5.5 / Haiku 4.5), brief template, agent reply contract, escalation, context hygiene (`/clear` at phase boundaries, delegate verbose reading). |
| `templates/.claude/agents/` | 8 subagents with `model:` + `effort:`: investigator, deployer (haiku) · builder, tester, edge-tester, reviewer (sonnet) · debugger, security-reviewer (opus). |
| `templates/.claude/settings.json` | Main model `opus`; per-model effort (Opus high for planning, set medium at build); context-warning hook. |
| `templates/.claude/hooks/context-warn.py` | Reads real token usage from the transcript; warns you and Claude at ~100k / ~160k tokens to `/clear` or `/compact`. |
| `templates/legal.md` | EU/GDPR legal checklist: privacy policy contents, ToS disclaimer + liability limits, cookies/consent, imprint, DPAs, rights flows, app-store privacy, accessibility, AI Act, `[lawyer]` flags. |
| `council-playbook.md` | How to run the six "LLM council" rounds (advisors → anonymized peer review → chairman) that review the config, question the brief, check the answers, and produce the final fix list and design spec. |
| `planning-sequence.md` | The ordered list of planning deliverables and the exit criterion for flipping to build mode. |
| `templates/` | Drop-in skeletons: `CLAUDE.md`, `mode.md`, `progress.md`, `decisions.md`, `open-risks.md`, `setup.md`, `testing.md`, `debugging.md`, `milestones.md`, `design-rules.md`, `launch-checklist.md`. |
| `EXAMPLE.md` | Walkthrough of the original project: what each round produced and what it caught. |

## Quick start

```bash
# in your new, empty repo
cp -r /path/to/claude_planner ./rules
cp -R rules/templates/. .     # includes .claude/agents + settings.json
# fill <PROJECT> in CLAUDE.md; leave mode.md = planning
claude
```

Then, in Claude Code:

1. `/init`-style setup is already done by `CLAUDE.md`. Tell Claude your working preferences and ask it to **council the working configuration** (round 1).
2. Ask the council **what you need to answer before planning** (round 2). Answer the questions.
3. Write your brief (features, platforms, references). Ask the council to **review the brief** (round 3) and answer its numbered decisions ("defaults" accepts the bracketed recommendations).
4. Let Claude write `product.md`, `data-model.md`, `sync-contract.md`, `milestones.md`, then run the **final review** (round 5) and **design council** (round 6).
5. Rebuild the knowledge graph, review, edit `mode.md` to `build`, then `/clear` and `/effort medium`. Milestone M0 starts; from here Claude writes briefs and dispatches the agent crew.

## Recommended Claude Code skills/plugins

Not required, but the playbook assumes them: `llm-council` (multi-advisor decisions), `graphify` (knowledge graph so sessions read fewer tokens), `caveman` (terse output), `superpowers` (brainstorm / debug / TDD process skills), and for UI work `taste-skill`, `impeccable`, `image-to-code-skill`, Playwright CLI, and style packs from [awesome-design-skills](https://github.com/bergside/awesome-design-skills).

## The mode gate

`mode.md` contains one word. While it says `planning`, Claude may only write Markdown, settings, and tool/skill files. Code requests are answered with specs. Only the human edits this file. This single rule is what keeps "let me just prototype it" from eating the plan.

## The handoff file

`progress.md` is rewritten at the end of every completed task, unconditionally. It has four sections: Done, In progress, Next, Open questions. Combined with `CLAUDE.md` (rules + doc map), `decisions.md` (why), and `setup.md` (what to install), a new session needs no chat history.

## Models, effort, context

Opus 5.5 runs the main thread in every phase: it plans, writes briefs, and merges results. Cheaper agents do the execution, and each agent file pins its own model and effort. The principle is that quality comes from the brief, not the model: a Sonnet builder with an exact brief beats an Opus builder with a vague one.

Anything whose result is needed but whose reading is not (searches, logs, test output, research, council rounds) goes to a subagent. Only a ≤12-line stub returns to the main thread; the full report goes to `docs/gates/`. At every phase boundary, and after any task whose follow-up doesn't need the current context, Claude updates `progress.md` and tells you to `/clear` with a paste-ready prompt for the next step. Unrelated requests in an already-long session get that prompt instead of being started on top of stale context. Model and effort changes happen only right after `/clear`, because a mid-session change invalidates the prompt cache. See `orchestration.md`.

Security and legal are gates, not afterthoughts: a per-diff `security-reviewer` agent, Cloudflare's official [`security-audit`](https://github.com/cloudflare/security-audit-skill) skill before any public build, and `legal.md` (privacy, ToS disclaimer, cookies, GDPR, imprint, store forms) worked through from planning on (process rules 16/17).

Permissions are asked once at task start (agents running in the background can't stop to ask), tests and builds are the minimum that proves a change (full suite and release builds only at milestone gates), and regenerable output is purged at task and milestone end (process rules 18–20). `settings.json` pre-allows read-only git/inspection commands and denies `git commit`/`push`/`reset --hard`/`clean` plus reading `secrets.md`/`.env`.

Claude pushes back once on a bad or risky idea: a verdict, why, the cost if it's wrong, and a better option. If you decide otherwise, the override is logged in `decisions.md` and Claude does it fully, without asking again in this session or later ones (process rules 6a/6b).

## Councils in one paragraph

A council is five or more sub-agents, each arguing from a fixed lens (Contrarian, First Principles, Expansionist, Outsider, Executor, plus domain specialists), answering the same framed question in parallel. Their answers are anonymized and peer-reviewed by a second set of agents, including a technical verifier whose only job is to find claims that are wrong. A chairman synthesizes agreement, clashes, blind spots, and a recommendation. Human rulings override the council and are logged. In the original project the verifier caught several incorrect API claims before they reached the plan.

## Test gates

`milestones.md` defines P (planning) and M0…Mn. Each milestone lists what to build and a gate: automated tests that must be green, manual checks the human signs off on a real device, and edge cases from the architecture contract's enumerated failure list. Features land last; the core path ships first.

## Adapting

- Solo developer who commits personally: keep rule 12 (Claude never runs `git commit`). Otherwise delete it.
- Public repo: replace the `secrets.md` convention with a gitignored `.env`.
- No UI: drop rule 14 and the design templates.
- Smaller projects: run council rounds 1, 3 and 5 only.

## License

MIT. See `LICENSE`.
