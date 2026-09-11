# Studio-G

Everything around PW-1x: the plan, the documents that describe the machine, the tool server that lets Claude use it, the control room that watches it all, and the measurements that replace the estimates.

PW-1x ("Projectile William v1") is a dual-role box — a local LLM server and a host for websites and dev environments. It is bought and awaiting delivery. The two documents in `docs/` say what it is; `docs/plan.md` says how it gets stood up and what the studio around it looks like.

## The shape of it

**One interface for you, connectors for frontier.** The console (`console/`) is where you work: watch what's running, steer it, chat with local models, and hand instructions and files to frontier providers. Frontier is a connector — you don't type into Claude there; you dispatch work to it and watch. Everything connected to the console is an adapter with one shape, so adding a thing is one file. Claude Code stays available when you want to type into it directly; nothing depends on that.

**One door to local models.** `studio-local` (`mcp/`) is the only way anything reaches them: an MCP face for Claude, an OpenAI-compatible `/v1` face for you and everything else. Every call is logged and metered whoever makes it. When Claude delegates, local reads the forty files and hands back a page, so frontier tokens go to judgment. That is the whole mechanism.

## Layout

| Directory | What lands here | When |
|---|---|---|
| `docs/` | The PW-1x Handoff, Build Sheet, Systems Map and Assembly Guide as version-controlled source, plus the plan | Now — mirrored from the canonical artifacts |
| `tools/` | `spec-check.py` — the mechanical checker CI runs over `docs/` | Now |
| `mcp/` | `studio-local` — the one door to local models: MCP for Claude, `/v1` for everything else | Now, against Ollama on the desktop; PW-1x attaches at A5 |
| `console/` | Your single interface; `adapters/` one file per connected thing | Now, skeleton + the Claude Code Remote and local-models adapters |
| `systemd/` | Units and resource-control drop-ins | After OS install (A3) |
| `caddy/` | `Caddyfile` | After OS install (A3) |
| `scripts/` | llama.cpp build, model fetch, kiosk scripts for the screens | Bring-up (A5) and screen builds |
| `bench/` | Measured tok/s — the numbers that replace the estimates | First real run (A5) |
| `notes/` | Facts checked against the real machine, one file each | As each is checked |

## The documents

- **PW-1x Handoff** — three layers: non-technical summary, full technical spec, machine-readable state.
- **PW-1x Build Sheet** — the same build, narrower and more opinionated.
- **Studio-G Systems Map** — physical topology, how a task moves, where things live. Three figures on one grid.
- **PW-1x Assembly Guide** — inventory checklist and the twelve-step open-bench build, CPU-only, written for a first server build.

The artifacts on claude.ai are canonical. `docs/` mirrors all three so the checker can run in CI.

## Verifying the documents

```
python3 tools/spec-check.py
```

Six checks over four documents: arithmetic, cross-document consistency (Handoff against Build Sheet, Assembly Guide against Build Sheet), stale strings (including GPU-build language in the guide), structural validity, the Systems Map's orthogonal edges and superseded-design words, and physics-vs-method. Exits non-zero on any failure. CI runs it on every push that touches `docs/`.

## Status

All hardware bought. Nothing left to procure. Awaiting delivery. The 4060 Ti stays in the desktop, so PW-1x starts CPU-only; a 3090-class card is the planned purchase once real prefill numbers exist. See `docs/plan.md`.
