# ROMED8-2T — what the printed Quick Installation Guide answers

Source: the sheet in the board's box. **P/N 15G065246001AK V1.3**, "Quick Installation
Guide, ROMED8-2T / ROMED8-NL", ASRock Rack. Read **14 September 2026**. Photographed;
every fact below is read off that sheet, not inferred.

The sheet's own first line: the full **User's Manual** is a download from
asrockrack.com. Several things below still need it.

## Answered — these were open questions in the assembly guide

| Question | Answer |
|---|---|
| Onboard power button? | **No.** The layout legend is a complete list of 44 headers and jumpers, plus eight rear-panel items. No power button appears. The board's only buttons are `UID1` (rear panel, an identification light) and `NMI_BTN1`. |
| Front-panel header name | **`PANEL1`** — "System Panel Header", callout 23. `AUX_PANEL1` (24) sits beside it. |
| Fan header names | **`FAN1`–`FAN7`, and every one is a "System Fan Connector".** There is no processor fan header on this board. `FAN1`/`FAN2`/`FAN3` (callouts 7, 9, 11) are the group nearest the socket; `FAN4`–`FAN7` (17–20) sit further out. |
| Beep / LED codes | The board carries a **Dr. Debug** two-digit POST-code display (printed on the layout near `TPM1`), and a `SPEAKER1` header (22). **No speaker was bought**, so there will be no beeps — the display is the whole signal. |
| Board form factor | **24.4 × 30.5 cm (9.6 × 12 in)** — full ATX. Socket silkscreened `LGA4094 Socket SP3`. |

## Found here, on nobody's list — the M.2 trap

The sheet's **section 4, Jumper Settings (PE8_SEL / PE16_SEL)**, is a four-row table over
the columns `PCIE2`, `M2_1`, `SATA_4_7`, `OCU1 & OCU2`:

| PE8_SEL | PE16_SEL | PCIE2 | M2_1 | SATA_4_7 | OCU1 & OCU2 |
|---|---|---|---|---|---|
| 1-2 | 1-2 | ✓ (x16) | ✗ | ✗ | ✗ |
| 1-2 | 2-3 | ✓ (x8) | ✓ | ✓ | ✗ |
| 2-3 | 2-3 | ✗ | ✓ | ✓ | ✓ |
| 2-3 | 1-2 | ✗ | ✗ | ✗ | ✓ |

So **`M2_1` is live only when `PE16_SEL` is on pins 2-3**, and in the other two positions a
drive in it does not exist — no error, no light, nothing in the BIOS. The sheet does not
say which position the board ships in.

**`M2_2` is not in that table at all**, so no jumper can take it away, and it accepts
lengths up to 22110 where `M2_1` stops at 2280. **The Kingston NV3 goes in `M2_2`.** That
sidesteps the whole question and costs nothing.

## Power connectors

Callouts 2, 3, 4: `ATX12V1` and `ATX12V2` (both labelled "ATX 12V Power Connector") and
`ATXPWR1` ("ATX Power Connector"), all three along the top edge beside `PSU_SMB1`.

**The quick guide prints no pin counts and does not say whether `ATX12V2` is required.**
The 24-pin / 8-pin / 4-pin figures the documents quote come from the User's Manual's
connector list, not from this sheet. Populating both 12V connectors is correct under
either reading, and the supply's two EPS 4+4 cables cover it. Question stays open.

## Rear I/O panel, in the sheet's own numbering

1 `UID1` switch · 2 `VGA1` · 3 `COM1` serial · 4 USB 3.2 Gen1 ×2 (`USB3_1_2`) ·
5 `IPMI_LAN1` management RJ-45 · 6 `LAN1` 10G · 7 `LAN2` 10G · 8 `USB31_TC_1` Type-C.

The management port is the network port that is *not* one of the 10G pair. The small
button is `UID1`, not power.

## Handling precautions, quoted

The sheet lists five. Two change the build procedure:

1. "Unplug the power cord from the wall socket before touching any components."
2. "…NEVER place your server board directly on the carpet or the like. Also remember to
   use a grounded wrist strap or touch a safety grounded object before you handle the
   components."

The assembly guide previously had the AC cord plugged in from step 0 to ground the
supply's shell. **Corrected 14 Sep 2026:** the cord now goes in at step 7, and the wrist
strap is the primary grounding method.

## Other names worth having

`SATA_0_3` and `SATA_4_7` are the two Mini-SAS HD connectors (8 SATA via breakout).
`OCU1`/`OCU2` OCuLink x4. `GFX_12V1` auxiliary graphics power — stays empty.
`CLRMOS1` is a clear-CMOS **pad**, not a jumper. `USB3_3_4` internal USB header.
DIMM slots `DDR4_A1`–`DDR4_H1`, two banks of four around the socket.
Chips: Intel X550 (or Broadcom BCM57416) for the 10G pair, ASPEED AST2500 for the BMC.

