#!/usr/bin/env python3
"""
PROSE_cost.py — 4.8 节离线成本与盈亏点段（R2 新增，跨对象核验）

R2 在 Sec. 4.8 末尾新增一段，回应审稿人 #4 意见 4.5（"只比推理时间不公平，
应给出训练与数据生成成本"）。段中的十余个数值不在任何表里，源头是归档日志：

  数据生成   Dataset/R1/<cfg>/run_*.log 的全局统计块
             8000 个解、均值 873.1 ms、中位数 871.4 ms、P95 973.2 ms、求解总计 6984.4 s
  训练       Raw_Experimental_Data/4.4_Comparison/No15_R1_Proposed/…/statistics_epoch200.json
             timing_summary.train.total_s = 22351.8 s；日志"使用GPU数量: 8"
  推理       4.8_Performance/No43_R1/…/gpu1_full_run_*.log 测试集平均每样本 17.08 ms
             （与 Table 13(a) 的 1 GPU 行同源，T13 已核）

核验链
  1. 源日志存在、能解析
  2. 正文字面量 ↔ 源值（按印刷位数舍入后逐字符相等）
       1.94 h = 6984.4/3600 · 873.1 / 871.4 / 973.2 · 6.21 h = 22351.8/3600
       49.7 accelerator-hours = 6.21 h × 8 · 22352 s · 6984 s · 17.08 ms
  3. 推导量用**印刷值**现场重算（读者拿正文里的数就能验）
       0.856 s = (873.1 − 17.08)/1000 · 29336 = 22352 + 6984
       N* = 29336/0.856 = 3.43e4 → 3.4×10^4 · N*/8000 ≈ 4.3 → "about four times"
  4. 口径句：训练 8 卡、推理单卡；Case 15 与 Case 43 的归属

PROSE_numbers.py 对 sec:runtime 的小数同样从 common/costlog.py 取值，
故本段的数在"每个小数的出处"审计里归入"日志"一类，而不再是"无出处"。
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import costlog, paths, report, texparse as T  # noqa: E402

SLUG = "PROSE_cost"
B = chr(92)


def window(txt):
    """Sec. 4.8 成本段：从起句到 \\section{Conclusion}。"""
    i = txt.find("A comparison of this kind is complete only when the cost")
    j = txt.find(B + "section{Conclusion}", i)
    return txt[i:j] if i >= 0 and j > i else ""


def run():
    c = report.Checker(SLUG, "4.8 节离线成本与盈亏点（日志 ↔ 正文）", "table",
                       "prose (Sec. 4.8 cost paragraph)", "—")
    gen = costlog.comsol_stats("R1")
    tr = costlog.train_stats(15)
    inf_ms, inf_log = costlog.single_gpu_infer_ms(43)
    c.source("印刷面 tex", paths.TEX, "Sec. 4.8 末段")
    c.source("COMSOL 生成日志", gen["path"] if gen else None, "R1 数据集，全局统计块")
    c.source("训练统计 JSON", tr["json"], "Case 15，timing_summary.train.total_s")
    c.source("训练日志", tr["log"], "Case 15，使用GPU数量")
    c.source("单卡推理日志", inf_log, "Case 43，测试集平均每样本时间")

    txt = T.tex_text()
    win = window(txt)

    # ── 1 ────────────────────────────────────────────────────────
    c.section("1. 源日志可解析")
    c.check(bool(win), "4.8 节成本段可定位", "起句 `A comparison of this kind is complete…`")
    c.check(gen is not None and None not in (gen["n"], gen["mean_ms"], gen["median_ms"],
                                             gen["p95_ms"], gen["total_s"]),
            "COMSOL 生成日志含全局统计块", str({k: v for k, v in (gen or {}).items() if k != "path"}))
    c.check(tr["total_s"] is not None and tr["epoch"] == 200,
            "Case 15 statistics_epoch200.json 含训练墙钟", f"total_s={tr['total_s']} epoch={tr['epoch']}")
    c.check(tr["n_gpu"] is not None, "Case 15 日志含卡数", f"n_gpu={tr['n_gpu']}")
    c.check(inf_ms is not None, "Case 43 单卡日志含测试集每样本时间", f"{inf_ms} ms")
    if not (gen and tr["total_s"] and inf_ms):
        return c

    # ── 2 ────────────────────────────────────────────────────────
    c.section("2. 正文字面量 ↔ 源值（按印刷位数舍入）")
    n = int(gen["n"])
    lits = [
        (f"${n}$ reference solutions", f"{n} 个参考解 = 日志总样本数", True),
        (f"${gen['total_s'] / 3600:.2f}$" + B + ",h", "数据生成 1.94 h = 求解总计/3600", True),
        (f"${gen['mean_ms']:.1f}$" + B + ",ms per solve", "均值 873.1 ms", True),
        (f"median of ${gen['median_ms']:.1f}$" + B + ",ms", "中位数 871.4 ms", True),
        (f"95th percentile of ${gen['p95_ms']:.1f}$" + B + ",ms", "P95 973.2 ms", True),
        (f"${tr['total_s'] / 3600:.2f}$" + B + ",h on eight accelerators", "训练 6.21 h = total_s/3600", True),
        (f"${tr['total_s'] / 3600 * tr['n_gpu']:.1f}$ GPU-hours", "49.7 卡时 = 6.21 h × 8", False),
        (f"${tr['total_s']:.0f}$" + B + ",s of training", "训练 22352 s（取整）", True),
        (f"${gen['total_s']:.0f}$" + B + ",s of data generation", "数据生成 6984 s（取整）", True),
        (f"${inf_ms:.2f}$" + B + ",ms in Case~43", "推理 17.08 ms（Case 43 单卡）", True),
        (f"${gen['mean_ms']:.1f}$" + B + ",ms for COMSOL", "COMSOL 873.1 ms（同一均值）", True),
    ]
    for lit, desc, hard in lits:
        ok = lit in win
        if not ok and not hard:
            # R2 投稿版写 "GPU-hours"，校样改为 "accelerator-hours"（训练用的是 DCU）
            alt = lit.replace("GPU-hours", "accelerator-hours")
            ok = alt in win
            lit = f"{lit} | {alt}"
        c.check(ok, desc, f"`{lit}`")
    c.check(tr["n_gpu"] == 8 and "eight accelerators" in win, "卡数 8 ↔ 正文 eight accelerators",
            f"日志 {tr['n_gpu']}")

    # ── 3 ────────────────────────────────────────────────────────
    c.section("3. 推导量（用正文印刷值现场重算）")
    mean_p, inf_p = round(gen["mean_ms"], 1), round(inf_ms, 2)
    train_p, gen_p = round(tr["total_s"]), round(gen["total_s"])
    save = (mean_p - inf_p) / 1000
    c.check(f"${save:.3f}$" + B + ",s" in win, "每次查询节省 0.856 s = (873.1 − 17.08)/1000",
            f"`{save:.4f}`")
    offline = train_p + gen_p
    c.check(f"${offline}$" + B + ",s" in win, f"离线总计 {offline} s = {train_p} + {gen_p}", "")
    nstar = offline / round(save, 3)
    mant, exp = nstar / 10 ** 4, 4
    lit = f"N^{{*}}" + B + f"approx{mant:.1f}" + B + f"times10^{{{exp}}}"
    c.check(lit in win, f"盈亏点 N* = {offline}/{save:.3f} = {nstar:.0f} → {mant:.1f}×10^4", f"`{lit}`")
    ratio = nstar / n
    words = {3: "three", 4: "four", 5: "five"}
    c.check(f"about {words.get(round(ratio), '?')} times the size of the dataset" in win,
            f"N*/8000 = {ratio:.2f} → \"about {words.get(round(ratio), '?')} times\"", "")

    # ── 4 ────────────────────────────────────────────────────────
    c.section("4. 口径句")
    c.check("one training run on eight accelerators and inference on a single accelerator" in win,
            "口径：训练 8 卡墙钟 + 单卡推理", "")
    c.check("(Case~15)" in win and "Case~43" in win, "训练归 Case 15、推理归 Case 43", "")
    return c


if __name__ == "__main__":
    sys.exit(run().finish())
