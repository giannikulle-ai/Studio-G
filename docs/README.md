# docs/

Mirrors of the canonical artifacts, plus the plan.

| File | Canonical source | How it got here |
|---|---|---|
| `handoff.html` | https://claude.ai/code/artifact/518fcfa6-6bd5-4751-b982-98056c5f555a | Byte-exact copy of the artifact read |
| `build-sheet.html` | https://claude.ai/code/artifact/af94f37f-10d3-43d1-a183-66c2a7306341 | Mirrored from the artifact read |
| `systems-map.html` | https://claude.ai/code/artifact/0d57bcf9-55a9-4eda-87c9-4807749ee677 | The authored source; the artifact is published from this file |
| `console-mockup.html` | https://claude.ai/code/artifact/bba85142-a162-48fd-b06f-840e41162b62 | The authored source; the artifact is published from this file. A mockup, not a spec — see below |
| `plan.md` | This repo | The approved plan |

**The artifacts are canonical.** These files exist so `tools/spec-check.py` can run over them in CI. When an artifact is republished, re-mirror it here in the same commit and run the check — the checker will tell you if the two mirrors have drifted from each other, which is the failure mode that actually bites.

The Handoff and Build Sheet carry the platform's wrapper line (`<!doctype html>…<body>`) as the artifact read returns it; the Systems Map does not, because it is the authored source rather than a read-back. Either is fine — the checker strips tags before comparing text.

The Systems Map is checked for structure (tag balance, every class styled), for orthogonal edges (no diagonal `<line>`, no curve commands in any `<path>`), and for words from the superseded design (a local Foreman, a handoff bus, execution tiers). It carries no figures the other two documents share, so it is not part of the cross-document fact check.

The Console mockup is a draft for decision, not a canonical document. It is drawn from two paper sketches: the page answers **Where are we?** first, grouping everything connected into *Lost in the jungle* and *Navigating*; the log sits on the right with live work pinned to the top; the tool section is a grid of bracketed tiles (Bot Land, Project Center, Local models, Dashboards, Storage, Connections, Printer, and a dashed one for whatever comes next); and the header carries PW-1x's work-and-server split, which opens the dashboard. Below the console the same file documents how it is built: what earns a place on the page, the one Node service, the routes, the adapter types, a handoff step by step, the three kiosk screens, the layout on disk and the build order. It is not checked by `spec-check.py`. When a choice in it is confirmed, it belongs in `console/README.md`.
