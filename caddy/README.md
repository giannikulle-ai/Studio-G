# caddy/

The `Caddyfile` for PW-1x. Lands after OS install (plan §A3).

Three kinds of site block will live here:

- **The Console** — served on the Tailscale interface only. No public route.
- **Grafana kiosk** — same, Tailscale only. Every screen points at one URL here.
- **Hosted sites** — each behind the Cloudflare Tunnel. Caddy terminates locally; Cloudflare Access handles auth at the edge. No inbound port is ever opened on the router.

Caddy gets automatic Let's Encrypt for anything with a public name. Internal names use Tailscale's certificates or plain HTTP on the tailnet.

The static "PW-1x is down" page is **not** here — it lives on Cloudflare Pages so it keeps serving when this box is off.
