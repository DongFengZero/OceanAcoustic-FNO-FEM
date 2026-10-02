#!/usr/bin/env python3
"""build_accuracy_xlsx.py — 从训练日志重建 4.2-4.7 的精度汇总 xlsx

补上取数链条里唯一的缺口
--------------------------
第四章的表分两种取数路径：

  · 表 3 / 5 / 9-12 —— 脚本直接读 .mat / .npz 现场算，本来就是源数据
  · 表 4 / 6-8 / 13-19 —— 读归档的"数据汇总 xlsx"

后者的 xlsx 是当初跑实验时随流程产出的，仓库里原先没有能重建它的脚本，
链条到 xlsx 就断了。本脚本把它接上：**只用训练日志**重建这些 xlsx。

  日志 (full_run_*.log)  →  本脚本  →  精度汇总 xlsx  →  table*.py / 论文表

解析用的是 ch4_validation/common/metrics.py 里的 log_best_epoch() 与
log_epoch()——与 verify.py 的"双渠道交叉"同一套函数，不另写一份。

    python build_accuracy_xlsx.py --check      # 只比对，不写文件（推荐先跑）
    python build_accuracy_xlsx.py --out DIR    # 重建到 DIR

--check 会把重建值与归档 xlsx 逐案例逐频率比对。二者不要求逐位相同：
xlsx 存的是当时写入的值，日志侧是现场重算，相对容差取 2e-6（与 verify.py
的双渠道判定一致），即在表格给出的有效数字范围内一致即可。
"""
import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.join(os.path.dirname(_HERE), "ch4_validation")
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

from common import metrics as M          # noqa: E402
from common import paths                 # noqa: E402

# 节 → (xlsx 文件名, 案例区间)
SECTIONS = [
    ("4.2", "Case1-2_数据汇总.xlsx", range(1, 3)),
    ("4.3", "Case3-14_数据汇总.xlsx", range(3, 15)),
    ("4.4", "Case15-24_数据汇总.xlsx", range(15, 25)),
    ("4.5", "Case25-32_数据汇总.xlsx", range(25, 33)),
    ("4.6", "Case33-38_数据汇总.xlsx", range(33, 39)),
    ("4.7", "Case39-42_数据汇总.xlsx", range(39, 43)),
]

RTOL = 2e-6      # 与 verify.py 双渠道交叉同一容差
ATOL = 1e-9

GROUPS = ("Overall", 25, 50, 75, 100)
QUANTS = ("sol", "tl")


def from_log(no):
    """一个案例：从日志取 best epoch 及该轮的 Sol/TL。"""
    lp = paths.log_path(no)
    if not lp or not os.path.exists(lp):
        return None
    be = M.log_best_epoch(lp)
    if be is None:
        return None
    d = M.log_epoch(lp, be)
    if d is None:
        return None
    d["best_epoch"] = be
    return d


def close(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= max(ATOL, abs(b) * RTOL)


def check():
    """重建值 vs 归档 xlsx，逐案例逐频率比对。"""
    tot = ok = bad = skip = 0
    for sec, fname, cases in SECTIONS:
        xl = paths.xlsx_path(sec)
        print(f"\n=== {sec}  {fname} ===")
        if not os.path.exists(xl):
            print("  归档 xlsx 不在本机，跳过")
            continue
        for no in cases:
            lg = from_log(no)
            if lg is None:
                print(f"  Case {no:<3} 日志缺失或无法解析 → 跳过")
                skip += 1
                continue
            try:
                xd = M.xlsx_case(xl, no)
            except Exception as e:
                print(f"  Case {no:<3} xlsx 无此行：{e}")
                skip += 1
                continue

            bes = "" if xd.get("best_epoch") == lg["best_epoch"] else \
                  f"  ⚠ best epoch xlsx={xd.get('best_epoch')} log={lg['best_epoch']}"
            diffs = []
            for g in GROUPS:
                for q in QUANTS:
                    a = (lg.get(g) or {}).get(q)
                    b = (xd.get(g) or {}).get(q)
                    tot += 1
                    if close(a, b):
                        ok += 1
                    else:
                        bad += 1
                        diffs.append(f"{g}/{q}: log={a} xlsx={b}")
            flag = "OK" if not diffs else "DIFF"
            print(f"  Case {no:<3} best={lg['best_epoch']:<4} {flag}{bes}")
            for d in diffs[:4]:
                print(f"        {d}")
    print(f"\n合计 {tot} 项：{ok} 一致 / {bad} 不一致 / {skip} 案例跳过")
    print(f"判定容差：相对 {RTOL:g}（绝对下限 {ATOL:g}），与 verify.py 双渠道一致")
    # 纯 ASCII 摘要行：给 run_all.py 解析用（中文经管道可能变成乱码）
    print(f"SUMMARY total={tot} ok={ok} bad={bad} skipped={skip}")
    return bad == 0


def build(outdir):
    """把重建值写成 xlsx。列结构与归档件一致：
    No. / Dataset / Best Epoch / 每组(Overall+四频) × (损失, MSE=Sol, TL)。
    """
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font

    os.makedirs(outdir, exist_ok=True)
    made = []
    for sec, fname, cases in SECTIONS:
        rows = []
        for no in cases:
            lg = from_log(no)
            if lg is not None:
                rows.append((no, lg))
        if not rows:
            print(f"{sec}: 无可用日志，跳过")
            continue

        wb = Workbook()
        ws = wb.active
        ws.title = f"{sec} rebuilt"
        ws["A1"] = f"{fname[:-5]} · 由训练日志重建（build_accuracy_xlsx.py）"
        ws["A1"].font = Font(bold=True, size=12)
        ws["A2"] = ("取数：common/metrics.py 的 log_best_epoch() + log_epoch()，"
                    "即 verify.py 双渠道交叉所用的同一套解析。"
                    "Sol = (总损失 − w_prior×prior)/w_rel × 1e6，权重逐轮现场解析。")
        ws["A2"].font = Font(italic=True, size=9, color="595959")

        hdr = ["No.", "Best Epoch"]
        for g in GROUPS:
            tag = "Overall" if g == "Overall" else f"{g}Hz"
            hdr += [f"{tag} 损失", f"{tag} MSE(Sol,1e-6)", f"{tag} TL(dB)"]
        for j, h in enumerate(hdr, 1):
            c = ws.cell(4, j, h)
            c.font = Font(bold=True)
            c.alignment = Alignment(horizontal="center", wrap_text=True)

        r = 5
        for no, lg in rows:
            vals = [no, lg["best_epoch"]]
            for g in GROUPS:
                b = lg.get(g) or {}
                vals += [b.get("loss"), b.get("sol"), b.get("tl")]
            for j, v in enumerate(vals, 1):
                ws.cell(r, j, v if v is not None else "—")
            r += 1

        out = os.path.join(outdir, fname.replace(".xlsx", "_rebuilt.xlsx"))
        wb.save(out)
        made.append(out)
        print(f"{sec}: 写出 {len(rows)} 行 -> {out}")
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="只比对重建值与归档 xlsx，不写文件")
    ap.add_argument("--out", metavar="DIR",
                    help="重建 xlsx 的输出目录")
    a = ap.parse_args()
    if not a.check and not a.out:
        ap.print_help()
        print("\n提示：先跑 --check 看重建值是否与归档一致。")
        return 0
    rc = 0
    if a.check:
        rc = 0 if check() else 1
    if a.out:
        build(a.out)
    return rc


if __name__ == "__main__":
    sys.exit(main())
