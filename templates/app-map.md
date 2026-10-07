# app-map.md — how the app actually works. Next session reads this before any code. Update at every milestone gate (and when structure changes). ≤150 lines; facts + pointers, no prose.

Last updated: <date> · milestone: <Mx> · commit: <short sha>

## One paragraph
<what it does, for whom, main flow in 3 sentences>

## Run it
- dev: `<cmd>` · test: see CLAUDE.md §Commands · URLs/ports/devices: <…>
- env/config: <files, never values>

## Architecture (boxes → arrows)
<client> → <api> → <db/services> · sync/background jobs · external providers
Diagram: <path to visualize/CodeWiki output, if any>

## Modules (path · responsibility · owns data · talks to)
- `<path>` · <what> · <tables/state> · <deps>

## Entry points + key flows (flow · start file:line · steps)
- <login> · `<file:line>` · <a → b → c>

## Data
Entities + where stored → data-model.md. Invariants that must never break: <list or pointer to sync-contract.md>

## Gotchas (non-obvious; things a fresh session would get wrong)
- <…>

## Where things are not yet built
- <feature → milestone>
