# planning-sequence.md — what planning produces before code

1. `brief.md` — user's raw brief verbatim-compact, incl. descriptions of every reference image (images vanish from future sessions).
2. Council rounds 1–2 (council-playbook.md).
3. `product.md` — one sentence · users · day-one story · views/features · non-negotiables · not-in-v1 · "v1 works" test sentence.
4. `data-model.md` — entities, identity rules, storage, caps, sync state, conflicts, migrations, backup.
5. `sync-contract.md` (or `architecture.md`) — provider interfaces, protocol, client states + copy, enumerated failure cases (each tested at a gate), security baseline.
6. `milestones.md` — P, M0 toolchain, M1…Mn; each: Build list · Gate (automated + manual + edge list). Core first, features last, ≤2 weeks each; feature flags in one codebase.
7. `legal.md` — audience/data/analytics decisions made; data inventory (field · purpose · basis · retention · processor) in data-model.md; legal docs + consent + rights flows placed into milestones; `[lawyer]` items listed in open-risks.md.
8. `design-rules.md` (bans) + `design.md` (spec via design council) + `launch-checklist.md`.
9. Council rounds 3–6; fixes applied; `open-risks.md` left only with build-phase verifications.
10. `/graphify . --update`; user flips `mode.md` → `/clear` → `/effort medium` (build phase, orchestration.md §1). Copy `.claude/agents/` + settings if not done; add real test/build commands to CLAUDE.md §Commands.

Exit criterion: every question in the council verdicts answered in `decisions.md`; no "TBD/undecided" left in docs except open-risks build-phase items.
