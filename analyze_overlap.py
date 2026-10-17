"""Analyse benchmark_results.csv to show coverage overlap between engines."""
import csv
import sys
from itertools import combinations


def load(path="benchmark_results.csv"):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def engines(rows):
    return [k[:-7] for k in rows[0] if k.endswith("_Answer")]


def nonempty(row, engine):
    a = (row.get(f"{engine}_Answer") or "").strip()
    return bool(a) and a != "[Empty]"


def main():
    rows = load(sys.argv[1] if len(sys.argv) > 1 else "benchmark_results.csv")
    engs = engines(rows)
    n = len(rows)

    print(f"Queries: {n}")
    print(f"Engines: {len(engs)}\n")

    # --- Per-engine coverage ---
    print("=== Per-engine coverage ===")
    cov = {e: sum(1 for r in rows if nonempty(r, e)) for e in engs}
    for e in sorted(cov, key=cov.get, reverse=True):
        print(f"  {e:<25} {cov[e]:>3}/{n}  ({cov[e]/n*100:5.1f}%)")

    # --- Union ---
    union = sum(1 for r in rows if any(nonempty(r, e) for e in engs))
    print(f"\n=== Union coverage ===")
    print(f"  At least one engine answered: {union}/{n} ({union/n*100:.1f}%)")
    print(f"  Nobody answered:              {n - union}/{n} ({(n-union)/n*100:.1f}%)")

    # --- Unique contributions ---
    print(f"\n=== Unique contributions (queries ONLY this engine answered) ===")
    for e in engs:
        u = sum(
            1 for r in rows
            if nonempty(r, e) and not any(nonempty(r, o) for o in engs if o != e)
        )
        if u:
            print(f"  {e:<25} {u}")

    # --- Pairwise overlap ---
    print(f"\n=== Pairwise overlap (both engines returned non-empty) ===")
    pairs = []
    for a, b in combinations(engs, 2):
        ov = sum(1 for r in rows if nonempty(r, a) and nonempty(r, b))
        un = sum(1 for r in rows if nonempty(r, a) or nonempty(r, b))
        pairs.append((un, ov, a, b))
    pairs.sort(reverse=True)
    print("  Top pairs by union coverage:")
    for un, ov, a, b in pairs[:10]:
        j = ov / un * 100 if un else 0
        print(f"    {a} + {b}: union {un}/{n}, overlap {ov}, jaccard {j:.0f}%")

    # --- Which pairs are worth combining ---
    print(f"\n=== Best combos (union > best single engine) ===")
    best_single = max(cov.values())
    for un, ov, a, b in pairs[:5]:
        delta = un - best_single
        mark = " ✅" if delta > 0 else ""
        print(f"    {a} + {b}: union {un} (+{delta} over best single){mark}")


if __name__ == "__main__":
    main()
