#!/usr/bin/env python3
"""SessionStart hook.
1. Setup check → red warning shown to the user immediately (before first prompt):
   missing plugins/LSP binaries (setup.py); auto-installs on open (opt-out: .claude/no-auto-install); `install` prompt retries.
2. Resume context for Claude: mode, progress.md, last decisions, app-map head, git.
3. Records session start time so context-warn.py can flag .claude/ edits needing restart.
"""
import json, os, subprocess, sys, tempfile, time

root = os.environ.get("CLAUDE_PROJECT_DIR", ".")
try:
    data = json.load(sys.stdin)
except ValueError:
    data = {}

def read(p, head=None, tail=None):
    try:
        lines = open(os.path.join(root, p)).read().splitlines()
    except OSError:
        return None
    if head: lines = lines[:head]
    if tail: lines = lines[-tail:]
    return "\n".join(lines)

# 1. setup check + auto-install (opt-out: empty file .claude/no-auto-install)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import setup
problems = setup.check()
installed_log = None
if problems and not os.path.exists(os.path.join(root, ".claude/no-auto-install")):
    installed_log = setup.install()
    problems = setup.check() if any(l.startswith("✘") for l in installed_log) else []

# 2. resume context
parts = ["## Resume context (auto-injected; follow CLAUDE.md session-start order)"]
mode = read("mode.md")
if mode: parts.append("mode: " + mode.strip())
for title, text in [("progress.md", read("progress.md", head=80)),
                    ("decisions.md (last 15)", read("decisions.md", tail=15)),
                    ("app-map.md (head; read full file before touching code)", read("app-map.md", head=25))]:
    if text: parts.append(f"### {title}\n{text}")
try:
    git = subprocess.run(["git", "-C", root, "log", "--oneline", "-5"], capture_output=True, text=True, timeout=5).stdout
    st = subprocess.run(["git", "-C", root, "status", "--short"], capture_output=True, text=True, timeout=5).stdout
    parts.append("### git\n" + git + "\n".join(st.splitlines()[:15]))
except (OSError, subprocess.SubprocessError):
    pass
if installed_log:
    parts.append("Tools were just auto-installed; they load only after restart — tell the user in red to /exit and reopen.")
if problems:
    parts.append("SETUP INCOMPLETE — tell the user first, in red, before any work: " + " | ".join(problems))

# 3. start stamp for restart detection
try:
    open(os.path.join(tempfile.gettempdir(), f"ctx-start-{data.get('session_id', 'x')}"), "w").write(str(time.time()))
except OSError:
    pass

out = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n\n".join(parts)}}
if installed_log and not problems:
    out["systemMessage"] = "🛠 Auto-installed:\n" + "\n".join(installed_log) + "\n🔴🔴 RESTART REQUIRED 🔴🔴 /exit, open a NEW terminal, run claude"
elif problems:
    out["systemMessage"] = ("\n".join(installed_log or []) + "\n" if installed_log else "") + ("🔴🔴 SETUP INCOMPLETE 🔴🔴 " + " | ".join(problems)
                            + "\n👉 Fix the ✘ items above (setup.md §8), or type `install` to retry. Then /exit, open a NEW terminal, run claude.")
print(json.dumps(out))
