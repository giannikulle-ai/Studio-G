# console/adapters/ — one file per connected thing

Every adapter has the same shape. That is the whole design.

```ts
interface Adapter {
  id: string;                          // "claude-code-remote", "p2s", ...
  kind: "session" | "call" | "device" | "service" | "outbound";
  status(): Promise<Status>;           // what it is right now
  events(): AsyncIterable<Event>;      // what it's doing — streamed as SSE
  verbs: Verb[];                       // what it can do, each with an input schema
}

interface Verb {
  name: string;                        // "create", "send", "pause", "notify"
  schema: JSONSchema;                  // what it takes
  run(input: unknown): Promise<Result>;
}
```

The UI renders every adapter from this alone: a card from `status`, a stream from `events`, a button per `verb`. `kind` is a hint the UI uses for layout and the work log uses for the throughput comparison — it doesn't change the shape.

**A handoff is a verb whose input is another adapter's output — and you are the one who runs it, at the console.** "Send session 3's result to a new session" is `claude-code-remote.create({ prompt, files: fromResultOf("session-3") })`; "send local's brief to Claude" is the same verb with `files: fromResultOf("local-models")`. The work log records the chain. Nothing needs to know anything else exists.

## Kinds

| kind | examples | status | events | verbs |
|---|---|---|---|---|
| `session` | Claude Code Remote; another agent product later | live sessions | output stream | create · send · interrupt · schedule · watch |
| `call` | local models via `studio-local`; OpenAI / Gemini if wanted | health, quota, model loaded | call log | call · batch |
| `device` | P2S, USB light, smart plugs, sensors, cameras — or one Home Assistant adapter fronting all of them | state | MQTT / webhook stream | the device's own controls |
| `service` | GitHub, Cloudflare, calendar, email, Notion, Linear, registrar, billing | polled | webhooks where offered | few — open PR, redeploy, acknowledge |
| `outbound` | phone push (ntfy, self-hosted and free; or Pushover) | — | — | `notify(level, text, actions[])` |

An outbound notification's `actions[]` each carry a verb on another adapter. "Act on it from the lock screen" is phone → console → the session or device. The console needs one inbound route reachable from the phone for that — Tailscale, or Cloudflare Access if the phone isn't on the tailnet.

## At launch

| Adapter | kind | status | events | verbs |
|---|---|---|---|---|
| `claude-code-remote` | session | sessions, routines | session output | create, send, interrupt, title, tag, schedule, watch |
| `local-models` | call | backends up/down, model loaded | work log (MCP and `/v1`) | ask, batch job |
| `pw1x` | device | CPU/RAM/temps via Prometheus | alerts | restart llama-server |
| `p2s` | device | print state, progress, temps | MQTT + AI-detection events, camera | pause, resume |
| `usb-light` | device | on/off | — | on, off, auto |
| `github` | service | repos, last push, CI | webhook events | open PR |
| `cloudflare` | service | Pages/Workers deploys, tunnel health | deploy events | redeploy |
| `phone` | outbound | — | — | notify |

## Reserved: hooks for other AIs

Nothing installed; the landing spot is named so adding one is a plug-in, not a redesign.

| Adapter | kind | status | events | verbs | needs |
|---|---|---|---|---|---|
| `agent-other` — another agent product that runs sessions | session | sessions | session output | create, send, interrupt, schedule, watch — identical to `claude-code-remote` | the product's session API; a key in the sops file |
| `openai`, `gemini` — any request/response API | call | quota, model | call log | `ask(instruction, files)`, `batch` | an API key, one line in the sops file |
| another local runtime or box (vLLM, a second machine) | — | — | — | none new | not an adapter: a backend behind `studio-local`, see `../../mcp/README.md` |

**The rule for every frontier connector, Claude included: never a chat box.** You hand it instructions and files and watch. Its calls land in the console's work log. If it can use the local door itself — as Claude does over MCP — that is logged under its own `source`.

## The `ask` verb

`local-models.ask({ model, text, turns })` is chat with local. The card renders a text input and a model picker; the reply streams into the card's events panel. It is one call to `studio-local`'s `/v1` with `source = console` — logged and metered like every other call. Conversation history is the work log; `turns` carries the last N. A `file` input lands as a path reference later. This is the same shape as every other verb, which is the point.

## Adding one

1. Copy `_template.ts` to `<id>.ts`.
2. Fill in `kind`, `status`, `events`, `verbs`.
3. Register it in `index.ts`.

That's it. If it speaks HTTP or MQTT, it's an afternoon. Secrets it needs come from the sops-encrypted file, never from the adapter source.
