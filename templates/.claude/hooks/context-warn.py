#!/usr/bin/env python3
"""UserPromptSubmit hook: warn user + Claude when main-session context grows.

Claude cannot see its own context meter; this reads real token usage from the
transcript. Warns once per band (soft, hard) per session. Thresholds via env:
CTX_SOFT (default 100000), CTX_HARD (default 160000) tokens.
"""
import json, os, sys, tempfile

SOFT = int(os.environ.get("CTX_SOFT", 100_000))
HARD = int(os.environ.get("CTX_HARD", 160_000))

def context_tokens(path):
    last = 0
    try:
        with open(path) as f:
            for line in f:
                try:
                    e = json.loads(line)
                except ValueError:
                    continue
                if e.get("isSidechain"):
                    continue
                m = e.get("message")
                u = m.get("usage") if isinstance(m, dict) else None
                if u:
                    last = (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                            + u.get("cache_read_input_tokens", 0))
    except OSError:
        pass
    return last

def main():
    data = json.load(sys.stdin)
    tokens = context_tokens(data.get("transcript_path", ""))
    band = 2 if tokens >= HARD else 1 if tokens >= SOFT else 0
    state = os.path.join(tempfile.gettempdir(), f"ctx-warn-{data.get('session_id', 'x')}")
    try:
        warned = int(open(state).read())
    except (OSError, ValueError):
        warned = 0
    if band < warned:  # context shrank (/compact): reset
        warned = band
    if band > warned:
        k = tokens // 1000
        if band == 2:
            user = f"Context ~{k}k tokens: quality dropping. /clear (phase done) or /compact <focus> now."
            claude = (f"Main context ~{k}k tokens (HARD). Before anything else: make progress.md current, "
                      "finish only the current step, then tell the user to /clear (or /compact <focus> if mid-task). "
                      "Delegate all further reading to agents.")
        else:
            user = f"Context ~{k}k tokens. Plan a /clear at the next phase end."
            claude = (f"Main context ~{k}k tokens (SOFT). Delegate further reading to agents; at the next "
                      "phase boundary update progress.md and tell the user to /clear.")
        print(json.dumps({"systemMessage": user,
                          "hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": claude}}))
    try:
        open(state, "w").write(str(max(band, warned)))
    except OSError:
        pass

if __name__ == "__main__":
    main()
