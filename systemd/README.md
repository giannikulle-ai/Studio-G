# systemd/

Unit files and resource-control drop-ins for PW-1x. Lands after OS install (plan §A3), before anything is hosted.

What will live here:

- `llama-server.service` — the inference server. The drop-in `limits.conf` pins it to logical CPUs `0-11,32-43` with `MemoryMax=76G`. The Handoff's config is correct and goes in verbatim.
- `studio-hosting.slice` — the slice every container runs under: CPUs `12-31,44-63`, `MemoryMax=40G`.
- `usb-light.service` — the alert-webhook receiver that toggles the relay.
- `studio-mcp.service` — the `studio-local` MCP server (`mcp/`), in the hosting slice.
- `studio-console.service` — the control room (`console/`), in the hosting slice.

**Before writing any `AllowedCPUs` line**, run `lscpu -e=CPU,CORE` on the real machine and save the output to `notes/`. Sibling enumeration varies by kernel and BIOS. Pinning a core without its sibling isolates nothing.

Caps must not sum above 128GB. 76 + 40 leaves 12 for the host and page cache. Above that, the OOM killer picks, and it will pick the 63GB process.
