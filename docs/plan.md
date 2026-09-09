# PW-1x — bring-up, routing, hosting, and repo

## Context

PW-1x ("Projectile William v1") is a dual-role machine: a local LLM server that absorbs high-volume agent work currently hitting rate limits on a commercial plan, and a host for websites and dev environments. All parts are bought (~$2,240.59); nothing is left to procure. The machine does not exist yet — it is awaiting delivery.

Two artifacts describe it and both now pass a full mechanical check (arithmetic, cross-document consistency, stale strings, structural validity, physics-vs-method):

- **PW-1x Handoff** — https://claude.ai/code/artifact/518fcfa6-6bd5-4751-b982-98056c5f555a
- **PW-1x Build Sheet** — https://claude.ai/code/artifact/af94f37f-10d3-43d1-a183-66c2a7306341

Those documents say *what* the machine is. This plan says *how it gets stood up* and *what has to be decided before the boxes arrive*. **It does not modify either artifact.**

The repo `giannikulle-ai/Studio-G` is currently empty — no commits at all, and branch `claude/pw-1x-handoff-spec-inwpu5` has no history.

---

## How the four workstreams interlock

```
NOW (no hardware)          ON DELIVERY              AFTER INFERENCE IS STABLE
─────────────────          ───────────              ─────────────────────────
D. Repo scaffold  ─────────────────────────────────────────────────────────▶
A0. Baseline + measure  ──▶  A1–A5 Bring-up  ──────▶
B. Routing design ─────────────────────────────────▶  B. Routing implement ─▶
C. Hosting design ──┐                                 C. Hosting migrate ───▶
                    └──▶ must be settled before A3 (OS install / partitioning)
```

Three things make this ordering non-obvious, and each is a real constraint rather than a preference:

1. **Partitioning is an install-time decision.** `/var/lib/containers` on its own partition (Handoff, "Storage") cannot be retrofitted without a rebuild. So the hosting plan must be settled *before* OS install, even though migration happens last.
2. **The throughput baseline can only be captured before the machine exists.** The headline claim is "roughly double usable throughput." That is unprovable unless the *current* rate-limit-hit rate is recorded first. This measurement window closes the day the box comes up.
3. **The memory return window starts at delivery, not order** — and memtest needs an assembled machine (see the ordering correction below).

---

## A. Bring-up sequence

### Correction to the Handoff's own "Next actions"

The Handoff lists memtest (step 2) *before* assembly (step 3). That order can't execute: memtest86+ needs the CPU, cooler, PSU and board mounted and POSTing. **Assembly comes first.** This matters because the 30-day return window is running while you work it out. The corrected order is A1 → A2 below.

### A0 — Now, before anything ships (costs nothing)

- Install Ollama on the existing desktop, pull `gpt-oss:20b`, run it on the 4060 Ti, point the current agent harness at `localhost:11434/v1`.
- **Record the current state before changing it:** rate-limit hits per day, sessions lost to them, rough share of work that is high-volume/low-difficulty. Without this there is no "before" to double.
- Answers the assumption the whole build rests on: is the small tier actually useful? If it isn't, the 120B tier is doing more work than planned and the tok/s estimates matter far more.
- Check whether llama.cpp PR #20539 actually landed stock support for Nemotron's `modelopt`/NVFP4 quant. It's a five-minute check that could move the best-scoring model from "Unresolved" to "Primary" and change the model set before you tune anything.
- Confirm the board's EPS requirement against the ASRock manual (docs flag it as sourced from a ServeTheHome review only). The PSU covers either reading, so this is not a purchase risk — it's a no-POST-at-2am risk.

### A1 — Assemble (on delivery)

Open bench, non-conductive surface, off carpet, away from pets. 24-pin + EPS per A0's confirmed answer. Do not shuck the G-DRIVE — no SATA ports on this board.

### A2 — memtest86+ — the clock is running

