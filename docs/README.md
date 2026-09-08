# docs/

Mirrors of the canonical artifacts, plus the plan.

| File | Canonical source | How it got here |
|---|---|---|
| `handoff.html` | https://claude.ai/code/artifact/518fcfa6-6bd5-4751-b982-98056c5f555a | Byte-exact copy of the artifact read |
| `build-sheet.html` | https://claude.ai/code/artifact/af94f37f-10d3-43d1-a183-66c2a7306341 | Mirrored from the artifact read |
| `plan.md` | This repo | The approved plan |

**The artifacts are canonical.** These files exist so `tools/spec-check.py` can run over them in CI. When an artifact is republished, re-mirror it here in the same commit and run the check — the checker will tell you if the two mirrors have drifted from each other, which is the failure mode that actually bites.

Both HTML files carry the platform's wrapper line (`<!doctype html>…<body>`) as the artifact read returns it. That is expected; the checker strips tags before comparing text.
