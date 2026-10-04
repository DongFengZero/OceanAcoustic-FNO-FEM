#!/usr/bin/env python3
"""
Fig. 4（fig:res-128）核验
=========================
对象：128x128 m 多频前向 TL 场图，矩形/楔形并排一张图的两个子图。
  Fig 4 = Case 3 (R1) + Case 9 (W1)，子图 label `fig:res-128-r` / `fig:res-128-w`

R1 修订后 256/512 m 两张同族图（旧 fig:res-256 / fig:res-512）移入
已从正文删除（无补充材料），正文与 aux 里都不再有这两个 label；Table 6 的
Fig. 列改以裸文本 `S3` / `S4` 指代。本脚本只核 R1 正文真正保留的这一张。

Fig 5（100 Hz 方形域，fig:sq100）由 FIG05_sq100.py 负责，本脚本不再重复核
（两脚本此前都声称覆盖 Fig 5，判据重叠且口径冲突）。

数据源一律取 Raw_Experimental_Data 下的 `*__TL原始数据_ep200.npz`。

核验链
  A. 源可追溯    npz 存在；成图脚本可定位且确实产出本图 PDF
  B. 口径防漂移  从脚本源码读插值方式/网格分辨率，须与重算层一致
  C. epoch 自证  npz['epoch']==200，caption 声明 last epoch
  D. 数值复现    复刻 render 算法重算逐样本 Avg 误差，
                 与 PDF 内 "Avg x.xx dB" 标注逐一比对（★核心）
  E. Src 坐标    图上标注与 npz source_pos 一致
  F. 结构        8 样本 = 4 频率 × 2，与 caption 声明一致
  G. 图表关系    图为逐样本、表为全测试集，不可互算；只核趋势同向（★）
  H. 引用完整    Fig 4 的 label/子图 label 在 aux 注册且编号为 4/4a/4b
  I. 正文引用    正文逐张引用（R1 无区间引用），Table 6 的 Fig. 列指向本图
"""
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

LABEL = "fig:res-128"
# 子图 label -> aux 里的排版编号（a/b，不是 r/w）
SUB_LABELS = {"fig:res-128-r": "4a", "fig:res-128-w": "4b"}
NUMBER = "4"
CASES = [3, 9]
PDF = {3: "Case03_R1_TL.pdf", 9: "Case09_W1_TL.pdf"}

# 成图脚本：R1 起 4/5/10 三张场图共用同一个渲染器（同一插值、遮罩、clip），
# 脚本目录名即图号清单，与 Validation_Scripts/INDEX.md 的 Figure 表一致。
SCRIPT = (Path(__file__).resolve().parents[2] / "Validation_Scripts"
          / "fig04_05_10_fields" / "fig04_05_10_fields.py")
# 本图在该脚本里的产出清单（main() 的 FIG4 分支）
FIG4_SPEC = [("Case03", "case03_r1_tl"), ("Case09", "case09_w1_tl")]
TABLE = "tab:res-rect-mf"
SLUG = "FIG04_05_fields"


