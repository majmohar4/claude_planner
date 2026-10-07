# testing.md — how to verify each component. Sections fixed; append per component.

## Definition of done
Automated tests green + manual-device items for touched components checked by user.

## Automated
- (none yet)

## Manual / device
- 

## Edge cases (ask user to verify)
- 

## Frontend visual
- Playwright screenshots at desktop + mobile sizes vs design refs; design-rules.md checklist.

## Legal / privacy
- No non-essential cookie/storage/request before consent (Playwright: fresh profile, assert network + storage). Reject-all path works. Export + delete account end-to-end. Policy links reachable from every page/screen.

## Process checks (planning mode)
- Session start order followed; progress.md updated; `git status` shows only `.md`/settings while mode = planning.
- Agents: every build task has a brief + report in `docs/gates/<task>/`; no agent commits; reviewer 🔴/🟡 closed before gate.
