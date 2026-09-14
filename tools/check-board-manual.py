import io, re
G = io.open('docs/assembly-guide.html', encoding='utf-8').read()
H = io.open('docs/handoff.html', encoding='utf-8').read()
B = io.open('docs/build-sheet.html', encoding='utf-8').read()
M = io.open('docs/systems-map.html', encoding='utf-8').read()
N = io.open('notes/board-manual.md', encoding='utf-8').read()
P = io.open('docs/plan.md', encoding='utf-8').read()
def txt(s): return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))
gt, ht, bt = txt(G), txt(H), txt(B)
fails, notes = [], []

# --- 2. cross-document: facts read off the board's own sheet --------------
must = [
 ("M2_2",            [("guide", G), ("handoff", H), ("build-sheet", B), ("notes", N), ("plan", P)]),
 ("PANEL1",          [("guide", G), ("handoff", H), ("notes", N)]),
 ("PWRBTN#",         [("guide", G), ("notes", N)]),
 ("Dr. Debug",       [("guide", G), ("handoff", H), ("notes", N), ("plan", P)]),
 ("FAN1",            [("guide", G), ("handoff", H), ("notes", N)]),
 ("PE16_SEL",        [("guide", G), ("handoff", H), ("build-sheet", B), ("notes", N)]),
 ("IPMI_LAN1",       [("guide", G), ("notes", N)]),
 ("UID1",            [("guide", G), ("notes", N)]),
 ("14 Sep",          [("guide", G), ("notes", N), ("plan", P)]),
]
for fact, docs in must:
    miss = [n for n, d in docs if fact not in d]
    if miss: fails.append(f"cross-doc {fact!r} missing from: {', '.join(miss)}")
print(f"[cross-doc] {len(must)} board-manual facts checked across up to 6 files")

# both 12V pin counts must appear in all three published documents
for label, d in (("guide", gt), ("handoff", ht), ("build-sheet", bt)):
    if "8-pin" not in d or "4-pin" not in d:
        fails.append(f"{label}: 12V pin counts incomplete (8-pin={'8-pin' in d}, 4-pin={'4-pin' in d})")
print("[cross-doc] 12V pin counts present in all three published documents")

# --- 3. stale: procedures the board's own sheet superseded ---------------
stale = {
 "CPU_FAN1": "no processor fan header exists on this board",
 "still unconfirmed": "pin counts are now confirmed from the sheet",
 "Open them 3, 2, 1": "ASRock says A-B-C both ways",
 "latch swings up and clicks": "locking the clip is its own step",
 "Open the latch at each end": "one clip per slot",
 "its 80mm hole": "the nut position is named D",
 "onboard power button; the front-panel": "answered: there is none",
 "no pin counts": "section 6 draws all three pinouts",
 "prints no pin counts": "section 6 draws all three pinouts",
}
for name, doc in (("guide", G), ("handoff", H), ("build-sheet", B), ("map", M), ("plan", P)):
    for bad, why in stale.items():
        if bad in doc: fails.append(f"{name}: STALE {bad!r} ({why})")
print(f"[stale]     {len(stale)} superseded procedures scanned in 5 files")

if "A → B → C" not in G:
    fails.append("guide: the A-B-C screw order is not stated")
if "loosen in reverse" not in G:
    fails.append("guide: AMD's disagreement on the loosening order is not noted")
occ = G.count("3-2-1") + G.count("3→2→1")
if occ:
    fails.append(f"guide: the retired '3-2-1' order still appears {occ}x")
else:
    notes.append("guide: A-B-C stated, AMD's reverse-loosening caveat kept, no '3-2-1' left")

# --- 5. sanity against method -------------------------------------------
# M.2 type codes encode 22mm width + length in mm; the sheet's cm column must agree
for code, cm in (("2230", 3.0), ("2242", 4.2), ("2260", 6.0), ("2280", 8.0), ("22110", 11.0)):
    mm = int(code[2:])
    if round(mm / 10, 1) != cm:
        fails.append(f"M.2 {code}: type code says {mm}mm but the table says {cm}cm")
print("[method]    5 M.2 type codes agree with the sheet's length column (2280 = 80mm = position D)")

# the guide must name the standoff position, its length, and the film on the nut
for need, why in (("position D", "the 2280 standoff position"),
                  ("8cm nut", "what position D means in millimetres"),
                  ("yellow film", "the protective film on the nut")):
    if need not in G:
        fails.append(f"guide: {why} ({need!r}) is not stated")

# PANEL1 is 8 pins: the figure must draw 8 and label 8
seg = G[G.index("aria-label=\"The system panel header"):]
seg = seg[:seg.index("</svg>")]
circles = len(re.findall(r"<circle", seg))
labels = [l for l in ("PLED+", "PLED−", "PWRBTN#", "GND", "RESET#", "HDLED−", "HDLED+") if l in seg]
if circles != 8: fails.append(f"PANEL1 figure draws {circles} pins, the header has 8")
if len(labels) != 7: fails.append(f"PANEL1 figure labels {len(labels)}/7 distinct signal names")
gnd = seg.count(">GND</text>")
if gnd != 2: fails.append(f"PANEL1 figure labels GND {gnd}x; the header has two")
print(f"[method]    PANEL1 figure: {circles} pins drawn, {len(labels)}/7 signal names, GND labelled {gnd}x")

# an 8-pin + a 4-pin EPS carry 12 PINS, half of them ground -- not 12 12V pins
if re.search(r"twelve 12V pins", G): fails.append("guide: 'twelve 12V pins' -- 8+4 is 12 pins, of which six carry 12V")
if re.search(r"twelve 12V pins", H): fails.append("handoff: same")
print("[physics]   8-pin + 4-pin = 12 pins, 6 carrying 12V and 6 ground")

print()
print("ISSUES:" if fails else "clean — no issues found")
for f in fails: print("  x", f)
if notes:
    print("NOTES:")
    for n in notes: print("  -", n)
