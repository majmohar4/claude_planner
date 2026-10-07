# council-playbook.md — llm-council rounds that worked

Format per round: framed packet (secrets redacted) → N advisors in parallel (one message) → anonymized peer review (3–5 reviewers incl. a technical verifier and a "user advocate") → chairman synthesis → save `council/<date>-<topic>.md` (+ `-VERDICT.md`) → decisions into `decisions.md` → questions to user with recommended defaults in brackets so they can answer "defaults".

Rounds, in order:
1. **Working-config review** — pressure-test the process itself (tools, handoff, testing). 5 core advisors (Contrarian, First Principles, Expansionist, Outsider, Executor).
2. **Pre-plan questionnaire** — "what must the developer answer before planning?" 5 advisors → dedup into grouped one-line questions, ★ top 3. Skip peer review.
3. **Brief review** — after user writes the full brief: CLARIFY / ADD / PROBLEMS / KILL-OR-SHRINK (pre-mortem: "it's 6 months later and this failed — why?"; is any part not worth building, or a second product?). 5 core + specialists (platform/tech, backend/sync/security, privacy/end-user). Peer review 5 incl. technical verifier (catches wrong API claims). Chairman outputs ≤30 numbered decisions with defaults + milestone skeleton.
4. **Answers check** — verify answers actually answer, contradictions, new questions, research unknowns (WebSearch agent), security baseline for the chosen setup.
5. **Final review** — all planning docs: contradictions, gaps, infeasibility; chairman emits a verbatim FIX LIST applied to docs the same day.
6. **Design council** — 3–4 designers (editorial, product/system, motion/engineering, anti-generic critic) → chairman writes `design.md`; user reviews 10–15 taste calls.

Models: advisors + peer reviewers = sonnet · high; technical verifier + chairman = opus · high (fable · xhigh only for an irreversible call where opus verdicts conflict). Pass `model` per Agent call. Each agent writes its answer to `council/<date>-<topic>/<role>.md` and replies ≤10 lines; chairman reads files, main thread reads only the VERDICT. Round done → `/clear` (process rule 4).

Rules: advisors lean fully into their lens; consensus "looks good" with no problems found = round failed, re-run Contrarian with "find the 3 biggest flaws"; reviewers anonymized; chairman may side with minority; user rulings override council and are logged; every technical correction becomes a `decisions.md` fact line.