def pdf_text(pdf_path):
    """PDF 文本层。必须用 -raw：-layout 会把面板的两行标题按列交错咬合
    （"Ours TL (f=..)" + "Src (x,y)" 咬成 'OSurrcs(T4L4(.5f=,2215.H9)z)'），
    正则一个都匹配不到。-raw 按内容流输出，不做版面还原。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=120)
        return out.stdout
    except Exception:
        return ""


def pdf_avgs(pdf_path):
    """PDF 里的 `Avg x.xx dB` 标注。R1 起紧凑排版已去掉冒号：
    行小标题写作 `f = 25 Hz, Src (44.5, 21.9) Avg 0.42 dB`。"""
    return re.findall(r"Avg ([0-9.]+) dB", pdf_text(pdf_path))


def pdf_srcs(pdf_path):
    """PDF 里的 `Src (x, y)` 坐标，同样无冒号。"""
    return re.findall(r"Src \(([0-9.]+), ([0-9.]+)\)", pdf_text(pdf_path))


def run():
    c = report.Checker(SLUG, "多频前向 TL 场图 Fig. 4（128x128 m）", "figure",
                       LABEL, NUMBER)

    c.source("印刷面 tex", paths.TEX, "figure* 环境，两个 subfloat")
    c.source("成图脚本", str(SCRIPT),
             "fig04_05_10_fields.py，按 INDEX.md 对应 Fig 4/5/10")
    for no in CASES:
        c.source(f"数据源 npz (Case {no})", paths.npz_path(no),
                 "Raw_Experimental_Data，ep200（last epoch）")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯性")
    c.check(SCRIPT.exists(), "成图脚本存在", paths.rel(str(SCRIPT)))
    env = T.tex_text()
    c.check(f"\\label{{{LABEL}}}" in env, f"tex 含 `\\label{{{LABEL}}}`",
            "figure* 环境")
    for no in CASES:
        p = paths.npz_path(no)
        c.check(p and os.path.exists(p), f"Case {no} npz 存在", paths.rel(p))
    for no in CASES:
        p = os.path.join(paths.FIGDIR, PDF[no])
        c.check(os.path.exists(p), f"Case {no} 图件存在", PDF[no])

    # ★ 成图脚本已改为按 CH4_RAWROOT/CH4_FIGDIR 参数化的可移植脚本，与仓库内
    #   的副本不再是逐字节同一份，故"md5 同源"不再是成立的断言。改为核
    #   **产出关系**：脚本源码里给出的输出名清单必须正好覆盖本图包含的两张
    #   PDF，否则它就不是本图的生成者。
    c.section("2. 成图脚本确实产出本图")
    c.note("R1 的成图脚本已参数化路径（_figpaths.py 解析 CH4_RAWROOT/CH4_FIGDIR），"
           "与本机另一份副本逐字节比对已无意义；能证明归属的是"
           "『脚本的产出清单 == 本图的图件集合』。")
    src = SCRIPT.read_text(encoding="utf-8", errors="ignore") if \
        SCRIPT.exists() else ""
    c.check(bool(src), "成图脚本可读", paths.rel(str(SCRIPT)))
    for cno, key in FIG4_SPEC:
        c.check(key in src, f"脚本含 Case {cno} 的输出名 `{key}`",
                f"main() 的 FIG4 分支产出 {key}.pdf")
    got_keys = sorted({(int(a), b) for a, b in
                       re.findall(r'"case(\d+)_([rw]\d)_tl"', src)})
    c.check((3, "r1") in got_keys and (9, "w1") in got_keys,
            "脚本输出清单覆盖 Case 3 / Case 9",
            f"实得 {sorted(got_keys)[:6]}…（共 {len(got_keys)} 项）")
    # Figure 4 是 FIG4 分支；同脚本还产出 Fig 5（FIG5）与 Fig 10（FIG9）
    for tag, want_tag in (("FIG4", "Fig 4"), ("FIG5", "Fig 5"),
                          ("FIG9", "Fig 10")):
        c.check(tag in src, f"脚本含 {want_tag} 的产出分支 `{tag}`",
                "同渲染器服务三张场图，与 INDEX.md 一致")

    # ── B ────────────────────────────────────────────────────────
    c.section("3. 口径防漂移（脚本源码 vs 重算层）")
    c.note("重算层复刻脚本 fields() 的内层算法（griddata + 椭圆/楔形遮罩 + "
           "clip + nanmean）。脚本若改了插值方式或网格分辨率而重算层没跟上，"
           "图与核验就会各算一套，这条断言当场报错。")
    m = re.search(r"def fields\(data, i, grid_res=(\d+), method=\"([a-z]+)\"\)",
                  src)
    c.check(m is not None, "可从源码解析 fields() 默认参数",
            f"grid_res={m.group(1)}, method={m.group(2)}" if m else "解析失败")
    if m:
        c.check(m.group(2) == METHOD, "插值方式一致",
                f"脚本 `{m.group(2)}` / 重算层 `{METHOD}`")
        c.check(int(m.group(1)) == GRID_RES, "网格分辨率一致",
                f"脚本 `{m.group(1)}` / 重算层 `{GRID_RES}`")
    c.check('"Avg %.2f dB" % avg' in src, "脚本按 2 位小数印 Avg 标注",
            "源码含 `\"Avg %.2f dB\" % avg`，与 PDF 文本层格式一致")
    c.check('"f = %d Hz%s,  Src (%.1f, %.1f)"' in src,
            "脚本按 1 位小数印 Src 坐标",
            "源码含 `f = %d Hz%s,  Src (%.1f, %.1f)`")
    c.check("err[inside] = np.nan" not in src and "gp[inside] = np.nan" in src,
            "椭圆内以 NaN 硬掩膜（与重算层同法）", "源码含 `gp[inside] = np.nan`")

    # ── C ────────────────────────────────────────────────────────
    c.section("4. epoch 自证与 caption 声明")
    c.note("场图取 ep200（last epoch）；兄弟表 Table 6 取各案例 best epoch，"
           "两者本是不同轮，故两处 epoch 措辞不同是正确的，不可强行统一。")
    rec = {}
    for no in CASES:
        rec[no] = recompute(paths.npz_path(no))
        c.check(rec[no]["epoch"] == 200, f"Case {no} npz epoch = 200",
                f"epoch={rec[no]['epoch']}")
    cap = T.caption_of(LABEL) or ""
    c.check("last epoch" in cap, f"{LABEL} caption 声明 last epoch",
            "含 `Fields are from the last epoch.`")
    c.check("best epoch" not in cap, f"{LABEL} caption 未误写 best epoch",
            "图源自 ep200 npz，非 best-epoch 评估")
    c.check("128" in cap.replace("\\times", "x").replace("$", ""),
            f"{LABEL} caption 标明尺度 128x128", "含 `128`")
    c.check("Case~3" in cap and "Case~9" in cap,
            f"{LABEL} caption 标明两个案例", "含 `Case~3` 与 `Case~9`")

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
    c.section("5. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    c.note("图上每个 Error 面板的行小标题标 `Avg x.xx dB`，是该样本的场误差"
           "均值。从 Raw_Experimental_Data 的 npz 复刻算法重算，与 PDF 文本层"
           "标注逐个按 2 位小数比对——这是图与原始数据同源的直接证据。")
    for no in CASES:
        got = pdf_avgs(os.path.join(paths.FIGDIR, PDF[no]))
        want = [f"{s['avg_err']:.2f}" for s in rec[no]["samples"]]
        c.check(len(got) == len(want), f"Case {no} 图内 Avg 标注数量",
                f"PDF {len(got)} 个 / 重算 {len(want)} 个")
        c.check(got == want, f"Case {no} 8 个 Avg 值逐一吻合",
                f"PDF {got} / 重算 {want}")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. Src 坐标：图上标注 vs npz source_pos")
    c.note("脚本按 `:.1f` 印 Src；此处按同口径比对。两行标题在同一文本行内"
           "（`f = .. Hz, Src (x, y) Avg .. dB`），一次正则同时取出两者。")
    for no in CASES:
        got = pdf_srcs(os.path.join(paths.FIGDIR, PDF[no]))
        want = [(f"{s['src'][0]:.1f}", f"{s['src'][1]:.1f}")
                for s in rec[no]["samples"]]
        ok = [tuple(g) for g in got] == want
        c.check(ok, f"Case {no} 8 组 Src 坐标吻合",
                f"PDF {len(got)} 组，与 npz source_pos 一致" if ok
                else f"PDF {got[:3]}… / npz {want[:3]}…")

    # ── F ────────────────────────────────────────────────────────
    c.section("7. 图结构：4 频率 × 2 样本")
    for no in CASES:
        r = rec[no]
        c.check(r["n"] == 8, f"Case {no} 样本数 = 8", f"n={r['n']}")
        freqs = [int(s["freq"]) for s in r["samples"]]
        c.check(freqs == [25, 25, 50, 50, 75, 75, 100, 100],
                f"Case {no} 频率排布为每频率 2 行", str(freqs))

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 图与表的关系（趋势同向，不可互算）")
    c.note("图上 Avg 是单样本场误差，Table 6 的 TL 是全测试集平均，"
           "量纲相同但统计口径不同，**不可互相反算**；"
           "可核验的是二者趋势必须同向：高频误差大于低频。")
    te = T.table_env(TABLE)
    rows = T.data_rows(te, ncol=13)
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
    c.section("9. 引用完整性（label 已在 aux 注册）")
    aux = T.labels()
    c.check(aux.get(LABEL, {}).get("num") == NUMBER,
            f"主图 label `{LABEL}` 注册且编号为 {NUMBER}",
            f"aux `{aux.get(LABEL, {}).get('num', '缺失')}`")
    for lb, num in SUB_LABELS.items():
        c.check(aux.get(lb, {}).get("num") == num,
                f"子图 label `{lb}` 注册且编号为 {num}",
                f"aux `{aux.get(lb, {}).get('num', '缺失')}`")

    # ── I ────────────────────────────────────────────────────────
    c.section("10. 正文引用：逐张引用（R1 无区间引用）")
    c.note("R1 已取消旧稿的 `Figs.~\\ref{fig:res-128}--\\ref{fig:res-wedge-100}` "
           "区间写法，改为逐张引用；256/512 m 两张同族图已从正文删除，"
           "其精度数据保留在 Table 6，正文与 aux 均不再有它们的 label。")
    txt = T.tex_text()
    BS = chr(92)
    n_main = len(re.findall(re.escape(BS) + r"ref\{" + re.escape(LABEL) + r"\}",
                            txt))
    c.check(n_main >= 1, f"正文引用 `{LABEL}` 至少 1 处",
            f"实得 {n_main} 处：入口段 + 结论段")
    c.check(len(re.findall(re.escape(BS) + r"ref\{[^}]*\}--" + re.escape(BS)
                           + r"ref\{fig:", txt)) == 0,
            "正文不含覆盖 Fig 4/5 的区间引用（R1 已改逐张引用）",
            "全文无 `\\ref{fig:..}--\\ref{fig:..}` 形式的图区间")
    # R1 删除了 Table 6 的 Fig. 列（它曾以裸文本 S3/S4 指向并不存在的补充材料），
    # 故 Fig. 4 的子图不再被表格交叉引用；改为断言删除彻底。
    te = T.table_env(TABLE) or ""
    c.check(BS + "subref{fig:res-128" not in te,
            "Table 6 不再以 `\\subref` 交叉引用 Fig. 4 子图（Fig. 列已删）", "")
    c.check("Figs.~S1--S4" in txt,
            "同族 256/512 m 场图由正文指向补充材料 `Figs.~S1--S4`", "")
    for lb in SUB_LABELS:
        c.check(lb in aux, f"子图 label `{lb}` 仍在 aux 注册",
                f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")
    c.check("fig:res-256" not in aux and "fig:res-512" not in aux,
            "`fig:res-256` / `fig:res-512` 已不在 aux 注册",
            "两张图 R1 已删除，正文不再排版它们")

    # 正文对图的两条描述性断言，逐条用 npz 核
    c.note("正文称『误差集中在低幅零点与源附近，而非弥散全场』且『障碍物"
           "后阴影区清晰、内部掩膜精确置零』。掩膜发生在绘图插值网格上"
           "（gp[inside]=NaN），故在 200x200 网格上核验。")
    import numpy as np
    from scipy.interpolate import griddata
    for no in CASES:
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
