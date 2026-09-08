# Studio-G

Everything around PW-1x: the plan, the documents that describe the machine, the tool server that lets Claude use it, the control room that watches it all, and the measurements that replace the estimates.

PW-1x ("Projectile William v1") is a dual-role box — a local LLM server and a host for websites and dev environments. It is bought and awaiting delivery. The two documents in `docs/` say what it is; `docs/plan.md` says how it gets stood up and what the studio around it looks like.

## The shape of it

**Claude manages local.** You work in Claude Code on your subscription. PW-1x's local models are tools Claude calls through an MCP server (`mcp/`). Local reads the forty files and hands back a page; Claude spends its rate-limited tokens on judgment. That is the whole mechanism.

**A thin control room watches and steers** (`console/`). No chat box. It shows what's running — Claude sessions, local models, PW-1x, the printer, the light, your projects — and gives you verbs over them. Everything connected to it is an adapter with one shape, so adding a thing is one file. It never sits between you and Claude.

## Layout

| Directory | What lands here | When |
|---|---|---|
| `docs/` | The PW-1x Handoff and Build Sheet as version-controlled source, plus the plan | Now — mirrored from the canonical artifacts |
| `tools/` | `spec-check.py` — the mechanical checker CI runs over `docs/` | Now |
| `mcp/` | `studio-local` — local models as tools for Claude | Now, against Ollama on the desktop; PW-1x attaches at A5 |
| `console/` | The control room; `adapters/` one file per connected thing | Now, skeleton + the Claude Code Remote adapter |
| `systemd/` | Units and resource-control drop-ins | After OS install (A3) |
| `caddy/` | `Caddyfile` | After OS install (A3) |
| `scripts/` | llama.cpp build, model fetch, kiosk scripts for the screens | Bring-up (A5) and screen builds |
| `bench/` | Measured tok/s — the numbers that replace the estimates | First real run (A5) |
| `notes/` | Facts checked against the real machine, one file each | As each is checked |

## The documents

- **PW-1x Handoff** — three layers: non-technical summary, full technical spec, machine-readable state.
- **PW-1x Build Sheet** — the same build, narrower and more opinionated.
- **Studio-G Systems Map** — physical topology, how a task moves, where things live. An artifact; not mirrored here yet.

The artifacts on claude.ai are canonical. `docs/` mirrors them so the checker can run in CI.

## Verifying the documents

```
python3 tools/spec-check.py
```

Five checks: arithmetic, cross-document consistency, stale strings, structural validity, physics-vs-method. Exits non-zero on any failure. CI runs it on every push that touches `docs/`.

## Status

All hardware bought. Nothing left to procure. Awaiting delivery. The 4060 Ti stays in the desktop, so PW-1x starts CPU-only; a 3090-class card is the planned purchase once real prefill numbers exist. See `docs/plan.md`.
