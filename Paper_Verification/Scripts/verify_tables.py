# -*- coding: utf-8 -*-
"""
verify_tables.py
================
Recompute every Chapter-4 accuracy-table cell from the archived summary
spreadsheets and diff against the printed values in paper_values.py. Also verify
the runtime tables (T20/T21) from the performance spreadsheet, and the depth-line
tables (T5, T9-T12) by re-running the selection pipeline from the raw npz.

Each check yields a Finding(kind, id, expected, actual, ok, source). The master
runner aggregates and reports them.
"""
import math
import paper_values as PV
import data_sources as DS
import depthline_recompute as DL


class Finding:
    __slots__ = ("kind", "ident", "expected", "actual", "ok", "source", "note")

    def __init__(self, kind, ident, expected, actual, ok, source, note=""):
        self.kind = kind
        self.ident = ident
        self.expected = expected
        self.actual = actual
        self.ok = ok
        self.source = source
        self.note = note

    def as_dict(self):
        return dict(kind=self.kind, id=self.ident, expected=self.expected,
                    actual=self.actual, ok=self.ok, source=self.source, note=self.note)


def _close(a, b, atol, rtol):
    if a is None or b is None:
        return False
    return abs(a - b) <= max(atol, rtol * abs(b))


# Tolerances: printed values are rounded, so allow half-ULP of the printed
# precision plus a small relative margin.
SOL_ATOL, SOL_RTOL = 0.05, 0.012      # Sol printed to 2-3 sig figs (x1e-6)
TL_ATOL = 0.02                        # TL printed to 2 decimals (dB)
DL_ATOL = 0.02                        # depth-line MAE printed to 3 decimals
TIME_RTOL = 0.01                      # runtime ms/thr


def _check_perfreq(table_id, table, group, findings):
    summ, src = DS.load_summary(group)
    for no, freqs in table.items():
        if no not in summ:
            findings.append(Finding("table", f"{table_id}:No{no}", "present",
                                    "missing", False, src, "No. absent in xlsx"))
            continue
        for f, (sol_p, tl_p) in freqs.items():
            got = summ[no].get(f)
            if got is None:
                findings.append(Finding("table", f"{table_id}:No{no}:{f}Hz", (sol_p, tl_p),
                                        None, False, src, "freq block missing"))
                continue
            ok_sol = _close(got["sol"], sol_p, SOL_ATOL, SOL_RTOL)
            ok_tl = _close(got["tl"], tl_p, TL_ATOL, 0.0)
            findings.append(Finding(
                "table", f"{table_id}:No{no}:{f}Hz",
                dict(Sol=sol_p, TL=tl_p),
                dict(Sol=round(got["sol"], 3), TL=round(got["tl"], 3)),
                ok_sol and ok_tl, src))


def _check_singlefreq(table_id, table, group, findings):
    summ, src = DS.load_summary(group)
    for no, (sol_p, tl_p) in table.items():
        got = summ.get(no, {}).get(100)
        if got is None:
            findings.append(Finding("table", f"{table_id}:No{no}", (sol_p, tl_p),
                                    None, False, src, "100Hz block missing"))
            continue
        ok_sol = _close(got["sol"], sol_p, SOL_ATOL, SOL_RTOL)
        ok_tl = _close(got["tl"], tl_p, TL_ATOL, 0.0)
        findings.append(Finding(
            "table", f"{table_id}:No{no}",
            dict(Sol=sol_p, TL=tl_p),
            dict(Sol=round(got["sol"], 3), TL=round(got["tl"], 3)),
            ok_sol and ok_tl, src))


def verify_accuracy_tables():
    findings = []
    _check_perfreq("T4", PV.T4, "validation", findings)
    _check_perfreq("T6", PV.T6, "forward", findings)
    _check_singlefreq("T7T8", PV.T78, "forward", findings)
    _check_perfreq("T13T14", PV.T1314, "comparison", findings)
    _check_perfreq("T15T16", PV.T1516, "ablation", findings)
    _check_singlefreq("T17T18", PV.T1718, "mesh", findings)
    _check_perfreq("T19", PV.T19, "generalization", findings)
    return findings


