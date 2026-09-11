#!/usr/bin/env python3
"""spec-check — mechanical verification of the Studio-G documents.

Reading a document back does not find its errors. This does. It runs six
checks over docs/handoff.html, docs/build-sheet.html, docs/systems-map.html
and docs/assembly-guide.html and exits non-zero on any failure, so CI catches
drift the moment a price, a part, or a drawing changes.

  1. Arithmetic        every printed total equals the sum of its line items
                       (Handoff, Build Sheet)
  2. Cross-document    facts the Handoff and Build Sheet share appear in both;
                       the Assembly Guide's part numbers and prices match the
                       Build Sheet
  3. Stale strings     retired values are gone from every corner of both; the
                       Assembly Guide carries no GPU-in-PW-1x language
  4. Structure         tags balance; every class used has a stylesheet rule
                       (all four documents)
  5. Systems Map       every edge is orthogonal — no diagonal lines, no curve
                       commands — and no words from the superseded design
                       survive outside a sentence that names it as replaced
  6. Physics / method  model sizes are physically possible; stated throughput
                       ceilings match the stated formula

Update the fact tables below when the documents legitimately change.
Run:  python3 tools/spec-check.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# --------------------------------------------------------------------------
# Facts. These are the numbers the documents are supposed to agree on.
# Change them here first, then the documents, then run this.
# --------------------------------------------------------------------------

LINE_ITEMS = {"memory": 1315.69, "cooler": 57.92, "psu": 89.99, "ssd": 156.99}
SUNK = 620.00
REBATE = 10.00
PRINTED_ORDERED = 1620.59
PRINTED_TOTAL = 2240.59
PRINTED_REBATED = 2230.59
PRINTED_REMAINING = 304.90          # cooler + psu + ssd
MEM_CAPS_GB = {"inference": 76, "hosting": 40, "host_reserve": 12}
MEM_TOTAL_GB = 128

# Strings that must appear in BOTH documents.
SHARED = [
    "1,620.59", "2,240.59", "2,230.59", "1,315.69", "57.92", "89.99", "156.99",
    "12.1GB", "243GB", "122GB", "68GB", "63GB", "65GB",
    "17–25", "8–11", "50+", "60.47", "20504", "20539", "Unresolved",
    "0–11, 32–43", "12–31, 44–63", "76GB", "40GB", "12GB", "lscpu -e",
    "judgement rather than measurement", "ceilings are arithmetic",
]

# Strings that must appear in NEITHER document (superseded values).
STALE = [
    "1,610.59", "294.90", "95–100GB", "8–13",
    'MemoryMax</span>=<span class="v">80G', "Live options",
    '"chip stop">Blocked', 'AllowedCPUs</span>=<span class="v">0-11<',
    "Throughput figures are arithmetic", "Tok/s are arithmetic",
    "# arithmetic only", "arithmetic only; no benchmark",
]

# Strings the Assembly Guide must share with the Build Sheet (part numbers,
# prices, the platform facts the guide restates).
GUIDE_SHARED = [
    "ACFRE00133B", "SNV3S/1000G", "0G10265", "1,315.69", "57.92", "89.99",
    "156.99", "EPYC 7452", "ROMED8-2T", "no SATA", "30-day",
]

# The guide describes a CPU-only build. None of this belongs in it.
GUIDE_STALE = ["CUDA", "n-cpu-moe", "-ngl", "graphics card cable", "into the x16 slot"]

# Model footprints: (name, size_gb, total_params_b, min_bits, max_bits)
MODELS = [
    ("gpt-oss-120b", 63, 117, 3.8, 5.0),
    ("llama-4-scout", 65, 109, 4.0, 5.2),
    ("gpt-oss-20b", 12.1, 21, 4.0, 5.2),
    ("nemotron-3-super", 68, 120, 4.0, 5.2),
    ("llama-4-maverick", 243, 400, 4.3, 5.2),
]

# Stated throughput ceilings: (name, size_gb, total_b, active_b, stated_ceiling)
BANDWIDTH_GBS = 140.0
CEILINGS = [
    ("gpt-oss-120b", 63, 117, 5.1, 51),
    ("llama-4-scout", 65, 109, 17, 14),
]

TAGS = ("table", "thead", "tbody", "tfoot", "section", "pre", "div",
        "ul", "ol", "tr", "td", "th", "header", "footer", "nav")

# Systems Map: words from the design this replaced. A hit is fine only when
# the surrounding text is explaining that it was replaced.
MAP_STALE = [r"\bforeman\b", r"handoff bus", r"work item", r"three (execution )?tiers"]
MAP_STALE_OK = ["was backwards", "first draft", "direction backwards", "is gone", "no bus"]

# --------------------------------------------------------------------------


def strip(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html))


def main() -> int:
    try:
        H = (DOCS / "handoff.html").read_text(encoding="utf-8")
        B = (DOCS / "build-sheet.html").read_text(encoding="utf-8")
        M = (DOCS / "systems-map.html").read_text(encoding="utf-8")
        G = (DOCS / "assembly-guide.html").read_text(encoding="utf-8")
    except FileNotFoundError as e:
        print(f"missing document: {e.filename}")
        return 2

    ht, bt, gt = strip(H), strip(B), strip(G)
    fails, notes = [], []

    # 1. arithmetic --------------------------------------------------------
    ordered = round(sum(LINE_ITEMS.values()), 2)
    total = round(SUNK + ordered, 2)
    rebated = round(total - REBATE, 2)
    remaining = round(LINE_ITEMS["cooler"] + LINE_ITEMS["psu"] + LINE_ITEMS["ssd"], 2)
    caps = sum(MEM_CAPS_GB.values())
    for label, got, want in [
        ("ordered", ordered, PRINTED_ORDERED),
        ("total", total, PRINTED_TOTAL),
        ("rebated total", rebated, PRINTED_REBATED),
        ("remaining parts", remaining, PRINTED_REMAINING),
        ("memory caps", caps, MEM_TOTAL_GB),
    ]:
        if got != want:
            fails.append(f"arith {label}: computed {got} != printed {want}")
    print(f"[arith]     ordered={ordered} total={total} rebated={rebated} "
          f"remaining={remaining} caps={caps}/{MEM_TOTAL_GB}")

    # 2. cross-document ----------------------------------------------------
    ok = 0
    for k in SHARED:
        a, b = k in ht, k in bt
        if a and b:
            ok += 1
        else:
            fails.append(f"cross-doc {k!r}: handoff={a} build-sheet={b}")
    print(f"[cross-doc] {ok}/{len(SHARED)} shared facts present in both")
    gok = 0
    for k in GUIDE_SHARED:
        a, b = k in gt, k in bt
        if a and b:
            gok += 1
        else:
            fails.append(f"guide/build-sheet {k!r}: guide={a} build-sheet={b}")
    print(f"[cross-doc] {gok}/{len(GUIDE_SHARED)} guide facts match the build sheet")

    # 3. stale -------------------------------------------------------------
    for name, doc in (("handoff", H), ("build-sheet", B)):
        for bad in STALE:
            if bad in doc:
                fails.append(f"{name}: STALE {bad!r}")
    m = re.search(r"gpt-oss-20b.{0,300}?size_gb.{0,60}?>([\d.]+)<", H, re.S)
    if m and m.group(1) != "12.1":
        fails.append(f"handoff Layer 3 gpt-oss-20b size_gb={m.group(1)} (table says 12.1)")
    print(f"[stale]     {len(STALE)} retired strings scanned in both")
    for bad in GUIDE_STALE:
        if bad in G:
            fails.append(f"assembly-guide: GPU-build language {bad!r}")
    print(f"[stale]     {len(GUIDE_STALE)} GPU-build strings scanned in the guide")

    # 4. structure ---------------------------------------------------------
    for name, doc in (("handoff", H), ("build-sheet", B), ("systems-map", M),
                      ("assembly-guide", G)):
        for tag in TAGS:
            o = len(re.findall(r"<" + tag + r"[\s>]", doc))
            c = len(re.findall(r"</" + tag + r">", doc))
            if o != c:
                fails.append(f"{name}: <{tag}> {o} open / {c} close")
        used = {c for g in re.findall(r'class="([^"]+)"', doc) for c in g.split()}
        unstyled = sorted(c for c in used
                          if not re.search(r"\." + re.escape(c) + r"[\s,{:.]", doc))
        for c in unstyled:
            fails.append(f"{name}: .{c} used but not styled")
        print(f"[structure] {name}: {len(TAGS)} tag types checked, "
              f"{len(used)} classes used, {len(unstyled)} unstyled")

    # 5. systems map: orthogonal edges, no superseded-design words ----------
    diag = 0
    for l in re.findall(r"<line[^>]*>", M):
        g = re.search(r'x1="(\d+)" y1="(\d+)" x2="(\d+)" y2="(\d+)"', l)
        if g and g.group(1) != g.group(3) and g.group(2) != g.group(4):
            diag += 1
    curves = [d for d in re.findall(r'\bd="([^"]+)"', M)
              if not d.startswith("M0,0 L10,5") and re.search(r"[CcSsQqTtAa]", d)]
    if diag:
        fails.append(f"systems-map: {diag} diagonal <line> edge(s)")
    if curves:
        fails.append(f"systems-map: {len(curves)} curved <path> edge(s)")
    for bad in MAP_STALE:
        for hit in re.finditer(bad, M, re.I):
            ctx = M[max(0, hit.start() - 80): hit.end() + 40].lower()
            if not any(ok in ctx for ok in MAP_STALE_OK):
                fails.append(f"systems-map: superseded design word {bad!r}")
                break
    print(f"[map]       edges: {diag} diagonal, {len(curves)} curved; "
          f"{len(MAP_STALE)} superseded terms scanned")

    # 6. physics / method --------------------------------------------------
    for name, gb, bn, lo, hi in MODELS:
        bits = gb * 8.0 / bn
        if not lo <= bits <= hi:
            fails.append(f"{name}: {bits:.2f} bits/param outside {lo}–{hi}")
    for name, gb, bn, act, stated in CEILINGS:
        per_tok = act * (gb / bn)
        ceil = BANDWIDTH_GBS / per_tok
        if abs(ceil - stated) > 1.0:
            fails.append(f"{name}: ceiling {ceil:.1f} tok/s != stated {stated}")
        print(f"[physics]   {name}: {act}B active × {gb/bn:.3f} GB/B = "
              f"{per_tok:.2f} GB/tok → ceiling {ceil:.1f} (doc says {stated})")
    notes.append("maverick IQ1_S: 122GB over 400B = 2.44 bits/param vs the "
                 "'1.78-bit' label — upstream quant naming, not a defect")

    # report ---------------------------------------------------------------
    print()
    if fails:
        print("ISSUES:")
        for f in fails:
            print("  x", f)
    else:
        print("clean — no issues found")
    if notes:
        print("NOTES:")
        for n in notes:
            print("  -", n)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
