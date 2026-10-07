#!/bin/sh
# SessionStart hook: inject resume context so a fresh session never starts blind.
# Prints mode, progress.md (capped), last decisions, app-map header. Cheap: ~2-4k tokens max.
cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
echo "## Resume context (auto-injected; follow CLAUDE.md session-start order)"
[ -f mode.md ] && echo "mode: $(cat mode.md)"
[ -f progress.md ] && { echo; echo "### progress.md"; sed -n '1,80p' progress.md; }
[ -f decisions.md ] && { echo; echo "### decisions.md (last 15)"; tail -n 15 decisions.md; }
[ -f app-map.md ] && { echo; echo "### app-map.md (head; read full file before touching code)"; sed -n '1,25p' app-map.md; }
git rev-parse --git-dir >/dev/null 2>&1 && { echo; echo "### git"; git log --oneline -5 2>/dev/null; git status --short | head -15; }
exit 0
