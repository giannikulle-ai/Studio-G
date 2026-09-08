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

**A handoff is a verb whose input is another adapter's output.** "Send session 3's result to a new session" is `claude-code-remote.create({ prompt, files: fromResultOf("session-3") })`. The work log records the chain.

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
| `local-models` | call | backends up/down, model loaded | MCP work log | batch job |
| `pw1x` | device | CPU/RAM/temps via Prometheus | alerts | restart llama-server |
| `p2s` | device | print state, progress, temps | MQTT + AI-detection events, camera | pause, resume |
| `usb-light` | device | on/off | — | on, off, auto |
| `github` | service | repos, last push, CI | webhook events | open PR |
| `cloudflare` | service | Pages/Workers deploys, tunnel health | deploy events | redeploy |
| `phone` | outbound | — | — | notify |

## Adding one

1. Copy `_template.ts` to `<id>.ts`.
2. Fill in `kind`, `status`, `events`, `verbs`.
3. Register it in `index.ts`.

That's it. If it speaks HTTP or MQTT, it's an afternoon. Secrets it needs come from the sops-encrypted file, never from the adapter source.
