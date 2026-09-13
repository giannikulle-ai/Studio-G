# Delivery — all parts in hand

**Confirmed in hand: 13 September 2026.** Reported by the owner; not read off a carrier
tracking page. Everything in the Build Sheet's bill of materials is physically present.

| Part | Line | State |
|---|---|---|
| AMD EPYC 7452 | owned earlier | in hand |
| ASRock Rack ROMED8-2T | owned earlier | in hand |
| G-DRIVE mobile USB-C (0G10265) | owned earlier | in hand |
| A-Tech 128GB kit — 8 × 16GB DDR4-3200 ECC RDIMM 2Rx8 | $1,315.69 | in hand |
| ARCTIC Freezer 4U-M Rev. 2 (ACFRE00133B) | $57.92 | in hand |
| MSI MPG A850G PCIE5 | $89.99 | in hand |
| Kingston NV3 1TB (SNV3S/1000G) | $156.99 | in hand |

Nothing outstanding. Total $2,240.59, or $2,230.59 if the $10 PSU rebate lands.

## The clock this starts

The memory kit is the only part with a return window: **30 days, counted from the
vendor's delivery date.**

- Counted from 13 September 2026, the last day is **13 October 2026**.
- That is the *latest* it can be. The window runs from delivery, which may predate
  the day the boxes were opened and confirmed here.
- **Action: read the delivery date off the A-Tech invoice and write it in below.**
  Work to that date, not to the one computed above.

```
invoice delivery date: ____________
window closes:         ____________
```

What has to finish inside the window: assemble (A1), then memtest86+ across all eight
modules, full passes overnight (A2). A faulty stick found inside the window is a
defective-product return the vendor pays for. The same stick found afterwards is a
warranty claim needing a *matched* replacement on a 1DPC board, or replacing all eight.

`docs/assembly-guide.html` is the procedure; step 10 is the test. Record the result in
`memtest.md`.

## Before opening anything else

The board and the processor were bought used and neither is returnable. Inspect the
SP3 socket contact field and the processor's pads before assembly night — the
assembly guide's third inventory table has the method. A fault found now still leaves
four weeks inside the memory window to get a replacement board in and test the kit.
