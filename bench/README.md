# bench/

Measured numbers. The documents carry estimates; this directory is what replaces them.

## What gets recorded

For each model, on each configuration, from the first real run (plan §A5):

- **Decode tok/s** at steady state, batch 1
- **Prefill tok/s** on a 32k-token context — this is the number that decides the GPU purchase
- Configuration: llama.cpp commit, build flags (CPU-only / CUDA), `-b`, `-ub`, `-c`, and `--n-cpu-moe` once a GPU exists
- `lscpu`, RAM, and which CPUs the server was pinned to

## The ceilings to compare against

| Model | Stated ceiling | Stated estimate |
|---|---|---|
| gpt-oss-120b | 51 tok/s | 17–25 |
| Llama 4 Scout | 14 tok/s | 8–11 |

If a measured decode number lands **above** its ceiling, the bandwidth figure or the active-parameter accounting in the documents is wrong. Investigate before celebrating.

## Also here

The A0 baseline: current rate-limit hits per day on the commercial plan, recorded **before** PW-1x exists. Without it the "roughly double throughput" claim can never be checked.

Format: one Markdown file per run, dated, with the raw `llama-bench` or `llama-server` log attached. No summaries without the log.
