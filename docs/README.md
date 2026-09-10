# docs/

Mirrors of the canonical artifacts, plus the plan.

| File | Canonical source | How it got here |
|---|---|---|
| `handoff.html` | https://claude.ai/code/artifact/518fcfa6-6bd5-4751-b982-98056c5f555a | Byte-exact copy of the artifact read |
| `build-sheet.html` | https://claude.ai/code/artifact/af94f37f-10d3-43d1-a183-66c2a7306341 | Mirrored from the artifact read |
| `systems-map.html` | https://claude.ai/code/artifact/0d57bcf9-55a9-4eda-87c9-4807749ee677 | The authored source; the artifact is published from this file |
| `console-mockup.html` | https://claude.ai/code/artifact/bba85142-a162-48fd-b06f-840e41162b62 | The authored source; the artifact is published from this file. A mockup, not a spec — see below |
| `console-drafts/console-rack.html` | https://claude.ai/code/artifact/933e6607-9d17-4a76-ac7a-588b616bf813 | Same content as the mockup, in a different skin: gunmetal rack units, amber readouts |
| `console-drafts/console-swiss.html` | https://claude.ai/code/artifact/4b552143-a4e5-4bb1-978c-7e4c9fac011b | Same content, white, black and one red |
| `console-drafts/console-soft.html` | https://claude.ai/code/artifact/f2019191-acdd-42ac-95a6-19d6bd2d9a57 | Same content, white cards on a tinted ground, teal |
| `plan.md` | This repo | The approved plan |

**The artifacts are canonical.** These files exist so `tools/spec-check.py` can run over them in CI. When an artifact is republished, re-mirror it here in the same commit and run the check — the checker will tell you if the two mirrors have drifted from each other, which is the failure mode that actually bites.

The Handoff and Build Sheet carry the platform's wrapper line (`<!doctype html>…<body>`) as the artifact read returns it; the Systems Map does not, because it is the authored source rather than a read-back. Either is fine — the checker strips tags before comparing text.

The Systems Map is checked for structure (tag balance, every class styled), for orthogonal edges (no diagonal `<line>`, no curve commands in any `<path>`), and for words from the superseded design (a local Foreman, a handoff bus, execution tiers). It carries no figures the other two documents share, so it is not part of the cross-document fact check.

The Console mockup is a draft for decision, not a canonical document: its Console tab shows example data as it will look at A5, its Screens tab the three kiosk routes and the fallback page, and its "Under the hood" tab the one Node service, routes, types and build order that `console/README.md` and `console/adapters/README.md` already imply. It is not checked by `spec-check.py`. When a choice in it is confirmed, it belongs in `console/README.md`. The three files in `console-drafts/` are the same page in three other visual treatments, for choosing between; the content and structure are identical to `console-mockup.html` and only the stylesheet differs. Once one is picked, the others go.
