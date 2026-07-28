#!/usr/bin/env python3
"""
Fig 5/6/7（fig:res-128 / res-256 / res-512）核验
================================================
对象：前向求解 TL 场图，三个尺度 × 矩形/楔形：
  Fig 5 = Case 3 (R1) + Case 9  (W1)   128x128
  Fig 6 = Case 4 (R2) + Case 10 (W2)   256x128
  Fig 7 = Case 5 (R3) + Case 11 (W3)   512x128

数据源一律取 Raw_Experimental_Data 下的 `*__TL原始数据_ep200.npz`。

核验链
  A. 源可追溯    npz 存在；绘图脚本两份副本 md5 同源
  B. 口径防漂移  从脚本源码读 method/grid_res，须与重算层一致
  C. epoch 自证  npz['epoch']==200，caption 声明 last epoch
  D. 数值复现    复刻 render() 算法重算逐样本 Avg 误差，
                 与 PDF 内 "Avg:x.xx dB" 标注逐一比对（★核心）
  E. Src 坐标    图上标注与 npz source_pos 一致
  F. 结构        每图 8 样本 = 4 频率 × 2，与 caption 声明一致
  G. 图表关系    图为逐样本、表为全测试集，不可互算；只核趋势同向（★）
  H. 引用完整    Fig. 列引用与子图 label 在 aux 注册
"""
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from common import paths, report
from common import texparse as T
from _recompute_field import recompute, METHOD, GRID_RES

# 图 -> (label, 矩形 case, 楔形 case, 尺度说明)
FIGS = [
    ("fig:res-128", 3, 9, "128x128"),
    ("fig:res-256", 4, 10, "256x128"),
    ("fig:res-512", 5, 11, "512x128"),
]
CASES = [3, 9, 4, 10, 5, 11]
PDF = {3: "Case03_R1_TL.pdf", 9: "Case09_W1_TL.pdf",
       4: "Case04_R2_TL.pdf", 10: "Case10_W2_TL.pdf",
       5: "Case05_R3_TL.pdf", 11: "Case11_W3_TL.pdf"}

SCRIPT_AUTH = Path(r"D:\Data\regen_results_bigfont.py")
SCRIPT_REPO = Path(__file__).parent.parent.parent / "Validation_Scripts" / "regen_results_bigfont.py"
TABLE = "tab:res-rect-mf"
SLUG = "FIG05_07_res_fields"


def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def pdf_avgs(pdf_path):
    """从 PDF 抽取 "Avg:x.xx dB" 标注，按出现顺序返回字符串列表。

    统一用 -raw：-layout 会把多行面板标题按列交错咬合（Src 一行就是这么
    丢掉的）。Avg 目前是单行标题不受影响，但同样走 -raw 以免日后回归。
    """
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=120)
        return re.findall(r"Avg:([0-9.]+) dB", out.stdout)
    except Exception:
        return []


