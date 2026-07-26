#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run_all.py
==========
Master verification runner: recompute all Chapter-4 tables and figures from the
archived raw data, diff against the printed paper values, and emit a structured
report (JSON + markdown). Run with:

    RAW_ROOT=/path/to/Raw_Experimental_Data python run_all.py

or set RAW_ROOT in your environment. See README.md for details.
"""
import os
import sys
import io
import json
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import verify_tables
import verify_figures

def main():
    print("="*70)
    print("Chapter 4 Verification Suite")
    print("Recomputing all tables and figures from raw data...")
    print("="*70)
    t0 = time.time()

    print("\n[1/2] Verifying tables (accuracy + depth-line + runtime)...")
    tf = (verify_tables.verify_accuracy_tables() +
          verify_tables.verify_depthline_tables() +
          verify_tables.verify_runtime_tables())

    print("[2/2] Verifying figures (field + depth-line + split + runtime)...")
    ff = verify_figures.verify_figures()

    allf = tf + ff
    elapsed = time.time() - t0

    # Aggregate
    by_kind = {}
    for f in allf:
        by_kind.setdefault(f.kind, []).append(f)

    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    total, passed, failed = len(allf), sum(1 for f in allf if f.ok), sum(1 for f in allf if not f.ok)
    print(f"Total:  {total} checks")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Time:   {elapsed:.1f}s")

    for kind in sorted(by_kind):
        checks = by_kind[kind]
        p = sum(1 for c in checks if c.ok)
        print(f"  {kind}: {p}/{len(checks)} pass")

    # Show failures
    bad = [f for f in allf if not f.ok]
    if bad:
        print("\n" + "="*70)
        print("FAILURES")
        print("="*70)
        for f in bad[:50]:
            print(f"  {f.ident}")
            print(f"    expected: {f.expected}")
            print(f"    actual:   {f.actual}")
            print(f"    source:   {f.source}")
            if f.note:
                print(f"    note:     {f.note}")

    # JSON report
    report = dict(
        total=total, passed=passed, failed=failed, elapsed=elapsed,
        checks=[f.as_dict() for f in allf],
        by_kind={k: dict(total=len(v), passed=sum(1 for c in v if c.ok))
                 for k, v in by_kind.items()},
    )
    with open("verification_results.json", "w", encoding="utf-8") as fp:
        json.dump(report, fp, indent=2, ensure_ascii=False)
    print(f"\nJSON report written to verification_results.json")

    # Markdown report
    md = []
    md.append("# Chapter 4 Verification Report\n")
    md.append(f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append(f"**Total checks**: {total}  ")
    md.append(f"**Passed**: {passed}  ")
    md.append(f"**Failed**: {failed}  ")
    md.append(f"**Elapsed**: {elapsed:.1f}s\n")
    md.append("## Summary by Kind\n")
    for kind in sorted(by_kind):
        checks = by_kind[kind]
        p = sum(1 for c in checks if c.ok)
        md.append(f"- **{kind}**: {p}/{len(checks)} pass\n")
    if bad:
        md.append("\n## Failures\n")
        for f in bad[:50]:
            md.append(f"### {f.ident}\n")
            md.append(f"- **Expected**: `{f.expected}`\n")
            md.append(f"- **Actual**: `{f.actual}`\n")
            md.append(f"- **Source**: `{f.source}`\n")
            if f.note:
                md.append(f"- **Note**: {f.note}\n")
    else:
        md.append("\n✓ All checks passed.\n")

    with open("VERIFICATION_REPORT.md", "w", encoding="utf-8") as fp:
        fp.write("".join(md))
    print(f"Markdown report written to VERIFICATION_REPORT.md")

    print("\n" + "="*70)
    if failed == 0:
        print("✓ ALL CHECKS PASSED")
        print("="*70)
        return 0
    else:
        print(f"✗ {failed} CHECK(S) FAILED")
        print("="*70)
        return 1

if __name__ == "__main__":
    sys.exit(main())
