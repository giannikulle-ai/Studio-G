# console/ — the control room

A small web app on PW-1x. **You work in Claude Code; you watch and steer from here.** No chat box.

It shows what's running and gives you verbs: send this instruction and these files to a new session, hand that session's result to this one, stop that, wake this one when the overnight job finishes. Those verbs already exist as the Claude Code Remote API — create, send, list, get, interrupt, title, tag, schedule, watch. The console is a viewer with buttons over them.

**It never sits between you and Claude.** If the console is down, Claude Code still works.

## The one rule

**The console knows nothing about Claude specifically.** Everything connected to it is an *adapter* with the same shape — see `adapters/README.md`. The UI renders every adapter the same way: a card, a stream, buttons. A handoff is a verb on one adapter whose input is another adapter's output. Adding a thing means writing one adapter file. Another AI provider later is just another adapter.

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