All eight modules together, full passes, overnight. If anything errors, re-run one stick at a time to identify it. **Do this inside the 30-day window**, counted from delivery. A failure found in week one is a defective return; the same failure in month four is a warranty claim needing a *matched* replacement on a 1DPC board, or replacing all eight.

### A3 — OS install and partitioning ⚠️ gated on C

Debian or Ubuntu Server, bare metal, no hypervisor. Partition per the hosting plan (§C) — at minimum `/var/lib/containers` separate so a runaway image pull cannot fill the disk out from under the model files. 1TB is tight for OS + 2–3 models + container images; the second M.2 slot stays free for later.

### A4 — Thermals under load

Load sustained inference, read VRM and DIMM temperatures over IPMI. Open bench means no directed airflow over the passive VRM heatsinks or DIMM bank. Add a ~$12 fan aimed at the DIMM bank **only if the numbers call for it** — the whole reason case and fans weren't bought.

### A5 — Inference stack and the first real numbers

- Build llama.cpp **CPU-only** — there is no GPU in PW-1x until one is bought. When a card arrives, rebuild with CUDA and check the startup log for device detection: a CPU-only build loads fine and runs at a crawl, which reads as "slow model" rather than "wrong build".
- Load `gpt-oss-120b-Q8_0` fully in RAM with `-b 4096 -ub 4096 -c 32768`. `--n-cpu-moe` and `-ngl` only apply once a GPU exists; then start from `--n-cpu-moe 40 -ngl 999` and tune downward until VRAM is nearly full.
- **Record actual tok/s — decode and prefill, prefill on a 32k context.** Prefill is the number that decides the GPU purchase. The published 17–25 is a judgement call discounted from a hard 51 tok/s ceiling; Scout's 8–11 sits under a 14 ceiling. Measured numbers replace both. If real decode lands above the stated ceiling, the bandwidth figure or the active-parameter accounting is wrong — investigate rather than celebrate.
- Repeat for Scout to validate the alternate.

### A6 — Housekeeping

Close the three memory quote threads (Topmemory, memory.net, TechMikeNY) with one line each. Keep the contacts — the second GPU and any Milan CPU come from the same channel.

---

## B. Claude manages local

**Direction (decided):** frontier manages, local works. Claude — on the subscription, in Claude Code (web, CLI, or Remote) — is the brain. Local models are **tools it calls**. This replaces the earlier "local Foreman dispatches to Claude as a tier" design, which had it backwards.

**Why this is the better answer to the original problem.** The rate limit is on frontier tokens. Under this design, local reads the forty files and hands Claude a one-page brief; Claude's context stays small and every subscription token is spent on judgment, not on reading. That is the "double throughput" mechanism, and it is simpler than a routing table.

**The mechanism: an MCP server on PW-1x.** `mcp/studio-local` exposes local models as tools Claude Code already knows how to call:

- `read_and_brief(paths | git_ref, question)` — the bulk-read primitive
- `summarize`, `classify`, `extract` — call-shaped volume work
- `batch_job(spec) → job_id`, `job_status`, `job_result` — long-running work

Behind it, the server picks a backend and Claude never sees which: llama.cpp on PW-1x (`/v1`, CPU-only until a GPU is bought — gpt-oss-120b, Scout) or, best-effort, Ollama on the desktop's 4060 Ti (gpt-oss-20b) over 10GbE, falling back to PW-1x when the PC is busy. Claude Code connects to it over Tailscale.

**"Have them talk to each other" is a tool call.** Local's output lands directly in Claude's context. For overnight batch work, `batch_job` returns immediately; when the job finishes PW-1x POSTs to the session's webhook URL and Claude wakes and continues. No bus, no queue beyond the job table.

**Instrumentation lives in the MCP server.** Every call is logged — tool, backend, tokens in/out, latency, fallback — to a work log (SQLite). That log is what the dashboards read and what the before/after throughput comparison against A0 is computed from.

**API keys are not needed for this.** Only if something must run with no Claude session at all. Nothing at launch.

**Direct access to the local models, without Claude — through the same door (decided).** `studio-local` is the *only* way to reach the local models, for Claude and for you. It has two faces on one process:

