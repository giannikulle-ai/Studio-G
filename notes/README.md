# notes/

Facts checked against the real machine, one file each, dated. These answer questions the plan leaves open until hardware exists.

| File | Question it answers | When |
|---|---|---|
| `delivery.md` | When did every part land, and when does the memory's 30-day return window close? | On delivery — done 13 Sep 2026 |
| `board-manual.md` | What does the board's own printed Quick Installation Guide settle — power button, fan headers, POST codes, the M.2 jumper trap? | On delivery — done 14 Sep 2026 |
| `eps-connector.md` | Is `ATX12V2` required or optional? The quick guide names both 12V connectors but prints no pin counts and no requirement; needs the full User's Manual. | Before assembly (A0/A1) |
| `nemotron-pr-20539.md` | Did llama.cpp PR #20539 land stock support for Nemotron 3 Super's NVFP4 quant? | A0 — five-minute check |
| `lscpu.txt` | Which logical CPUs share a physical core. Decides every `AllowedCPUs` line. | Right after OS install (A3) |
| `partitions.md` | The partition layout actually used, including `/var/lib/containers`. | A3 |
| `ipmi-thermals.md` | VRM and DIMM temperatures under sustained load on the open bench. Decides whether a fan is bought. | A4 |
| `memtest.md` | memtest86+ result, all eight modules, dated inside the 30-day return window. | A2 |
| `gpu-purchase.md` | What was bought, at what price, against which measured prefill number. | When it happens |

Facts only. Estimates go in the documents; measurements go in `bench/`.
