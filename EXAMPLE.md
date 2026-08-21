# Example: how the process ran on a real project

Project: a cross-platform planner (Flutter; iPad primary with Apple Pencil notes, iPhone, web) that mirrors an Outlook calendar via a published ICS feed now and Microsoft Graph later, with a self-hosted Docker backend. Solo developer, non-technical primary user. Everything below happened in planning mode, before a single line of application code.

## Day 1

**Round 1 — working-config review.** The developer listed 11 process rules. The council agreed on three changes that survived: "warn me when context is full" cannot fire reliably (the model can't see its own context meter), so the handoff file is written unconditionally after every task; "self-test every change" is empty without a runner, so it became a concrete test gate; and a one-line-per-decision log was added so the assistant stops re-asking settled questions.

**Round 2 — pre-plan questionnaire.** Five advisors produced ~65 questions, deduplicated to 30 across product, notes, sync, calendar, platforms, privacy, scope. The developer answered in one message.

**Round 3 — brief review.** The developer wrote the full brief (views, timetable, notes engines, theming, backend, admin, sharing, reference images). Eight advisors (five lenses + Flutter/PencilKit, backend/sync, privacy/end-user specialists), five reviewers, one chairman. Outcomes: a hard contradiction was found (native PencilKit is a must-have, but "edit ink on the laptop" is impossible because the drawing format is Apple-only) and resolved as a layered model; the technical verifier corrected three confident-but-wrong claims from advisors (no public stroke ID in PencilKit, eraser semantics, GDPR controller); TestFlight's 90-day build expiry and a possibly MDM-managed device were flagged as blockers nobody had considered.

**Round 4 — answers check.** The developer's answers were checked for consistency; research agents confirmed that TestFlight requires the paid developer program, that Flutter Windows cannot be built on a Mac, and the request-body limit of the chosen tunnel. A 12-item security baseline was produced for the chosen "open signup + link sharing + home server" setup.

## Day 2

**Planning docs written:** `product.md`, `data-model.md`, `sync-contract.md` (with 16 enumerated failure cases), `milestones.md` (P, M0–M8, each with a test gate).

**Round 5 — final review.** Six reviewers produced ~75 findings; the chairman deduplicated them into a verbatim fix list that was applied the same day. Blockers included: note identity must be the calendar UID, not a row id; the event unique key must include the source; conflicts must be resolved by server order, not client clocks; share tokens must not travel in URL paths; a `.home` LAN hostname cannot get a public TLS certificate; the PNG preview must be rendered from the canvas *and* the text layer.

**Round 6 — design council.** Four designers (editorial, product/system, motion/engineering, anti-generic critic) proposed directions; the chairman merged them into a single `design.md` with tokens, per-screen layouts, a motion table, theming algorithm, accessibility minimums, copy tone, and a compliance map against the banned-pattern list. The developer reviewed 14 taste decisions and amended six.

**Result:** 18 planning documents, 8 council transcripts, a 300-node knowledge graph, every decision answered and logged. `mode.md` flipped to build.

## What the process caught that a single chat would have missed

- An architecture that would have silently orphaned every user note on a calendar re-sync.
- Two confidently stated but nonexistent platform APIs.
- A distribution plan that would have made the app stop launching every 7 or 90 days.
- A LAN hostname choice that would have forced plaintext traffic or manual certificate installs.
- Five scope items that were actually a second product, re-phased instead of cut.
