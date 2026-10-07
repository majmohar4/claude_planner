#!/usr/bin/env python3
"""Project tool setup: check + idempotent install.

- check(): list of missing items (plugins from settings.json enabledPlugins, LSP binaries, PATH).
- install(): installs what's missing; returns log lines.
- As UserPromptSubmit hook: prompt exactly `install` → run install(), block the prompt
  (no tokens spent), show result + restart warning. Any other prompt → no-op.
Auto-install runs from session-start.py on open (opt-out: empty `.claude/no-auto-install`); typing `install` = manual retry.
"""
import json, os, shutil, subprocess, sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", ".")
NPM_BIN = None
LSP = {"typescript-lsp@claude-plugins-official": ("typescript-language-server", ["typescript-language-server", "typescript"]),
       "pyright-lsp@claude-plugins-official": ("pyright-langserver", ["pyright"])}

def _json(path, default):
    try:
        return json.load(open(path))
    except (OSError, ValueError):
        return default

def wanted():
    s = _json(os.path.join(ROOT, ".claude/settings.json"), {})
    return [p for p, on in s.get("enabledPlugins", {}).items() if on], s.get("extraKnownMarketplaces", {})

def installed():
    return _json(os.path.expanduser("~/.claude/plugins/installed_plugins.json"), {}).get("plugins", {})

def npm_bin():
    try:
        return subprocess.run(["npm", "prefix", "-g"], capture_output=True, text=True, timeout=20).stdout.strip() + "/bin"
    except (OSError, subprocess.SubprocessError):
        return None

def check():
    plugins, _ = wanted()
    have = installed()
    problems = []
    miss = [p for p in plugins if p not in have]
    if miss:
        problems.append("plugins missing: " + ", ".join(p.split("@")[0] for p in miss))
    nob = [b for p, (b, _) in LSP.items() if p in plugins and not shutil.which(b)]
    if nob:
        problems.append("not on PATH: " + ", ".join(nob))
    return problems

def run(cmd, log, timeout=300):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = (r.stdout + r.stderr).strip().splitlines()
        log.append(("✔ " if r.returncode == 0 else "✘ ") + " ".join(cmd) + (f" — {out[-1]}" if out else ""))
        return r.returncode == 0
    except (OSError, subprocess.SubprocessError) as e:
        log.append(f"✘ {' '.join(cmd)} — {e}")
        return False

def install():
    log = []
    plugins, markets = wanted()
    have = installed()
    if not shutil.which("claude") and any(p not in have for p in plugins):
        log.append("✘ `claude` CLI not on PATH — install plugins manually (setup.md §8)")
        markets, plugins = {}, [p for p in plugins if p in have] + [p for p in plugins if p not in have and p in LSP]
        have = {**have, **{p: 1 for p in plugins}}
    for name, spec in markets.items():
        src = spec.get("source", {})
        if src.get("source") == "github" and not any(p.endswith("@" + name) for p in have):
            run(["claude", "plugin", "marketplace", "add", src["repo"]], log)
    for p in plugins:
        if p not in have:
            run(["claude", "plugin", "install", p], log)
    pkgs = [pkg for p, (b, pk) in LSP.items() if p in plugins and not shutil.which(b) for pkg in pk]
    if pkgs and shutil.which("npm"):
        nb = npm_bin()
        missing_bins = [b for p, (b, _) in LSP.items() if p in plugins and not (nb and os.path.exists(os.path.join(nb, b)))]
        if missing_bins:
            run(["npm", "i", "-g"] + pkgs, log, timeout=600)
        if nb and nb not in os.environ.get("PATH", "").split(":"):
            rc = os.path.expanduser("~/.zshrc" if os.environ.get("SHELL", "").endswith("zsh") else "~/.bashrc")
            line = f'export PATH="{nb}:$PATH"'
            try:
                current = open(rc).read() if os.path.exists(rc) else ""
                if line not in current:
                    open(rc, "a").write(f"\n# added by claude_planner setup\n{line}\n")
                    log.append(f"✔ added {nb} to PATH in {rc}")
            except OSError as e:
                log.append(f"✘ PATH update {rc} — {e}")
    elif pkgs:
        log.append("✘ npm not found — install Node, then type `install` again")
    return log or ["✔ nothing to install"]

def main():
    data = json.load(sys.stdin)
    if data.get("prompt", "").strip().lower() != "install":
        return
    log = install()
    tail = ([] if log == ["✔ nothing to install"]
            else ["", "🔴🔴 RESTART REQUIRED 🔴🔴 /exit, open a NEW terminal, run claude"])
    msg = "\n".join(["🛠 Setup:"] + log + tail)
    print(json.dumps({"decision": "block", "reason": msg}))

if __name__ == "__main__":
    main()
