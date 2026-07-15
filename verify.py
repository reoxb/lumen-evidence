#!/usr/bin/env python3
"""
Recompute every number in the LUMEN validation dossier, from the labeled data.

The dossier asks you not to trust it. This is how you don't: this script reads
the hand-labeled CSVs in this repository and prints the precision and recall
table from scratch. If its output disagrees with the published page, the page is
wrong.

No dependencies. Python 3.8+.

    python3 verify.py
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent

# Which labeled CSV is authoritative for which rules. GENERATED from the auditor's
# EVIDENCE_MANIFEST (`npm run evidence`) — do not hand-edit. It holds POINTERS, never
# numbers, and it is the same list the dossier and the ledger check answer to, so the
# three cannot drift apart (they did once: 2026-07-13n).
# PUBLIC TIER ONLY (decision 004): this list carries the commodity families. The
# differentiated families' labels ship in the evaluator bundle, whose own copy of
# this script carries their SOURCES and recomputes them the same way.
SOURCES = [
    ("validation/2026-07-14u/validation_labeling.csv", "2026-07-14u", None, None),
    ("validation/2026-07-12c/baseline_labeling.csv", "2026-07-12c", "diagnosis", "validation/2026-07-13n/security_baseline_labeling.csv"),
]

MARKED = {"x", "1", "yes", "true"}


def marked(value: str) -> bool:
    return value.strip().lower() in MARKED


def main() -> int:
    rules = {}
    total_rows = 0

    current_prec = {}
    for rel, record, kind, current_rel in SOURCES:
        path = ROOT / rel
        if not path.exists():
            print(f"MISSING: {rel}", file=sys.stderr)
            return 1

        agg = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                rule = row["ruleId"]
                total_rows += 1
                if marked(row["true_positive"]):
                    agg[rule]["tp"] += 1
                elif marked(row["false_positive"]):
                    agg[rule]["fp"] += 1
                elif marked(row["false_negative"]):
                    agg[rule]["fn"] += 1
                else:
                    # A half-labeled set produces a metric that looks complete
                    # and is wrong. Refuse it.
                    print(f"UNLABELED ROW in {rel}: {row.get('finding_id','?')}", file=sys.stderr)
                    return 1

        for rule, c in agg.items():
            rules[rule] = dict(c, record=record, kind=kind)

        if current_rel is not None:
            cagg = defaultdict(lambda: {"tp": 0, "fp": 0})
            cpath = ROOT / current_rel
            if not cpath.exists():
                print(f"MISSING: {current_rel}", file=sys.stderr)
                return 1
            with cpath.open(newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    if marked(row["true_positive"]):
                        cagg[row["ruleId"]]["tp"] += 1
                    elif marked(row["false_positive"]):
                        cagg[row["ruleId"]]["fp"] += 1
            for rule, c in cagg.items():
                if c["tp"] + c["fp"]:
                    current_prec[rule] = c["tp"] / (c["tp"] + c["fp"])

    print()
    print("  LUMEN — validation evidence, recomputed from the labeled CSVs")
    print(f"  {total_rows} hand-labeled findings")
    print()
    print(f"  {'RULE':<40}{'TP':>6}{'FP':>5}{'FN':>5}{'PRECISION':>16}{'RECALL':>9}  RECORD")
    print("  " + "-" * 92)

    for rule in sorted(rules):
        c = rules[rule]
        tp, fp, fn = c["tp"], c["fp"], c["fn"]
        prec = tp / (tp + fp) if tp + fp else None
        rec = tp / (tp + fn) if tp + fn else None

        # A source marked "diagnosis" is a PRE-fix labeling: its false positives
        # were the bug, and they were fixed. The dossier prints both numbers and
        # says which is which; so does this.
        if c["kind"] == "diagnosis" and fp > 0 and rule in current_prec:
            p = f"{prec:.3f} -> {current_prec[rule]:.3f}"
        else:
            p = f"{prec:.3f}" if prec is not None else "—"

        r = f"{rec:.3f}" if rec is not None else "—"
        print(f"  {rule:<40}{tp:>6}{fp:>5}{fn:>5}{p:>16}{r:>9}  {c['record']}")

    print()
    print("  A row printed as `0.243 -> 1.000` is a rule whose false positives we found in")
    print("  our own tool and fixed. The left number is what it actually scored when we")
    print("  labeled it; the right is COMPUTED from the current artifact above. Both are")
    print("  published, because a")
    print("  product that only ever shows you its final number is asking you to trust that")
    print("  it looked.")
    print()
    print("  Disagree with a label? Every row above is a line in a CSV you can open, and")
    print("  every rule links to the dated record that argued for it. That is the point.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
