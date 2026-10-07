# orchestration.md — models, effort, agents, context (project-agnostic)

Principle: **quality is protected by the brief, not the model.** A Sonnet builder with an exact brief beats an Opus builder with a vague one. Opus (main thread) plans, writes briefs, merges; cheaper agents execute.

## 1. Model + effort matrix
Pick the lowest tier that passes "wrong is cheap?". Effort = how much the model spends (text, tool calls, thinking); raise effort when it skipped files/tests/bailed, change model when the problem is genuinely hard.

| Role | Model | Effort | Use for | Never for |
|---|---|---|---|---|
| Main thread | opus (Opus 5.5) | high in planning · medium in build | plan, brief, merge, talk to user | bulk reading, test runs, log dumps |
| investigator | haiku | low | locate: where/who calls/list uses/grep logs | judgement, fixes |
| deployer | haiku | low | run ONE exact recipe, verify each step | improvising, git |
| builder · tester | sonnet | medium | one leaf from a brief; tests to a spec | undiagnosed bugs ("find and fix") |
| edge-tester · reviewer | sonnet | high | failure hunting; diff review | — |
| reviewer (risky diff) | opus via `model` param | high | auth, data model/migrations, sync, money, deletes | — |
| debugger · security-reviewer | opus | high | unknown root cause; security review | routine edits |
| Council advisors | sonnet | high | lens answers, peer review | — |
| Council verifier + chairman | opus | high | fact-check claims, synthesis | — |
| Whole-app security audit | Cloudflare `security-audit` skill (own session) | — | pre-release audit, sandboxed | per-diff review (use security-reviewer) |
| Escalation ceiling | fable | xhigh | Opus at high failed twice on a hard problem | default use (cost) |

Rules:
- Escalate one tier (effort first, then model) when an agent fails its gate twice or replies NEEDS_CONTEXT/unclear. Never downgrade mid-flight.
- Agent tool `model` param overrides the agent file's `model:`; frontmatter `effort:` overrides session effort.
- Use `investigator` instead of built-in `Explore` (Explore inherits the main model = Opus cost).
- `xhigh`/`max` only where a real failure showed it helps; `max` overthinks and costs much more for small gains.
- `ultrathink` in a prompt = deeper reasoning for one turn; use it for a single hard call instead of raising session effort.
- Switching model or effort mid-session invalidates the prompt cache → switch only right after `/clear` (phase boundary).

## 2. Flow (build mode)
0. Main plans. Unknown root cause → `debugger` first; never send a builder to "find and fix".
1. Preflight (process 18): collect every permission all leaves need, ask user ONCE, add approved commands to `.claude/settings.local.json`. Briefs list exact allowed commands.
2. Main writes one brief per leaf (§3) → `docs/gates/<task>/brief-<n>.md`. Leaves own **disjoint files**.
3. Dispatch all independent leaves in ONE message; same-file leaves run sequentially (or worktrees).
4. Each agent writes full report → `docs/gates/<task>/report-<n>.md`, replies with stub (§4).
5. Main merges: reads stubs (not code dumps), spot-checks risky diffs, runs touched tests once → `reviewer` (+ `security-reviewer` if auth/input/secrets) → 🔴/🟡 findings = fix round via new brief; 🟢 batched for one final pass.
6. Gate passes → update progress.md/testing.md/debugging.md → tell user to `/clear` (§5).

