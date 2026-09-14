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
