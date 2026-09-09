# console/ — your single interface

A small web app on PW-1x. **One interface for you, connectors for frontier.** You watch what's running, steer it, chat with local models, and hand work to frontier providers — all here.

**Frontier is a connector, not a chat box.** You don't type into Claude here. You give it an instruction and files, and watch: send this to a new session, hand that session's result to this one, stop that, wake this one when the overnight job finishes. Those verbs already exist as the Claude Code Remote API — create, send, list, get, interrupt, title, tag, schedule, watch. The console is a viewer with buttons over them. Claude Code itself stays available when you want to type into it directly; if the console is down, it still works.

**Chat with local is a verb on a card.** The `local-models` adapter has an `ask` verb: a text input and a model picker, with the reply streaming into the card's events panel. Underneath it is one call to `studio-local`'s `/v1`, so it is logged and metered like everything else. No separate chat app is installed; Open WebUI is the documented upgrade if history and file uploads ever outgrow the card.

## The one rule

**The console knows nothing about Claude specifically.** Everything connected to it is an *adapter* with the same shape — see `adapters/README.md`. The UI renders every adapter the same way: a card, a stream, buttons. A handoff is a verb on one adapter whose input is another adapter's output. Adding a thing means writing one adapter file. Another AI provider later is just another adapter.

## "Have them talk to each other" — from your seat

A handoff is a verb at the console whose input is another adapter's output: local briefs a repo → you hand the brief to the Claude connector → its result comes back → you hand that to another connector, or back to local. The work log records the chain. You route, at one place; nothing needs to know anything else exists. Separately, a connector may use the local door on its own — Claude does, over MCP, mid-task, and it lands in the same log as `source = claude`. That is a bonus, not the mechanism. For overnight work `batch_job` returns at once and PW-1x wakes the session by webhook when done. There is no bus because the console, the adapters and the one door *are* the bus.

## Hooks for other AIs

Reserved, not installed — see the rows in `adapters/README.md`. Another agent product is a `session` connector with the same verbs as `claude-code-remote`. OpenAI, Gemini or any request/response API is a `call` connector with `ask(instruction, files)` and `batch`. Another local runtime or box is not a connector at all: it is a backend behind `studio-local` (see `../mcp/README.md`). Every frontier connector obeys the same rule as Claude: never a chat box; you hand it instructions and files and watch, and its calls land in the work log.

## What it serves

| Route | For | Auth |
|---|---|---|
| `/` | The full console | Tailscale only |
| `/screens/bench` | Screen A — hardware truth, print progress, the light | Tailscale / direct LAN |
| `/screens/night` | Screens B and C — overnight summary, alerts, PW-1x up or down | Tailscale |
| `/hook/<adapter>` | Inbound webhooks (GitHub, Cloudflare, P2S, phone actions) | Per-adapter secret |

Screen routes are read-only and embed Grafana panels. Each Pi's kiosk script health-checks this box and falls back to the static "PW-1x is down" page on Cloudflare Pages when it fails, so no screen is ever blank.

## Stack, kept boring

One Node/TypeScript service. SSE for streams. SQLite for the work log. One plain HTML front end. No framework religion — the point is that it stays small enough to rewrite in a weekend.

Served by Caddy, reached over Tailscale. Both free, both replaceable plumbing.

## Build order

The skeleton and the `claude-code-remote` adapter need nothing from PW-1x — build and run them on the desktop first. Real backends attach at A5.