- **MCP** — what Claude Code connects to. The tools in the list above.
- **OpenAI-compatible `/v1`** — what everything else connects to: the console's `ask` verb, curl, scripts, editor extensions. Same backend selection, same fallback, same swap logic.

Both faces write to the **one work log** (SQLite: source = `claude` | `console` | `client`, tool or endpoint, backend, tokens in/out, latency, fallback) and the **one `/metrics` endpoint** in Prometheus format — calls by source and backend, token counters, latency histograms, `studio_active_requests`. That last gauge drives the USB light instead of llama.cpp's own metric, so the light is right whichever backend is working.

Consequences:
- `llama-server` on PW-1x and Ollama on the desktop bind to localhost and the 10GbE link only. Nothing reaches them except `studio-local`. llama.cpp's built-in chat page is therefore not exposed; it can still be used on the box itself for debugging.
- **Chat with local is an `ask` verb on the `local-models` adapter card (decided).** The card gets a text input and a model picker; the reply streams into the card's events panel. Underneath it is one call to `studio-local`'s `/v1` with `source = console`, so it is logged and metered like everything else. No extra app, no extra container, same shape as every other card. Conversation history is the work log, which already exists; `ask` carries the last N turns. File drop is a later verb input of type `file` that lands as a path reference. **Open WebUI is not installed.** It stays documented as the upgrade if history and uploads ever outgrow the card. The console is the single interface: watch, steer, chat with local, dispatch to frontier.

**The sentence this all reduces to (the original brief, restated):** *single interface for you, connectors for frontier.* The console is the interface. Frontier providers are adapters you hand instructions and files to and watch — never a chat box. Local models are one door, `studio-local`, that logs everything whoever calls it. Claude Code stays available when you want to type into it directly, but nothing depends on that.
- The throughput comparison against A0 can now separate Claude-delegated work from your direct use, because `source` is a column.
- The "no chat box" rule stands for Claude; the local `ask` verb doesn't conflict with it.
- Figure 2 of the Systems Map: the console becomes the hub box (your single interface), the MCP box reads "MCP for Claude · /v1 for everyone else", and Claude Code is drawn as a connector you hand work to. Content change; goes in with this step.

**On Prometheus, since it was asked:** a free metrics database. Exporters publish small pages of numbers; Prometheus scrapes them every 15s and stores the series; Grafana graphs them; Prometheus alert rules fire when a number crosses a line (the light). One place every screen reads from, instead of each thing polling the model server.

**Two models, one card** still applies on PW-1x once a GPU exists — gpt-oss-20b and the 120b swap, they don't coexist. The MCP server owns that decision (which backend, whether to swap), not Claude.

---

## C. Hosting migration

Design before A3. Execute after A5.

**Isolation.** The Handoff's config is now correct and should be used verbatim rather than re-derived: inference on logical CPUs `0-11,32-43`, hosting on `12-31,44-63`, `MemoryMax=76G` / `40G`, 12GB left for host and page cache. **Run `lscpu -e=CPU,CORE` first** — sibling enumeration varies by kernel and BIOS, and pinning core-without-sibling silently isolates nothing. Caps must not sum above 128GB or the OOM killer picks, and it will pick the 63GB process.

**Security posture.** Co-location is the real risk, not performance. Public sites share a host with dev environments and the model stack. Everything internet-facing runs in **rootless Podman**; treat the host as exposed. Containers are not a hard security boundary.

