# milestones.md — build plan. Every milestone ends with a TEST GATE. Core first, features last.

## Rules
- Gate = automated tests green + manual checklist signed by user + testing.md/debugging.md/progress.md updated. No gate → no next milestone.
- Legal + security in every milestone that touches them (legal.md, process 16/17): consent before tracking, export/delete with accounts, policies before any public build. Last milestone before release gate: Cloudflare `security-audit` clean (no confirmed criticals) + legal.md fully ticked.
- Gate end: full suite + release build once, then `purge` (CLAUDE.md §Commands) with `du -sh` before/after in progress.md.
- ≤2 weeks per milestone; split if bigger. Feature flags in one codebase.

## P — Planning
Deliver: product.md · data-model.md · sync-contract.md · design.md · milestones.md confirmed · decisions answered.
Gate P: user reviews all; flips `mode.md`.

## M0 — Toolchain & skeleton
Build: toolchain · fill CLAUDE.md §Commands (single-test, full test, debug/release build, output dirs, purge) · gitignore output dirs · allow list in `.claude/settings.local.json` · 
Gate M0: 

## M1 — 
Build: 
Gate M1: automated — · manual — · edge — 
