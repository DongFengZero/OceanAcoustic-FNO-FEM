#!/usr/bin/env python3
"""
Fig 23（fig:perf）核验

对象：推理性能图，三个子图
  (a) 多 GPU 吞吐（R1/W1，1/2/4 卡 A800）
  (b) 相对 COMSOL 的吞吐加速比
  (c) 单 DCU 每样本推理时间 vs 网格节点数（域 128->512 m）

本组特点
  · 与 Fig 20 同样无 epoch 概念（推理耗时与训练轮次无关），
    caption 不含 epoch 声明是正确的。
  · 数据源是 Tables 20/21 的同一批运行时统计，不是 npz 场数据。
  · ★ 已知缺口：仓库内没有生成 perf_merged.pdf 的脚本
    （build_perf.py 只产 xlsx，不画图），故无法做"脚本产物 vs 论文图件"
    的 md5 同源比对。改以"图上标注 vs 表值"逐点核验替代，并把该缺口
    显式记录为 exempt。

数据源：4.8_Performance 的 xlsx 两个 sheet。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG23_perf"
LABEL = "fig:perf"
PDF_NAME = "perf_merged.pdf"

# 图(a) 吞吐标注（取整）与图(b) 加速标注（取整），按 R1 1/2/4 卡 + W1 1/2/4 卡
FIG_THR = ["53", "98", "164", "62", "120", "212"]
FIG_SPD = ["46", "85", "142", "31", "60", "106"]
# 子图 (c) 标注的域边长
FIG_SCALE_LBL = ["128 m", "256 m", "512 m"]


def pdftext(p):
    """PDF 文本层。用 bytes 再解码：图内含 × 符号，GBK 环境直接 text=True 会崩。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(p), "-"],
                             capture_output=True, timeout=180)
        return out.stdout.decode("utf-8", "replace")
    except Exception:
        return ""


