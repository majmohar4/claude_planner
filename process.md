# process.md — working rules (project-agnostic)

## Session start (always, in order)
1. Read `mode.md` → obey mode gate.
2. Read `progress.md` → resume point.
3. Read `decisions.md` → never re-ask settled questions.
4. If docs/code changed since last graph: `/graphify . --update`; query graph before raw files.
5. Missing tools → `setup.md` §Bootstrap.
6. Model/effort for the phase per `orchestration.md` §1 (switch only right after `/clear`).

## Mode gate
`mode.md` holds the phase; only the user edits it.
- `planning` → NO application code, no spikes. Allowed writes: `*.md`, settings (`.claude/*.json`), tool/skill files. Code requests → spec in Markdown.
- Exit: planning deliverables exist (see planning-sequence.md) + user flips the file.

## Rules
1. **Terse chat, compact docs.** Caveman mode always on (`/caveman full`; plugin in setup.md) for main thread AND agent replies. Docs as compact as possible while fully actionable by another AI; every instruction + why preserved. Code/commits/security warnings/irreversible confirmations in normal prose.
1a. **Output discipline.** Chat is for the user to read, not a worklog. Tool calls run silent: no narration before/between them ("Now I'll…", "Let me check…"), no restating tool output. Text only for: a question/decision the user must make, a warning (pushback, context, security), or the end-of-task summary. Summary = what changed · what's verified vs not · what user must do next; skip what the user already knows. Brevity never drops substance: findings, risks, and numbers stay.
2. **Knowledge graph.** `/graphify` on repo; rebuild on material change; read graph before raw files.
3. **Council for decisions.** `llm-council` for architecture/component/irreversible decisions, not UI nits. Run as subagents (sonnet advisors, opus verifier + chairman); transcripts → `council/`, main thread reads only the verdict.
4. **Handoff.** `progress.md` updated at end of every completed task, unconditionally (Done / In progress / Next / Open questions / Last session date). Phase done → end reply with `🧹 Phase done — progress.md current. /clear, then: <next prompt>`; long mid-phase → suggest `/compact <focus>` (orchestration.md §5). Fresh session/account must resume from CLAUDE.md → progress.md → setup.md alone.
5. **Verify.** Every change self-tested per `testing.md`; if automated test impossible (device-only, live service) → ask user to check, naming exact edge cases.
6. **Ask, don't guess.** Unclear → one clarifying question first. Check `decisions.md` first. User absent + choice reversible → decide, record, proceed.
6a. **Push back, once.** Bad/risky idea (from user, brief, or another agent) → say so before acting: verdict (risky | bad) · why in one line · cost if wrong · better alternative. Weak plan → say which part and why; agreeing to be agreeable is a failure. Big/irreversible → offer council.
6b. **User overrides → comply, never re-ask.** After one warning the user's call is final: log `date · <choice> · override of: <warning> · user` in decisions.md, execute fully and well (no sandbagging, no reduced effort), never re-raise it in this or later sessions, never pass it to agents as a concern. Exception: new evidence the user hasn't seen (e.g. data loss in a test) → state it once as new fact.
7. **decisions.md.** One line per decision: `date · what · why · who`. Write on every user/council ruling. Supersede by appending, never silently editing.
8. **Secrets.** Repo private may hold secrets in ONE named file (`secrets.md`); never copy into council packets, graph exports, progress, or new files; strip before any publish. (If repo public: gitignored `.env` only.)
9. **setup.md** append-only: every change needing install/config, dated; §Bootstrap lists everything a new machine needs.
10. **testing.md** per-component: automated / manual-device / edge-cases; definition of done = automated green + manual items signed.
11. **debugging.md** append on real incidents: symptom · cause · check.
12. **Git.** Claude never runs `git commit`/`push`; suggests `! git ...` command text; no Co-Authored-By. (User preference — drop if not wanted.)
13. **Agent crew + context.** Follow `orchestration.md`: Opus main thread plans + writes briefs; `.claude/agents/` execute at the matrix's model/effort. Delegate anything whose reading isn't needed in main context; independent agents in one message; disjoint file ownership (else worktrees); ≤12-line stubs, full reports in `docs/gates/`; main merges + updates progress/testing/debugging. Agents never commit.
14. **Design gate.** All UI passes `design-rules.md` (banned patterns) + project `design.md` (spec). Tools: taste-skill, impeccable, image-to-code, Playwright screenshots, awesome-design-skills picks.
15. **Milestone gates.** No next milestone until gate passes (see planning-sequence.md).
16. **Security gate.** Per diff: `security-reviewer` agent on auth/input/secrets/data changes. Whole app: Cloudflare `security-audit` skill (setup.md) before first public build, before launch, after major auth/data/infra changes — run in a sandbox on a clean checkout with NO secrets (`secrets.md`/`.env` removed), network isolated. Heavy (many parallel agents): run as its own session, `/clear` after; findings → fix briefs; confirmed criticals block the gate.
17. **Legal gate.** Every app ships with `legal.md` worked through: Privacy Policy, ToS with warranty disclaimer + liability limits (within consumer-law limits), Cookie Policy + consent banner, imprint, OSS notices, GDPR rights flows (export/delete), DPAs, app-store privacy forms. Decided in planning, built in milestones, all ticked before any public build. Claude flags `[lawyer]` items; never presents generated legal text as legal advice.
18. **Permissions up front.** At task start (before any work, before dispatching agents) list every permission the task will need — installs, network, writes outside repo, deletes, docker, device/simulator, long builds — and ask ONCE in one message; approved recurring commands → `.claude/settings.local.json` allow list (or `/permissions`). Background agents can't stop to ask: anything a brief needs must be pre-approved, else the agent reports BLOCKED. Mid-task new need → batch all remaining ones into one question, never drip.
19. **Disk + build discipline.** Test/build the minimum that proves the change: touched tests only (agents), affected package/target only, debug/incremental builds, no `clean` between iterations (kills caches). Full suite + release build only at milestone gates. Never loop rebuilds to "see if it passes"; second failure → stop, diagnose. All generated output (builds, coverage, screenshots, logs, traces) in gitignored dirs listed in CLAUDE.md §Commands.
20. **Purge when done.** Each task end: delete scratch files, temp logs, screenshots, worktrees (`git worktree prune`) it created. Milestone gate end: run CLAUDE.md §Commands `purge` (release artifacts, coverage, old screenshots, dangling docker images/containers), report `du -sh` before/after. Delete only regenerable, gitignored output — list it first; never tracked files, never `secrets.md`/`.env`, never anything unknown.
21. **Fresh context by default.** Every end-of-task summary judges: does the next step need this session's context? No → end with `🧹 Next step doesn't need this context — /clear (or new session), then: <paste-ready prompt incl. files to read>`. Yes → say `Continue here (needs: <what>)`. New user request unrelated to current context: context above soft warning → don't start; give the paste-ready prompt + `/clear`; below → do it, then suggest `/clear`. Paste-ready prompt must be self-contained (points to progress.md/brief, not to chat). Reason: stale context costs tokens every turn and dilutes attention; cache only pays off when the next turn reuses it.