## 3. Brief template (≤40 lines, plan-only: no code beyond signatures)
```
TASK:   one sentence, outcome not activity
MODEL:  <agent> · <model> · <effort>
OWNS:   files this leaf may edit (others → STOP, report why)
KNOWN:  facts already established (root cause file:line, decisions.md lines, invariants).
        Never git stash/checkout/reset/restore/commit/push/stage.
DO:     numbered steps
GATES:  claim | CHECK (runnable cmd) | EXPECT (exact output)   — bug: first gate = RED test failing on old code
TESTS:  exact test files to run (not whole suite); build = affected target, debug, no clean
PERMS:  pre-approved commands for this leaf (anything else → BLOCKED, don't attempt)
PURGE:  temp files/screenshots/worktrees this leaf must delete before reporting
REPORT: docs/gates/<task>/report-<n>.md + stub
CHECKLIST: <paste project pre-review checklist so first pass passes review>
```
User overrides (decisions.md lines tagged `override`) go into KNOWN as settled — agents implement them, never re-flag them.
Briefs contradicting code/spec in a behaviour-changing way → agent stops with NEEDS_CONTEXT, never guesses.

## 4. Agent reply contract
Full report to file; reply ≤12 lines:
`Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT` · files changed · one-line test result (re-measured, not remembered) · concerns · report path.
No narration of files read; caveman-terse. Subagents never dispatch subagents.
Pushback: an agent that thinks the brief's approach is bad (not just different) still stops only for broken invariants/data loss (→ NEEDS_CONTEXT); otherwise implements and adds one line under concerns: `approach risk: <why> · cost if wrong · alternative`. Main thread surfaces it to the user once.

## 5. Context hygiene (main thread + agents)
**Delegate when the result is needed but the reading is not:** sweeps of >3 files, logs, test/build output, web/doc fetches, research, council rounds, conflict scans. Only the stub returns.
**Stay inline when:** iterating with the user, editing files already in context, one-file lookups where path is known, quick edits.

Main thread:
- Silent tool calls: no narration between steps; chat text only for questions, warnings, final summary (process 1a).
- Summaries, not dumps: `wc -l`, `grep -c`, `| tail -20`, `sed -n 'a,bp'`; never cat big files to "look".
- Read reports, not diffs; spot-check only risky hunks.
- **Phase boundary = `/clear`**: after a council round, a milestone gate, a mode flip, or switching to unrelated work. First make progress.md current, then end the reply with:
  `🧹 Phase done — progress.md current. /clear, then: <exact next prompt>` (add `/model …` or `/effort …` line if next phase needs it).
- Claude cannot run `/clear`/`/compact` or see its own context meter → `.claude/hooks/context-warn.py` reads real usage from the transcript and warns user + Claude at soft (~100k) / hard (~160k). On hard warning mid-phase: progress.md current, suggest `/compact <focus>` (focus = current task + open files). Prefer `/clear` (free) over `/compact` (costs a large request). Built-in auto-compact = last-resort only (fires late, summary loses detail).
- One milestone per session.
- Not only phase ends: every summary says `/clear` + paste-ready prompt when the next step doesn't reuse this context, else `Continue here (needs: …)` (process 21). Cache helps only when reused; stale context taxes every turn.

Subagents:
- One task per agent; its context dies with it. Continue the same agent (SendMessage) only for the same task (e.g. fix round on its own leaf); new task → new agent.
- Brief carries KNOWN facts so agents don't re-discover them. Targeted `grep -n`/`sed -n` ranges only; no repo sweeps; run only touched tests.
- Oversized input (big plan, many files) → split across agents writing to files; main reads the merged summary.

## 6. Bug-hunt pipeline
symptom (user's words, no guessing) → known? (`git log --oneline | grep`, debugging.md) → locate (investigator) → root cause by evidence (log line, DB row, failing test), not plausibility; two refuted hypotheses → bisect → RED test → fix via brief (builder) → reviewer. Green suite ≠ correct: check against the invariants in the architecture doc.

## 7. Settings
`.claude/settings.json` (template): main model `opus`, per-model effort via `modelSettings` (top-level `effortLevel` does not apply to Opus 5.5+). Planning → build flip: `/clear`, then `/effort medium`. Per-launch override: `claude --effort high`; env `CLAUDE_CODE_EFFORT_LEVEL` beats everything (avoid). Provider ≠ Anthropic API: aliases may resolve to older models → pin `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL`.