def run():
    import pandas as pd

    c = report.Checker(SLUG, "推理性能图 Fig 23", "figure", LABEL, "23")
    c.source("印刷面 tex", paths.TEX, "单个 figure* 环境")
    c.source("运行时 xlsx", paths.xlsx_path("4.8"), "两个 sheet，Tables 20/21 同源")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 图件与已知缺口")
    pdf = os.path.join(paths.FIGDIR, PDF_NAME)
    c.check(os.path.exists(pdf), "图件存在", PDF_NAME)
    c.note("成图脚本原先不在仓库内（build_perf.py 只产 xlsx 不画图），现已"
           "收入 Validation_Scripts/build_perf_figure.py。该脚本把数值**硬编码**"
           "在源码里而非从 xlsx 读取，所以真正的风险不是『图与脚本不一致』，"
           "而是『脚本里的常量与表值脱钩』——下一节直接解析源码常量与 xlsx "
           "比对，正是针对这一点。")

    src = os.path.join(paths.PLOTDIR, "build_perf_figure.py")
    c.check(os.path.exists(src), "成图脚本已入库",
            "Validation_Scripts/build_perf_figure.py")

    txt = pdftext(pdf)
    c.check(len(txt) > 50, "PDF 文本层可读", f"{len(txt)} 字符")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 子图(a)(b) 标注 vs Table 20")
    c.note("图上标注取整，表值保留小数。逐点核『图标注 == round(表值)』。")
    df1 = pd.read_excel(paths.xlsx_path("4.8"), sheet_name=0, header=2)
    rows = [r for _, r in df1.iloc[1:].iterrows()
            if "GPU" in str(r.iloc[4])]
    c.check(len(rows) == 6, "Table 20 含 6 行 GPU 数据（R1/W1 各 1/2/4 卡）",
            f"实得 {len(rows)}")

    for k, r in enumerate(rows):
        thr_tab = float(r.iloc[6])
        spd_tab = float(r.iloc[8])
        c.check(FIG_THR[k] == f"{round(thr_tab):.0f}",
                f"图(a) 第{k+1}点吞吐 {FIG_THR[k]} == round({thr_tab})",
                f"表 `{thr_tab}` → `{round(thr_tab)}`")
        c.check(FIG_SPD[k] == f"{round(spd_tab):.0f}",
                f"图(b) 第{k+1}点加速 {FIG_SPD[k]}x == round({spd_tab})",
                f"表 `{spd_tab}` → `{round(spd_tab)}`")
        c.check(FIG_THR[k] in txt, f"图(a) 标注 `{FIG_THR[k]}` 见于 PDF", "")
        c.check(FIG_SPD[k] in txt, f"图(b) 标注 `{FIG_SPD[k]}` 见于 PDF", "")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 子图(c) 标注 vs Table 21")
    c.note("子图(c) 只在数据点旁标域边长，不标数值；核标注齐全且与 Table 21 "
           "的 Lx 列一致（三种尺度各出现于矩形与楔形两条曲线）。")
    df2 = pd.read_excel(paths.xlsx_path("4.8"), sheet_name=1, header=2)
    lx_tab = sorted({int(r.iloc[3]) for _, r in df2.iloc[1:].iterrows()})
    c.check(lx_tab == [128, 256, 512], "Table 21 的 Lx 取值 = 128/256/512",
            str(lx_tab))
    for lbl in FIG_SCALE_LBL:
        c.check(txt.count(lbl) >= 2,
                f"子图(c) 标注域边长 {lbl}（矩形+楔形两条曲线各一次）",
                f"PDF 内出现 {txt.count(lbl)} 次")

    # ── C2 ───────────────────────────────────────────────────────
    c.section("3b. 成图脚本硬编码常量 vs xlsx 表值")
    c.note("脚本里 thr/spd/nodes/time 四组常量是手抄进去的，一旦表值更新而"
           "常量未同步，图就会静默过期。此处用 ast 解析源码取出常量，与 "
           "xlsx 逐值比对——这是比『图上标注 vs 表值』更靠前的一道闸。")
    import ast as _ast
    tree = _ast.parse(open(src, encoding="utf-8").read())
    consts = {}
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Assign) and len(node.targets) == 1:
            tgt = node.targets[0]
            if isinstance(tgt, _ast.Name):
                try:
                    consts[tgt.id] = _ast.literal_eval(node.value)
                except Exception:
                    pass

    # Table 20：吞吐与加速比（跳过 COMSOL 行）
    gpu_rows = [r for _, r in df1.iloc[1:].iterrows()
                if "GPU" in str(r.iloc[4])]
    want_thr = {"R1": [], "W1": []}
    want_spd = {"R1": [], "W1": []}
    for r in gpu_rows:
        key = "R1" if int(r.iloc[0]) == 43 else "W1"
        want_thr[key].append(round(float(r.iloc[6]), 2))
        want_spd[key].append(round(float(r.iloc[8]), 1))
    for key in ("R1", "W1"):
        got = [round(float(v), 2) for v in consts.get("thr", {}).get(key, [])]
        c.check(got == want_thr[key], f"脚本 thr[{key}] 与 Table 20 一致",
                f"脚本 {got} / xlsx {want_thr[key]}")
        got = [round(float(v), 1) for v in consts.get("spd", {}).get(key, [])]
        c.check(got == want_spd[key], f"脚本 spd[{key}] 与 Table 20 一致",
                f"脚本 {got} / xlsx {want_spd[key]}")

    # Table 21：节点数与推理时间
    for pre, geo in (("R", "Rect."), ("W", "Wedge")):
        rows = [r for _, r in df2.iloc[1:].iterrows()
                if str(r.iloc[1]).startswith(pre)]
        wn = [int(r.iloc[5]) for r in rows]
        wt = [round(float(r.iloc[6]), 2) for r in rows]
        gn = [int(v) for v in consts.get(f"nodes_{pre}", [])]
        gt = [round(float(v), 2) for v in consts.get(f"time_{pre}", [])]
        c.check(gn == wn, f"脚本 nodes_{pre} 与 Table 21 一致",
                f"脚本 {gn} / xlsx {wn}")
        c.check(gt == wt, f"脚本 time_{pre} 与 Table 21 一致",
                f"脚本 {gt} / xlsx {wt}")
    c.check([int(v) for v in consts.get("edge", [])] == [128, 256, 512],
            "脚本 edge 标注 = 128/256/512",
            str(consts.get("edge")))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. caption 与正文引用")
    cap = T.caption_of(LABEL) or ""
    c.check("epoch" not in cap.lower(),
            "caption 不含 epoch 声明（推理耗时与训练轮次无关，正确）", "")
    for tag in ("(a)", "(b)", "(c)"):
        c.check(tag in cap, f"caption 说明子图 {tag}", "")
    c.check("A800" in cap, "caption 标明 GPU 型号 A800", "")
    c.check("DCU" in cap, "caption 标明子图(c) 用单 DCU", "")
    c.check("45" in cap and "50" in cap,
            "caption 标明子图(c) 案例区间 45-50", "含 `Cases~45--50`")
    c.check("COMSOL" in cap, "caption 说明子图(b) 的基准是 COMSOL", "")

    txt_all = T.tex_text()
    aux = T.labels()
    c.check(aux.get(LABEL, {}).get("num") == "23", "编号为 23",
            f"aux `{aux.get(LABEL, {}).get('num', '缺失')}`")
    # 正文两处分别引用 (a,b) 与 (c)
    c.check("\\ref{fig:perf}(a,b)" in txt_all,
            "正文以 `Fig.~\\ref{fig:perf}(a,b)` 引用多 GPU 部分", "")
    c.check("\\ref{fig:perf}(c)" in txt_all,
            "正文以 `Fig.~\\ref{fig:perf}(c)` 引用域缩放部分", "")
    for tab in ("tab:runtime", "tab:runtime-scale"):
        hits = T.sentences_with(re.escape(tab), txt_all)
        c.check(bool(hits), f"兄弟表 `{tab}` 在正文被引",
                f"tex 行 {T.line_of(hits[0][0], txt_all)}" if hits else "未找到")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