def verify_depthline_tables():
    findings = []
    # T5 ideal
    for no in (1, 2):
        section, case_dir = PV.CASE_MAP[no]
        z, rel = DS.load_npz(section, case_dir)
        if z is None:
            findings.append(Finding("table", f"T5:No{no}", "npz", "missing", False, "-"))
            continue
        got, yline = DL.ideal_depthline(z, y_line=44.7)
        for f, (mae_p, src_p) in PV.T5[no].items():
            g = got.get(f)
            ok = g is not None and _close(g[0], mae_p, 0.05, 0.10)
            findings.append(Finding(
                "table", f"T5:No{no}:{f}Hz", dict(MAE=mae_p),
                dict(MAE=None if g is None else g[0], src=None if g is None else g[1]),
                ok, rel, f"y={yline:.1f}"))
    # T9-T12 comparison/ablation depth-line
    tid = {"comparison_R1_model_advantage": "T9",
           "comparison_W1_model_advantage": "T10",
           "ablation_R1_module_advantage": "T11",
           "ablation_W1_module_advantage": "T12"}
    for group, tag in tid.items():
        try:
            got, yline, srcs = DL.recompute_group(DS.load_npz, group)
        except Exception as e:  # pragma: no cover
            findings.append(Finding("table", f"{tag}:{group}", "recompute", str(e),
                                    False, "-"))
            continue
        exp = PV.DEPTHLINE[group]
        for f in (25, 50, 75, 100):
            for label, mae_p in exp[f].items():
                g = got.get(f, {}).get(label)
                ok = _close(g, mae_p, DL_ATOL, 0.0)
                findings.append(Finding(
                    "table", f"{tag}:{f}Hz:{label}", mae_p, g, ok,
                    "; ".join(srcs), f"y={yline:.1f}"))
    return findings


def verify_runtime_tables():
    findings = []
    runtime, scale, src = DS.load_perf()
    method_alias = {"COMSOL (CPU)": "COMSOL", "1×A800 GPU": "1 GPU",
                    "2×A800 GPU": "2 GPU", "4×A800 GPU": "4 GPU"}
    rt = {}
    for row in runtime:
        m = method_alias.get(row["method"], row["method"])
        rt[(row["case"], m)] = row
    for (case, method), (t_p, thr_p, sp_p) in PV.T20.items():
        row = rt.get((case, method))
        if row is None:
            findings.append(Finding("table", f"T20:{case}:{method}", (t_p, thr_p, sp_p),
                                    None, False, src, "row missing"))
            continue
        ok = (_close(row["time_ms"], t_p, 0.05, TIME_RTOL) and
              _close(row["thr"], thr_p, 0.05, TIME_RTOL) and
              _close(row["speedup"] or sp_p, sp_p, 0.2, 0.02))
        findings.append(Finding(
            "table", f"T20:{case}:{method}",
            dict(time=t_p, thr=thr_p, speedup=sp_p),
            dict(time=row["time_ms"], thr=row["thr"], speedup=row["speedup"]),
            ok, src))
    sc = {row["case"]: row for row in scale}
    for case, (lx_p, n_p, t_p) in PV.T21.items():
        row = sc.get(case)
        if row is None:
            findings.append(Finding("table", f"T21:{case}", (lx_p, n_p, t_p),
                                    None, False, src, "row missing"))
            continue
        ok = (_close(row["N"], n_p, 0.5, 0.0) and
              _close(row["time_ms"], t_p, 0.05, TIME_RTOL) and
              _close(row["Lx"], lx_p, 0.5, 0.0))
        findings.append(Finding(
            "table", f"T21:{case}", dict(Lx=lx_p, N=n_p, time=t_p),
            dict(Lx=row["Lx"], N=row["N"], time=row["time_ms"]), ok, src))
    return findings


if __name__ == "__main__":
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    allf = (verify_accuracy_tables() + verify_depthline_tables()
            + verify_runtime_tables())
    bad = [f for f in allf if not f.ok]
    print(f"tables: {len(allf)} checks, {len(allf)-len(bad)} pass, {len(bad)} fail")
    for f in bad[:40]:
        print("  FAIL", f.ident, "exp", f.expected, "got", f.actual, f.note)