## Still open — needs the full User's Manual

- The **`PANEL1` pinout**: which two pins are the power switch.
- The **Dr. Debug code table**.
- Whether the DIMM slots latch at **both ends or one**.
- Whether **`ATX12V2` is required or optional**.

Unrelated to the board, still open: whether the ARCTIC cooler's two fans share one lead
or use two (answered by the cooler's box, not this sheet).

---

# Back of the same sheet — read 14 September 2026

Sections 5 to 10. This side is procedures rather than names, and it closes almost
everything the front side left open.

## Section 5, Install the Processor and Heatsink — a contradiction

> "Locate the three torx screws on the CPU socket and unscrew them according to the
> order **A→B→C**." … "Close the bracket that holds the CPU. Close the retention cover.
> Fasten the torx screw according to the order **A→B→C**."

**ASRock says the same order in both directions.** AMD's SP3 documentation numbers the
screws 1/2/3 and says tighten 1→2→3, loosen 3→2→1. The guide followed AMD until now.

Both agree on **fastening ascending**, which is the direction that seats the processor
evenly. They differ only on loosening, where nothing is being seated. The guide now
follows the sheet that came with the board and says so, with the disagreement stated.

Also on this side, and previously missing from the guide:

- **"Open the second bracket. Take out the internal plastic cover."** A protective
  plastic insert ships in the rail frame and must come out before the processor goes in.
- **"Install CPU along with the carrier frame, do not separate them"** — printed twice,
  once in a warning triangle. Consistent with what the guide already said.
- "We recommend using the CPU Installation tool to avoid CPU pin-bent problem."
- No torque figure is given. AMD's 1.58 ± 0.1 N·m stands, attributed to AMD.

## Section 6, Install the Power Cables — pin counts confirmed

The section draws all three connectors with full pinouts: a **24-pin**, an **8-pin 12V**,
and a **4-pin 12V**. So `ATXPWR1` 24-pin / `ATX12V1` 8-pin / `ATX12V2` 4-pin is now the
board's own statement, not a figure borrowed from the User's Manual.

**Still not stated in words:** whether the 4-pin is mandatory. It is drawn as part of
power installation. Both get populated; the question is now cosmetic.

## Section 7, Install the Memory — one clip

1. "Unlock a DIMM slot by pressing the module clip outward."
2. "Insert the memory module."
3. "Lock the clip."

The drawings show **a single clip at one end**, not a latch at both. And locking it is
**its own numbered step** — so the guide no longer tells you the latch closes itself.

## Section 8, LAN Port LED Indications

| Port | Activity/Link LED | Speed LED |
|---|---|---|
| `IPMI_LAN1` | off = no link · blinking yellow = traffic · on = link | off = 10 Mbps or no link · yellow = 100 Mbps · green = 1 Gbps |
| `LAN1` / `LAN2` (ROMED8-2T) | same | off = 100 Mbps or no link · **off** = 1 Gbps (yellow on R3.0X) · green = **10 Gbps** |

Useful beyond the build: **green on `LAN1` is the test for whether the desktop link
actually negotiated 10GbE**, which was an open decision in the guide's third table. Note
the trap — on the 10G ports a dark speed LED with a live link means 1 Gbps, not a fault.

## Section 9, Headers — the `PANEL1` pinout

System Panel, eight pins in two rows of four, pin 1 marked at the lower left:

```
 PLED+   PLED−   PWRBTN#   GND
 GND     RESET#  HDLED−    HDLED+
```

**The power button is `PWRBTN#` and the `GND` beside it on the same row.** Short them
for about a second. `RESET#` + its `GND` is the reset pair.

The sheet also prints pinouts for `AUX_PANEL1` (SMB, locator, chassis-open, LAN link
LEDs, `+3V5B`/`+5VSB`), `TPM-SPI` and `RDS1`. **`AUX_PANEL1` carries standby power** —
it is the header next to `PANEL1` and must not be confused with it.

## Section 10, M.2 SSD Module Installation — nut positions

| Position | A | B | C | D | E |
|---|---|---|---|---|---|
| Length | 3 cm | 4.2 cm | 6 cm | 8 cm | 11 cm |
| Type | 2230 | 2242 | 2260 | 2280 | 22110 |

`M2_1` has A–D; `M2_2` has A–E. **The Kingston 2280 uses position D.**

Procedure notes worth having:

- Step 3: **"Peel off the yellow protective film on the nut."** Hand-tighten the standoff.
- Step 5: "Please do not overtighten the screw."

## What is left

Only the **Dr. Debug code table**, and the word "required" next to `ATX12V2`. Both are in
the full User's Manual; neither blocks assembly.
