#!/usr/bin/env python3
"""
Fig 14/15（fig:perf-rect / fig:perf-wedge）核验

对象：五方法统一网格场图。
  Fig 14 = perf_grid_R1.pdf，R1 矩形，Cases 15-19
  Fig 15 = perf_grid_W1.pdf，W1 楔形，Cases 20-24

与前几组的关键差别：本组图上**不标任何数值**（无 Src、无 Avg），
面板标题只有方法名与 Pred./|Error|。因此数值锚点只能取：
  · 行标签 `f = XX Hz (a/b)` 的频率与样本序
  · 列结构 COMSOL(Ref) + 五方法 x (Pred., |Error|)
  · 逐方法场误差的**排序**须与兄弟表 Tables 13/14 的 Avg TL 排序同向
    （图误差是 8 个展示样本的场均值，表 TL 是全测试集平均，
      数值不同但排序必须一致——这是可核的关系）

数据源：Raw_Experimental_Data 下各 case 的 ep200 npz。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG14_15_perf_grid"
SCRIPT_AUTH = Path(r"D:\Data\regen_method_grid.py")
SCRIPT_REPO = Path(r"D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts"
                   r"\regen_method_grid.py")
METHODS = ["Proposed", "DeepONet", "FNO", "KNO", "CNO"]

# (图 label, 组名, 兄弟表 label, 图号, 域, 案例, PDF)
FIGS = [
    ("fig:perf-rect", "perf_grid_R1", "tab:perf-rect",
     "14", "Rectangle", (15, 16, 17, 18, 19), "perf_grid_R1.pdf"),
    ("fig:perf-wedge", "perf_grid_W1", "tab:perf-wedge",
     "15", "Wedge", (20, 21, 22, 23, 24), "perf_grid_W1.pdf"),
]
FREQS = (25, 50, 75, 100)


def md5(p):
    import hashlib
    try:
        return hashlib.md5(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def script():
    """import 权威绘图脚本，复用其取数与插值函数（口径防漂移）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("rmg", str(SCRIPT_AUTH))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pdftext(pdf_path):
    """PDF 文本层，必须 -raw（-layout 会把多行面板标题按列咬合）。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return out.stdout
    except Exception:
        return ""


def run():
    import numpy as np
    from common import metrics as M

    c = report.Checker(SLUG, "五方法统一网格场图 Fig 14/15", "figure",
                       "fig:perf-rect / fig:perf-wedge", "14/15")

    c.source("印刷面 tex", paths.TEX, "单个 figure* 内含两图")
    c.source("成图脚本（权威）", str(SCRIPT_AUTH), "regen_method_grid.py")
    c.source("成图脚本 repo 副本", str(SCRIPT_REPO), "md5 应与权威副本相同")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯与口径防漂移")
    ma, mc = md5(SCRIPT_AUTH), md5(SCRIPT_REPO)
    c.check(ma is not None and ma == mc, "成图脚本两份副本 md5 同源",
            f"权威 `{(ma or '-')[:8]}` / repo `{(mc or '-')[:8]}`")
    m = script()
    c.check(m.GRID == 200, "GRID == 200", f"脚本内 `{m.GRID}`")
    c.check(m.METHOD == "cubic", "插值 METHOD == cubic", f"脚本内 `{m.METHOD}`")
    c.check(m.N_SAMPLE == 2, "每频率展示 2 个样本", f"脚本内 `{m.N_SAMPLE}`")
    c.check(list(m.FREQS) == list(FREQS), "FREQS 一致", f"`{list(m.FREQS)}`")

    for label, g, _, _, _, cases, pdf in FIGS:
        cfg = m.GROUPS[g]
        c.check([lb for _, lb in cfg["methods"]] == METHODS,
                f"{label} 方法顺序与表行序一致", str([lb for _, lb in cfg["methods"]]))
        c.check(os.path.exists(os.path.join(paths.FIGDIR, pdf)),
                f"{label} 图件存在", pdf)

    # ── B ────────────────────────────────────────────────────────
    c.section("2. epoch 双侧判据与 caption 声明")
    c.note("图取 ep200(last)，兄弟表 Tables 13/14 取 best epoch，本是两套口径。"
           "故除『caption 含 last』外，还须断言『caption 未误写 best』，"
           "并列出各 case 的 best 与 200 的差异佐证。")
    for label, g, tab, num, dom, cases, pdf in FIGS:
        cfg = m.GROUPS[g]
        eps = sorted({int(np.load(m.find_npz(sub), allow_pickle=True)["epoch"])
                      for sub, _ in cfg["methods"]})
        c.check(eps == [200], f"{label} 全部 npz epoch == 200 (last)",
                f"实得 {eps}（{len(cfg['methods'])} 份 npz）")
        cap = T.caption_of(label) or ""
        c.check("last epoch" in cap, f"{label} caption 声明 last epoch",
                "含 `Fields are from the last epoch.`")
        c.check("best epoch" not in cap, f"{label} caption 未误写 best epoch",
                "图源自 ep200 npz")
        c.check(f"Cases~{cases[0]}--{cases[-1]}" in cap,
                f"{label} caption 标明案例区间 {cases[0]}-{cases[-1]}", "")
        for no in cases:
            be = M.xlsx_case(paths.xlsx_path("4.4"), no)["best_epoch"]
            c.check(be is not None, f"Case {no} best epoch 可读",
                    f"best={be}, last=200, "
                    + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 图内结构：行标签与列标题")
    c.note("本组图不标任何数值（无 Src、无 Avg），故锚点取图内文本："
           "8 个行标签 `f = XX Hz (a/b)` 须与 pick_rows 的取样序一致；"
           "列标题须含 COMSOL(Ref) 与五个方法名。")
    for label, g, tab, num, dom, cases, pdf in FIGS:
        cfg = m.GROUPS[g]
        base = np.load(m.find_npz(cfg["methods"][0][0]), allow_pickle=True)
        rows = m.pick_rows(base, cfg.get("nsample", m.N_SAMPLE))
        want = [f"f = {f} Hz ({chr(97 + k)})" for f, _, k in rows]

        txt = pdftext(os.path.join(paths.FIGDIR, pdf))
        got = re.findall(r"f = \d+ Hz \([ab]\)", txt)
        c.check(len(rows) == 8, f"{label} 行数 = 8（4 频率 x 2 样本）",
                f"实得 {len(rows)}")
        c.check(sorted(got) == sorted(want),
                f"{label} 8 个行标签与取样序一致",
                f"图上 {len(got)} 个，缺 {sorted(set(want) - set(got)) or '无'}")
        c.check([i for _, i, _ in rows] == list(range(8)),
                f"{label} 样本索引按 0-7 顺序取", str([i for _, i, _ in rows]))
        c.check("COMSOL" in txt, f"{label} 含 COMSOL 参考列", "")
        for name in METHODS:
            c.check(name in txt, f"{label} 含方法 {name} 的列标题", "")
        c.check("|Error|" in txt or "Error" in txt,
                f"{label} 含 |Error| 列", "")

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 图误差排序 vs 兄弟表 Avg TL 排序")
    c.note("图上 8 个展示样本的逐方法场误差均值，与表的全测试集 Avg TL "
           "数值不同（样本集不同），但**排序必须同向**——若图里某方法看着"
           "最准而表里它最差，就是图表不同源的信号。")
    for label, g, tab, num, dom, cases, pdf in FIGS:
        cfg = m.GROUPS[g]
        base = np.load(m.find_npz(cfg["methods"][0][0]), allow_pickle=True)
        gfem = {i: m.fem_grid(base, i) for i in range(8)}
        fig_err, tab_tl = [], []
        for (sub, lb), no in zip(cfg["methods"], cases):
            d = np.load(m.find_npz(sub), allow_pickle=True)
            e = float(np.mean([
                float(np.nanmean(np.abs(m.grid_of(d, i)[0] - gfem[i])))
                for i in range(8)]))
            fig_err.append((lb, e))
            tab_tl.append((lb, M.xlsx_case(paths.xlsx_path("4.4"),
                                           no)["Overall"]["tl"]))
        o_fig = [lb for lb, _ in sorted(fig_err, key=lambda t: t[1])]
        o_tab = [lb for lb, _ in sorted(tab_tl, key=lambda t: t[1])]
        c.check(o_fig == o_tab, f"{label} 图误差排序 == 表 TL 排序",
                f"图 {o_fig} / 表 {o_tab}")
        c.check(o_fig[0] == "Proposed", f"{label} 图上本文法误差最小",
                " < ".join(f"{lb}:{e:.3f}" for lb, e in sorted(
                    fig_err, key=lambda t: t[1])))

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 正文引用")
    txt_all = T.tex_text()
    aux = T.labels()
    for label, g, tab, num, dom, cases, pdf in FIGS:
        c.check(aux.get(label, {}).get("num") == num,
                f"{label} 编号为 {num}",
                f"aux `{aux.get(label, {}).get('num', '缺失')}`")
    n1 = txt_all.count("\\ref{fig:perf-rect}")
    c.check(n1 >= 1, "Fig 14 被引用（含 Fig 15 caption 的 Layout 交叉引用）",
            f"`\\ref{{fig:perf-rect}}` 出现 {n1} 处")
    hits = T.sentences_with(r"tab:perf-rect", txt_all)
    c.check(bool(hits), "兄弟表 Table 13 在正文被引",
            f"tex 行 {T.line_of(hits[0][0], txt_all)}" if hits else "未找到")

    return c

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
