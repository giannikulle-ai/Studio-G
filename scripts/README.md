# scripts/

Build and helper scripts. Each lands when its step in the plan arrives.

| Script | When | What |
|---|---|---|
| `build-llama-cpp.sh` | A5 | Builds llama.cpp. **CPU-only until a GPU is bought** — the 4060 Ti stays in the desktop. Pins the commit. Re-run with CUDA once a card is installed. |
| `fetch-model.sh` | A5 | Pulls a GGUF to the NVMe, verifies its checksum, records size in `bench/`. |
| `kiosk.sh` | Screen builds | Runs on each Pi. Health-checks PW-1x every 30s and swaps the browser between the Grafana kiosk URL and the static "down" page on Cloudflare Pages. |
| `usb-light.sh` | After telemetry | Webhook target for the Prometheus alert. Toggles the relay. |
| `p2s-exporter/` | When the P2S arrives | Subscribes to the printer's MQTT in Developer Mode, exposes Prometheus metrics. |

Nothing here is written yet. The plan describes each; the machine has to exist first.
