# mcp/ — `studio-local`

The MCP server that makes PW-1x's local models into tools Claude calls. This is the whole "tiered routing" layer: Claude decides what to delegate, local does the bulk, and only a compact result comes back into Claude's context.

**Direction:** frontier manages, local works. Claude is the brain; this server is the hands. It never decides *what* to do — only *how* to do the thing it was asked, and on which backend.

## Tools

| Tool | Shape | What it does |
|---|---|---|
| `read_and_brief(paths \| git_ref, question)` | call | The bulk-read primitive. Reads whatever it's pointed at, answers the question in a page. Claude gets the page, not the files. |
| `summarize(text \| path)` | call | Volume work. |
| `classify(text, labels[])` | call | Volume work. |
| `extract(text, schema)` | call | Volume work, structured output. |
| `batch_job(spec) → job_id` | async | Long-running work. Returns immediately. |
| `job_status(job_id)` | call | Queued / running / done / failed. |
| `job_result(job_id)` | call | The output, once done. |

When a batch job finishes, this server POSTs to the webhook URL the session registered, and Claude wakes and continues. That is how "have them talk to each other" works for overnight work — no queue beyond the job table.

## Backends

The server picks. Claude never sees which.

| Backend | Where | When |
|---|---|---|
| Ollama, gpt-oss-20b | the desktop's 4060 Ti, over 10GbE | Call-shaped volume work, **best-effort** — first choice when the PC is idle, skipped without complaint when it isn't (Ollama's idle unload means it yields naturally) |
| llama.cpp, gpt-oss-120b / Scout | PW-1x, `/v1`, CPU-only until a GPU is bought | Reads and briefs, anything the small model shouldn't do, and the fallback for everything |

Once PW-1x has a GPU, gpt-oss-20b and the 120b **swap** on that card — they don't coexist. This server owns that decision.

## Work log

Every call is logged to SQLite: tool, backend, tokens in/out, latency, whether it fell back. The console's `local-models` adapter reads it. The before/after throughput comparison against the A0 baseline is computed from it. Without this log the "double throughput" claim can't be checked.

## Build order

This can be built and tested **before PW-1x exists** — against Ollama on the desktop. That's the A0 baseline with a real interface on it. Point Claude Code at it over Tailscale (or localhost while developing), confirm the tools appear, confirm a `read_and_brief` round-trips and lands in the log. PW-1x becomes a second backend when it's up.

Stack: Node/TypeScript, the official MCP SDK, SQLite. The `mcp-builder` skill covers the conventions.
