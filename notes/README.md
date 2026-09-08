# notes/

Facts checked against the real machine, one file each, dated. These answer questions the plan leaves open until hardware exists.

| File | Question it answers | When |
|---|---|---|
| `eps-connector.md` | Does the ROMED8-2T want one 8-pin + one 4-pin, or two 8-pin? The docs source this from a ServeTheHome review only. | Before assembly (A0/A1) |
| `nemotron-pr-20539.md` | Did llama.cpp PR #20539 land stock support for Nemotron 3 Super's NVFP4 quant? | A0 — five-minute check |
| `lscpu.txt` | Which logical CPUs share a physical core. Decides every `AllowedCPUs` line. | Right after OS install (A3) |
| `partitions.md` | The partition layout actually used, including `/var/lib/containers`. | A3 |
| `ipmi-thermals.md` | VRM and DIMM temperatures under sustained load on the open bench. Decides whether a fan is bought. | A4 |
| `memtest.md` | memtest86+ result, all eight modules, dated inside the 30-day return window. | A2 |
| `gpu-purchase.md` | What was bought, at what price, against which measured prefill number. | When it happens |

Facts only. Estimates go in the documents; measurements go in `bench/`.
