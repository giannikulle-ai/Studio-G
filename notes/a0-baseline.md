# A0 — desktop baseline

First real numbers for the project. Everything above the line is measured; everything
below it is still owed.

## Measured — 2026-09-13

| | |
|---|---|
| Machine | desktop, RTX 4060 Ti FE |
| VRAM | **8GB** (see correction below) |
| Runtime | Ollama, gpt-oss-20b imported from a local GGUF |
| Placement | `50%/50% CPU/GPU` per `ollama ps` |
| Context | 4096 |
| Decode | **39.05 tok/s** (277 tokens in 7.09 s) |
| Prompt processing | 21.06 tok/s over 43 new tokens — too short to be meaningful, remeasure on a long prompt |
| Model size on disk | 12 GB |

## The correction this produced

The card is **8GB**, not the 16GB stated in the PW-1x Handoff and Build Sheet from
their first revision. NVIDIA made no Founders Edition of the 16GB 4060 Ti, so
"RTX 4060 Ti FE" and "16GB" never described the same real card. Both artifacts were
corrected on 2026-09-13; `tools/spec-check.py` now fails on the old strings.

Consequences, in order of weight:

1. gpt-oss-20b cannot be resident on that card. Twelve gigabytes of weights against
   eight of VRAM, so half its layers run on the desktop's processor.
2. The "50+ tok/s volume tier" estimate is replaced by the measured 39.
3. The desktop is a weak fast tier for this model. PW-1x CPU-only is expected to land
   in the same range, which makes the desktop's contribution close to nothing for the
   20b specifically. It becomes worth having again with a model small enough to sit
   entirely on 8GB, which is roughly an 8B at four-bit.
4. The runtime split drawn in both artifacts assumed a 16GB card inside PW-1x. PW-1x
   has no card at all.

## Still owed before A0 is complete

- [ ] A week of real volume work through the local model: triage, classification,
      diff summaries, first-pass repo reads.
- [ ] The "before" number: rate-limit hits per day on the commercial plan, and the
      rough share of work that is high-volume and low-difficulty. This is the only
      baseline the "roughly double throughput" claim can ever be checked against, and
      the window to record it closes when PW-1x comes up.
- [ ] A prefill figure from a long prompt, not a 43-token one.
- [ ] The same two numbers with the model's reasoning effort turned down, which is the
      largest speed knob on gpt-oss and matters most for exactly the volume work this
      tier is meant to absorb.