**Stack.** Podman (rootless, no daemon) · Caddy (automatic Let's Encrypt) · Tailscale free tier for dev environments without opening ports. All free.

**Migration order.** Least-critical site first, and let it sit through at least one reboot cycle before moving anything else. Uptime is coupled — a kernel update takes down every hosted service, and every experiment with the inference stack is a risk to them. That argues against putting anything with real availability expectations here at all; decide that explicitly rather than by drift.

**Build contention.** Cap parallelism at `-j16`, not `-j32`. A large parallel compile is the one hosting workload that genuinely fights inference for memory bandwidth.

---

## D. Studio-G repo

Start now — it is unblocked, and it is where everything the other three workstreams produce has to land. Branch `claude/pw-1x-handoff-spec-inwpu5` off the default branch.

Proposed layout:

```
docs/            handoff.html, build-sheet.html, plan.md — the artifacts as source, plus this plan
tools/           spec-check.py — the arithmetic/consistency/structure checker
mcp/             studio-local — the MCP server that exposes local models as tools to Claude (§B)
console/         the control room: one service, adapters/ one file per connected thing (§E)
systemd/         llama-server.service + limits.conf, container slice, mcp + console units
caddy/           Caddyfile
scripts/         build-llama-cpp.sh (CPU-only first), model fetch/verify, kiosk.sh for the screens
bench/           measurement harness + recorded tok/s results (replaces the estimates)
notes/           partition layout, lscpu -e output, IPMI thermal readings, EPS answer
```

Two things worth doing here specifically:

- **`tools/spec-check.py`** is the script from this session's verification pass. In the repo it can run in CI over `docs/`, so the arithmetic and cross-document consistency that were just fixed by hand stay fixed automatically. That closes the loop rather than re-doing this review each time a price moves.
- **`bench/`** is what makes A5's "record actual tok/s" durable. Estimates in the artifacts get replaced from recorded runs, not from memory.

A `SessionStart` hook (see the `session-start-hook` skill) would let web sessions run the checker without setup.

---

## E. The studio around the engine (added after the full brief)

Visualized in **Studio-G Systems Map** — https://claude.ai/code/artifact/0d57bcf9-55a9-4eda-87c9-4807749ee677 — three figures: physical topology, how a task moves, where things live and who watches.

**Physical adds beyond PW-1x.** Desktop PC (10GbE direct to PW-1x). Three screens: A on the bench (small panel + SBC, USB power and LAN from PW-1x, Grafana kiosk), B on the nightstand and C at a second location (repurposed iPad panels + driver board + SBC, over Wi-Fi / Tailscale or Cloudflare Access). USB light on a relay off PW-1x. Hooks with a reserved landing spot: Bambu 3D printer (LAN mode → MQTT → exporter), projector (off the PC, display only), more storage (OCuLink ×2, M.2 #2).

**Software layer — the control room (option "a": thin remote control, decided).** A small web app on PW-1x. **It is your single interface**: you watch and steer from here, you chat with local models here (the `ask` verb on the local-models card, see §B), and you dispatch to frontier from here. No chat box *for Claude* — frontier is a connector you hand work to, not a window you type into. Claude Code itself stays available for when you want to type into it directly. It shows what's running and gives you verbs: send this instruction + these files to a new session, hand this session's result to that one, stop that, wake this one when the overnight job finishes. Those verbs already exist as the Claude Code Remote API (create / send / list / get / interrupt / title / tags / routines / webhooks); the console is a viewer with buttons over them. If the console is down, Claude Code still works — it never sits between you and Claude.

**Design rule: the console is an adapter hub and knows nothing about Claude specifically.** Every connected thing is an **adapter** with one shape:

```
status()   → what it is right now            (read)
events     → a stream of what it's doing      (SSE)
verbs[]    → actions it accepts, each with a schema
```

The UI renders every adapter the same way — a card, a stream, buttons. A handoff is a verb on one adapter whose input is another adapter's output; the work log records the chain. **Adding a thing is writing one adapter file.** Another AI provider later is just another adapter with session-shaped or call-shaped verbs.

Adapters at launch, in `console/adapters/`:

| Adapter | status | events | verbs |
|---|---|---|---|
| `claude-code-remote` | sessions, routines | session output stream | create, send, interrupt, title, tag, schedule, watch |
| `local-models` | backends up/down, model loaded | work log (MCP and `/v1`) | ask, run batch job |
| `pw1x` | CPU/RAM/temps via Prometheus | alerts | restart llama-server |
| `p2s` | print state, progress, temps | MQTT + AI-detection events, camera | pause, resume |
| `usb-light` | on/off | — | on, off, auto |
| `github` | repos, last push, CI | webhook events | open PR |
| `cloudflare` | Pages/Workers deploys, tunnel health | deploy events | redeploy |

**Adapter kinds the shape must cover (decided: all of them).** The shape stays the same; each adapter declares a `kind`, which the UI uses for layout and the work log uses for the throughput comparison.

| kind | examples | status | events | verbs |
|---|---|---|---|---|
| `session` | Claude Code Remote; another agent product later | live sessions | output stream | create · send · interrupt · schedule · watch |
| `call` | local models via MCP; OpenAI / Gemini APIs if wanted | health, quota, model loaded | call log | call · batch |
| `device` | P2S, USB light, smart plugs, sensors, cameras, or one Home Assistant adapter fronting all of them | state | MQTT / webhook stream | the device's own controls |
| `service` | GitHub, Cloudflare, calendar, email, Notion, Linear, registrar, billing | polled | webhooks where offered | few — open PR, redeploy, acknowledge |
| `outbound` | phone push (ntfy self-hosted and free, or Pushover) | — | — | `notify(level, text, actions[])` |

An outbound notification's `actions[]` each carry a verb on another adapter, so "act on it from the lock screen" is a round trip through the console: phone → console → the session or device. That means the console needs one inbound route reachable from the phone — over Tailscale, or Cloudflare Access if the phone isn't on the tailnet.

**Tech, kept boring:** one Node/TypeScript service (the Claude Code Remote API and MCP are both easiest from TS), SSE for streams, SQLite for the work log, one plain HTML front end. Screens A/B/C are read-only routes of the same console with Grafana panels embedded. Served by Caddy, reached over Tailscale — both free, both replaceable plumbing (see the note below).

- **Projects:** GitHub is the only source. Cloudflare Pages/Workers for static/edge; PW-1x rootless Podman + Caddy for containers and dev envs; public exit only via Cloudflare Tunnel + Access.
- **Telemetry:** node / llama.cpp `/metrics` / IPMI exporters on PW-1x, nvidia exporter on the PC, P2S MQTT → Prometheus → Grafana. The USB light is a Prometheus alert → webhook → relay, not a poller, so it's correct when the model server is what's down.
- **Secrets:** sops + age, encrypted in the repo, decrypted on PW-1x at boot. Replaces "API keys all over the place" with one file.

**On Caddy and Tailscale, since it was asked:** both are $0 for personal use. Caddy is the one front door that lets the console, Grafana and hosted sites share one address with HTTPS instead of a list of ports. Tailscale is a private network between your devices so the phone, the nightstand screen and the second-location screen reach PW-1x without opening a router port. Neither is architecture. If everything only ever lived on the home LAN you could skip both.

**Where the five questions landed.** Q1: the **4060 Ti stays in the PC** — PW-1x starts CPU-only, the PC is a best-effort fast tier for gpt-oss-20b over 10GbE. Q2: **subscription, via Claude Code** — local is a tool Claude calls (§B); API keys only if something must run with no Claude session, and nothing does at launch. Q3: **SBC + 7" panel** for Screen A, wired to PW-1x's second 10GbE port. Q4: **Bambu Lab P2S** (256³ enclosed CoreXY, 1080p30 camera with AI detection, dual-band Wi-Fi; LAN mode + Developer Mode → MQTT/FTP/RTSP; ha-bambulab supports it). Q5: **Console on PW-1x + static fallback page on Cloudflare Pages**, kiosks health-check and swap.

**Consequences of Q1 for §A.** A5 becomes a CPU-only build: no CUDA build, `--n-cpu-moe` and `-ngl` are irrelevant, everything lives in RAM. The measured numbers — decode tok/s *and prefill tok/s* on a 32k context — are what decide the GPU purchase. A0's desktop baseline stops being a test and becomes the permanent fast tier. The Handoff's model table ("GPU-resident") and runtime section will need a CPU-only variant later; not edited now.

**The last three, decided.**

- **(a) GPU path: plan around CPU-only, and shop for a 3090-class card in parallel.** The measured CPU-only numbers from A5 are the baseline the purchase is judged against. Buying target, in order: a **used RTX 3090 24GB at or under ~$1,100** (936 GB/s, 350W; one 3090 + the EPYC is ~600W sustained — fine on the 850W ATX 3.1 supply, two would not be); if the 3090 market is above ~$1,300, a **used 4090 24GB at $1,400–2,000** is the better buy for this workload because prefill is the actual pain and the 4090 has roughly twice the compute at only ~7% more bandwidth; **fallback: a new 16GB card (~$430–450)**, which restores the design as drawn but not concurrency. Skip: 3090 Ti (no VRAM gain, 450W), A5000 (same 24GB at $1,800+), 5090 ($3,500+). Sept 2026 price trackers put used 3090s at ~$1,050 with a fair-asking band of $1,287–1,411, up from ~$1,010 in March — sources in the session; treat as volatile, set a ceiling, and use the Topmemory fleet-pull channel the Handoff already names.
- **(b) PC tier: best-effort, only when idle.** Ollama's default idle unload makes it yield; the MCP server tries the PC first for call-shaped volume work and falls back to PW-1x CPU-only without asking.
- **(c) Screens B and C: iPad 2/3/4 panels.** iPad 2 is LP097X02 (1024×768); iPad 3/4 is LP097QX1 (2048×1536 Retina). Both have commodity HDMI driver boards (~$30–50, Amazon/eBay/AliExpress), no touch. **Power is 12V 3A** for the board plus 5V for the Pi — a barrel supply and a buck, or a board variant with USB-C PD input, not a phone charger. A Pi Zero 2 W will not drive 2048×1536 comfortably; either use a Pi 4, or output 1024×768 and let the board upscale — for a dashboard at arm's length the latter is fine.

## First implementation step on approval

Scaffold `giannikulle-ai/Studio-G` on branch `claude/pw-1x-handoff-spec-inwpu5` (the repo is empty). Most of it is already on disk, uncommitted, from the earlier pass; it gets corrected to this design before anything is committed:

- `docs/` — this plan and the two PW-1x artifacts as source. `tools/spec-check.py` with the CI workflow that runs it over `docs/`.
- `mcp/README.md` and `console/README.md` + `console/adapters/README.md` — stating the tool list (§B) and the adapter shape (§E) so the first code written matches them.
- `systemd/`, `caddy/`, `scripts/`, `bench/`, `notes/` READMEs, rewritten to drop every mention of a Foreman or a bus.

Commit and push. Nothing touches hardware, the artifacts, or any external service beyond the repo.

**Sequencing against A–D:** the MCP server (§B) can be built and tested against Ollama on the desktop *before* PW-1x exists — that's the A0 baseline with a real interface on it. The console skeleton and the `claude-code-remote` adapter need nothing from PW-1x either. Both land in D now and get real backends at A5. Screens A/B/C are hardware builds that run in parallel with A1–A4. Hooks cost nothing until used.

## Second implementation step: Systems Map cleanup (all three figures)

**Why.** The Systems Map — https://claude.ai/code/artifact/0d57bcf9-55a9-4eda-87c9-4807749ee677 — is correct but crowded: boxes carry four to six lines of text, two edges are diagonal and one is a bezier, and several labels sit on box borders. It should read at a glance, with the words in the captions and the tables where they belong. Content is unchanged; this is layout only. The file is `scratchpad/systems-map.html`; it is mine, not one of the PW-1x pair.

**Rules, applied to every figure.**

1. **A box is a title and at most two short lines.** Everything else moves to the figcaption or the table under the figure.
2. **Every edge is orthogonal** — horizontal, vertical, or an elbow. No diagonals, no curves.
3. **Every edge has one label, in the gap beside the line, never over a box border.** Where a label sits, the gap is at least 70px.
4. **No crossings.** Nodes sit on a grid: fixed column x-positions, fixed row y-positions, matching widths within a column.
5. **One accent element per figure** — the mechanism that figure is about. Everything else in `currentColor`.
6. Same `viewBox` width (1000) and the same box widths across all three figures so they read as a set.

**Figure 1 — physical.** Trim PW-1x to title + "EPYC 7452 · 128GB · GPU slot open" + "llama.cpp · Podman · Console". Replace the two diagonals (Router → Screen B, Router → printer) with elbows off a shared vertical trunk in the right column, and the storage bezier with an elbow. Align Screen A, the light and the storage hook on one row at equal heights. Internet sits directly above Router; Screens C, B and the printer stack at equal heights beside them.

**Figure 2 — software.** Keep the grid; cut every box to two lines. Shorten the Remote API label to "Remote API" and move the verbs to the caption. Give the dashed batch-job return its own x so its label doesn't compete with the tool-call labels. Screens and Phone to two lines.

**Figure 3 — projects and telemetry.** Make the two circuits mirror: both columns 200/200 with the same gap, wide boxes the same width on both sides. Two lines per box. Keep the "the internet" stub, labeled.

**Captions.** Each figcaption absorbs the detail dropped from its boxes so nothing is lost, and each still opens with its one claim in bold.

**Verification.** Render each figure alone (the `fig-only` pattern already in the scratchpad) at 1100px and look once each; fix any collision found; republish once to the same URL; confirm the page's sweep for stale-design terms still returns nothing.

**Out of scope.** Any content change to the map; anything in the PW-1x artifacts; the repo (the map isn't mirrored there yet).

## Third implementation step: checker docstring

`tools/spec-check.py`'s module docstring still describes five checks over two files. Rewrite it to name all three documents and six checks (the map's orthogonal-edge and superseded-design pass is the sixth). The root `README.md` "Verifying the documents" paragraph says "Five checks" — same fix. Run the checker, commit, push. No behavior change.

## Fourth implementation step: one interface, one door

Bring the repo and the map into line with the corrected design — the console is your single interface, frontier providers are connectors, `studio-local` is the one logged door to local models, and chat-with-local is the `ask` verb. Wording only; no code yet.

- `README.md`, `console/README.md`, `console/adapters/README.md`, `mcp/README.md`: replace every "you work in Claude Code" framing; add the `/v1` face, the `source` column, `/metrics`, localhost binding, and the `ask` verb.
- `docs/systems-map.html` Figure 2: console becomes the hub; Claude Code drawn as a connector; MCP box reads "MCP for Claude · /v1 for everyone else"; lede, caption and callout rewritten. Layout rules from step two still hold.
- `docs/plan.md` synced. Checker clean. Republish the map. Commit, push.

## Verification

- **A0**: Ollama serving `gpt-oss:20b`, harness pointed at it, and a written record of current rate-limit-hit frequency. Nemotron PR status and EPS requirement both answered in `notes/`.
- **A2**: memtest86+ clean across eight modules, dated inside the return window.
- **A4**: IPMI VRM and DIMM temperatures captured under sustained load, recorded in `notes/`.
- **A5**: `curl` against `/v1/models` and a completion round-trip; measured decode and prefill tok/s for gpt-oss-120b and Scout committed to `bench/`, decode compared against its stated ceiling (51 and 14). Once a GPU is installed, the startup log shows CUDA device detection.
- **B**: Claude Code lists the `studio-local` MCP server's tools; a `read_and_brief` call returns and appears in the work log with tool, backend, tokens, latency; a `batch_job` completion wakes a session by webhook; before/after throughput compared against the A0 baseline.
- **C**: `lscpu -e=CPU,CORE` output matches the pinned ranges; `systemctl show llama-server -p AllowedCPUs,MemoryMax` confirms the caps; one site served over HTTPS through Caddy; dev environment reachable over Tailscale with no inbound ports open.
- **D**: `python3 tools/spec-check.py` exits clean in CI against `docs/`.

## Out of scope

Editing either artifact. Both pass their checks as they stand; any content change is a separate, explicit decision.