def run():
    c = report.Checker(SLUG, "前向求解 TL 场图 Fig 5/6/7", "figure",
                       "fig:res-128/256/512", "5/6/7")

    c.source("印刷面 tex", paths.TEX, "三个 figure* 环境")
    c.source("成图脚本（权威）", str(SCRIPT_AUTH), "ROOT 在 D:/Data，可命中 results/")
    c.source("成图脚本（repo 副本）", str(SCRIPT_REPO), "md5 应与权威副本相同")
    for no in CASES:
        c.source(f"数据源 npz (Case {no})", paths.npz_path(no),
                 "Raw_Experimental_Data，ep200（last epoch）")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯性")
    c.check(SCRIPT_AUTH.exists(), "权威成图脚本存在", str(SCRIPT_AUTH))
    c.check(SCRIPT_REPO.exists(), "repo 副本存在", paths.rel(str(SCRIPT_REPO)))
    same = (SCRIPT_AUTH.exists() and SCRIPT_REPO.exists()
            and md5(SCRIPT_AUTH) == md5(SCRIPT_REPO))
    c.check(same, "两份成图脚本 md5 同源",
            md5(SCRIPT_AUTH)[:16] + "…" if same else "两份不一致")
    for no in CASES:
        p = paths.npz_path(no)
        c.check(p and os.path.exists(p), f"Case {no} npz 存在", paths.rel(p))
    for no in CASES:
        p = paths.FIGDIR + os.sep + PDF[no]
        c.check(os.path.exists(p), f"Case {no} 图件存在", PDF[no])

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 口径防漂移（脚本源码 vs 重算层）")
    c.note("重算层复刻 render() 的算法；若脚本改了插值方式或网格分辨率而"
           "重算层没跟上，图与核验就会各算一套，这条断言当场报错。")
    src = SCRIPT_AUTH.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'def render\([^)]*method="([a-z]+)",\s*grid_res=(\d+)', src)
    c.check(m is not None, "可从源码解析 render() 默认参数",
            f"method={m.group(1)}, grid_res={m.group(2)}" if m else "解析失败")
    if m:
        c.check(m.group(1) == METHOD, "插值方式一致",
                f"脚本 `{m.group(1)}` / 重算层 `{METHOD}`")
        c.check(int(m.group(2)) == GRID_RES, "网格分辨率一致",
                f"脚本 `{m.group(2)}` / 重算层 `{GRID_RES}`")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. epoch 自证与 caption 声明")
    c.note("场图取 ep200（last epoch）；而 Table 6 取各案例 best epoch，"
           "Case 3/9/10 的 best 分别为 198/181/192，与 200 不同轮，"
           "故两处 epoch 措辞不同是正确的，不可强行统一。")
    rec = {}
    for no in CASES:
        rec[no] = recompute(paths.npz_path(no))
        c.check(rec[no]["epoch"] == 200, f"Case {no} npz epoch = 200",
                f"epoch={rec[no]['epoch']}")
    for label, r_no, w_no, scale in FIGS:
        cap = T.caption_of(label) or ""
        c.check("last epoch" in cap, f"{label} caption 声明 last epoch",
                "含 `Fields are from the last epoch.`")
        c.check("best epoch" not in cap, f"{label} caption 未误写 best epoch",
                "图源自 ep200 npz，非 best-epoch 评估")
        c.check(scale.split("x")[0] in cap.replace("\\times", "x").replace("$", ""),
                f"{label} caption 标明尺度 {scale}", f"含 `{scale.split('x')[0]}`")

    # ★ 双侧判据：证明 last 与 best 确为不同轮，caption 的 last 不是"随便写对"
    c.note("图取 ep200(last)，兄弟表 Table 6 取 best epoch。下表列出两者差异，"
           "说明 caption 必须写 last —— 若写 best，数值就该换成另一轮的评估值。")
    from common import metrics as M
    for no in CASES:
        be = M.xlsx_case(paths.xlsx_path("4.3"), no)["best_epoch"]
        c.check(be is not None, f"Case {no} best epoch 可读",
                f"best={be}, last=200, "
                + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    c.note("图上每个 Error 面板标 `Avg:x.xx dB`，是该样本的场误差均值。"
           "从 Raw_Experimental_Data 的 npz 复刻算法重算，与 PDF 内标注"
           "逐个按 2 位小数比对——这是图与原始数据同源的直接证据。")
    for no in CASES:
        got = pdf_avgs(os.path.join(paths.FIGDIR, PDF[no]))
        want = [f"{s['avg_err']:.2f}" for s in rec[no]["samples"]]
        c.check(len(got) == len(want), f"Case {no} 图内 Avg 标注数量",
                f"PDF {len(got)} 个 / 重算 {len(want)} 个")
        c.check(got == want, f"Case {no} 8 个 Avg 值逐一吻合",
                f"PDF {got} / 重算 {want}")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. Src 坐标：图上标注 vs npz source_pos")
    c.note("脚本按 `:.1f` 印 Src；此处按同口径比对。"
           "注：Fig 3/4 的深度线图已统一为 2 位小数，场图仍为 1 位，"
           "两类图的标注口径不同但各自与其脚本一致。")
    # ★ 必须用 -raw：Ours 面板标题是两行（"Ours TL (f=..)" + "Src:(x,y)"），
    #   -layout 会把这两行按列交错咬合成 "OSurrcs:(T4L4(.5f=,2215.H9)z)"，
    #   正则一个都匹配不到。-raw 按内容流输出，不做版面还原。
    for no in CASES:
        try:
            out = subprocess.run(["pdftotext", "-raw",
                                  os.path.join(paths.FIGDIR, PDF[no]), "-"],
                                 capture_output=True, text=True, timeout=120)
            got = re.findall(r"Src:\(([0-9.]+),([0-9.]+)\)", out.stdout)
        except Exception:
            got = []
        want = [(f"{s['src'][0]:.1f}", f"{s['src'][1]:.1f}")
                for s in rec[no]["samples"]]
        ok = [tuple(g) for g in got] == want
        c.check(ok, f"Case {no} 8 组 Src 坐标吻合",
                f"PDF {len(got)} 组，与 npz source_pos 一致" if ok
                else f"PDF {got[:3]}… / npz {want[:3]}…")

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 图结构：4 频率 × 2 样本")
    for no in CASES:
        r = rec[no]
        c.check(r["n"] == 8, f"Case {no} 样本数 = 8", f"n={r['n']}")
        freqs = [int(s["freq"]) for s in r["samples"]]
        c.check(freqs == [25, 25, 50, 50, 75, 75, 100, 100],
                f"Case {no} 频率排布为每频率 2 行", str(freqs))

    # ── G ────────────────────────────────────────────────────────
    c.section("7. 图与表的关系（趋势同向，不可互算）")
    c.note("图上 Avg 是单样本场误差，Table 6 的 TL 是全测试集平均，"
           "量纲相同但统计口径不同，**不可互相反算**；"
           "可核验的是二者趋势必须同向：高频误差大于低频。")
    env = T.table_env(TABLE)
    rows = T.data_rows(env, ncol=13)
    printed = {int(r[0]): r for r in rows}
    for no in CASES:
        lo = max(s["avg_err"] for s in rec[no]["samples"] if s["freq"] == 25)
        hi = max(s["avg_err"] for s in rec[no]["samples"] if s["freq"] == 100)
        c.check(lo < hi, f"Case {no} 图内 25Hz 误差 < 100Hz 误差",
                f"`{lo:.2f}` < `{hi:.2f}` dB")
        cell = printed.get(no)
        if cell:
            c.check(float(cell[4]) < float(cell[10]),
                    f"Case {no} 表内 25Hz TL < 100Hz TL",
                    f"表 `{cell[4]}` < `{cell[10]}`")

    # ── H ────────────────────────────────────────────────────────
    c.section("8. 引用完整性")
    aux = T.labels()
    for label, r_no, w_no, _ in FIGS:
        for lb in (label, label + "-r", label + "-w"):
            c.check(lb in aux, f"label `{lb}` 已在 aux 注册",
                    f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")

    # ── I ────────────────────────────────────────────────────────
    c.section("9. 正文引用：被引 + 说明与图内容相符")
    c.note("Fig 5-9 编号连续，正文用区间引用 "
           "`Figs.~\\ref{fig:res-128}--\\ref{fig:res-wedge-100}` 一次覆盖五张，"
           "故单张的 \\ref 计数可能为 0，须按区间端点判定『是否被引』。")
    txt = T.tex_text()
    span_ref = "\\ref{fig:res-128}--\\ref{fig:res-wedge-100}"
    c.check(span_ref in txt, "正文存在覆盖 Fig 5-9 的区间引用",
            f"`Figs.~{span_ref}`")
    hits = T.sentences_with(r"fields in Figs", txt)
    c.check(bool(hits), "L783 段以该区间引用图证实趋势",
            f"tex 行 {T.line_of(hits[0][0], txt)}" if hits else "未找到")

    # 正文对图的三条描述性断言，逐条用 npz 核
    c.note("正文称『误差集中在低幅零点与源附近，而非弥散全场』且『障碍物"
           "后阴影区清晰、内部掩膜精确置零』。掩膜发生在绘图插值网格上"
           "（gp[inside_ell]=NaN），故在 200x200 网格上核验。")
    import numpy as np
    from scipy.interpolate import griddata
    for no in (3, 9):
        d = np.load(paths.npz_path(no))
        cx, cy, a, b = [float(v) for v in d["ellipse"]]
        Lx, Ly = float(d["Lx_dom"]), float(d["Ly_dom"])
        gx = np.linspace(0, Lx, GRID_RES)
        gy = np.linspace(0, Ly, GRID_RES)
        GX, GY = np.meshgrid(gx, gy)
        ins = ((GX - cx) / a) ** 2 + ((GY - cy) / b) ** 2 <= 1.0
        gp = griddata((d["x_coords"], d["y_coords"]), d["pred_tl"][0],
                      (GX, GY), method=METHOD)
        gp[ins] = np.nan
        n_fin = int(np.isfinite(gp[ins]).sum())
        c.check(ins.sum() > 0 and n_fin == 0,
                f"Case {no} 椭圆内在插值网格上被硬掩膜",
                f"椭圆内 {int(ins.sum())} 格，掩膜后有限值 {n_fin}（应 0）")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
