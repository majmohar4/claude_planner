# process.md — working rules (project-agnostic)

## Session start (always, in order)
1. Read `mode.md` → obey mode gate.
2. Read `progress.md` → resume point.
3. Read `decisions.md` → never re-ask settled questions.
4. If docs/code changed since last graph: `/graphify . --update`; query graph before raw files.
5. Missing tools → `setup.md` §Bootstrap.

## Mode gate
`mode.md` holds the phase; only the user edits it.
- `planning` → NO application code, no spikes. Allowed writes: `*.md`, settings (`.claude/*.json`), tool/skill files. Code requests → spec in Markdown.
- Exit: planning deliverables exist (see planning-sequence.md) + user flips the file.

## Rules
1. **Terse chat, compact docs.** Chat in caveman (`/caveman full`). Docs as compact as possible while fully actionable by another AI; every instruction + why preserved. Code/commits/security warnings in normal prose.
2. **Knowledge graph.** `/graphify` on repo; rebuild on material change; read graph before raw files.
3. **Council for decisions.** `llm-council` for architecture/component/irreversible decisions, not UI nits. Transcripts → `council/`.
4. **Handoff.** `progress.md` updated at end of every completed task, unconditionally (Done / In progress / Next / Open questions / Last session date). When session is visibly long, end reply with `⚠️ Compact soon — progress.md is current.` Fresh session/account must resume from CLAUDE.md → progress.md → setup.md alone.
5. **Verify.** Every change self-tested per `testing.md`; if automated test impossible (device-only, live service) → ask user to check, naming exact edge cases.
6. **Ask, don't guess.** Unclear → one clarifying question first. Check `decisions.md` first. Execute instructions; concerns in one line, no lectures. User absent + choice reversible → decide, record, proceed.
7. **decisions.md.** One line per decision: `date · what · why · who`. Write on every user/council ruling. Supersede by appending, never silently editing.
8. **Secrets.** Repo private may hold secrets in ONE named file (`secrets.md`); never copy into council packets, graph exports, progress, or new files; strip before any publish. (If repo public: gitignored `.env` only.)
9. **setup.md** append-only: every change needing install/config, dated; §Bootstrap lists everything a new machine needs.
10. **testing.md** per-component: automated / manual-device / edge-cases; definition of done = automated green + manual items signed.
11. **debugging.md** append on real incidents: symptom · cause · check.
12. **Git.** Claude never runs `git commit`/`push`; suggests `! git ...` command text; no Co-Authored-By. (User preference — drop if not wanted.)
13. **Parallel agents.** Independent work → multiple subagents in one message. Build crew per task: builder · tester · edge-case tester · security reviewer · reviewer. No two agents edit the same file concurrently (worktrees); compact reports; main thread merges + updates progress/testing/debugging.
14. **Design gate.** All UI passes `design-rules.md` (banned patterns) + project `design.md` (spec). Tools: taste-skill, impeccable, image-to-code, Playwright screenshots, awesome-design-skills picks.
15. **Milestone gates.** No next milestone until gate passes (see planning-sequence.md).
