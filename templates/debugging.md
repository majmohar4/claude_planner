# debugging.md — known traps. Append on real incidents: symptom · cause · check.

## Process
- Claude wrote code in planning mode · ignored `mode.md` · revert; re-read CLAUDE.md session-start order.
- Next session lost context · `progress.md` not updated · always update at task end.

## Dev machine
- macOS `head -N` prints LWP usage · `head` resolves to Perl LWP · use `sed -n '1,Np'` or `/usr/bin/head`.
