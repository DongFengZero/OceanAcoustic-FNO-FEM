#!/usr/bin/env python3
"""
Fig 10/11（fig:dl-cmp-rect / fig:dl-cmp-wedge）核验

对象：五方法深度线 TL 对比图。
  Fig 10 = R1 矩形，y=56.1 m，Cases 15-19
  Fig 11 = W1 楔形，y=30.4 m，Cases 20-24

与场图（Fig 5-9）的差别：本组与 Tables 9/10 是同一次 build_group 的
两个产物（表给 MAE 数值，图给曲线），故除数值复现外，还能用 md5
证明图与表同源——这是比"各自与 npz 对得上"更强的锁。

数据源：ep200 npz，经 advantage_depth_line.py 现场提取。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import depthline as DL, paths, report, texparse as T  # noqa: E402

SLUG = "FIG10_11_dl_cmp"
FREQS = (25, 50, 75, 100)

# (图 label, 组名, 兄弟表 label, y 深度, 图编号, 案例区间)
FIGS = [
    ("fig:dl-cmp-rect", "comparison_R1_model_advantage",
     "tab:dl-cmp-rect", 56.1, "10", (15, 19)),
    ("fig:dl-cmp-wedge", "comparison_W1_model_advantage",
     "tab:dl-cmp-wedge", 30.4, "11", (20, 24)),
]
METHODS = ["Proposed (Ours)", "DeepONet", "FNO", "KNO", "CNO"]


def pdftext(pdf_path):
    """PDF 文本层。必须 -raw：-layout 会把多行面板标题按列咬合。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return out.stdout
    except Exception:
        return ""


def run():
    c = report.Checker(SLUG, "五方法深度线对比 Fig 10/11", "figure",
                       "fig:dl-cmp-rect / fig:dl-cmp-wedge", "10/11")

    c.source("印刷面 tex", paths.TEX, "两个并列 minipage，各含表+图")
    c.source("成图/取数脚本（权威）", DL.AUTH, "advantage_depth_line.py")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯与口径防漂移")
    ma, mc = DL.md5(DL.AUTH), DL.md5(DL.COPY)
    c.check(ma is not None and ma == mc, "成图脚本两份副本 md5 同源",
            f"权威 `{(ma or '-')[:8]}` / repo `{(mc or '-')[:8]}`")
    m = DL.script()
    c.check(m.GRID == 300, "GRID == 300", f"脚本内 `{m.GRID}`")
    c.check(m.METHOD == "cubic", "插值 METHOD == cubic", f"脚本内 `{m.METHOD}`")
    c.check(list(m.FREQS) == list(FREQS), "FREQS 一致",
            f"脚本内 `{list(m.FREQS)}`")
    src_txt = open(DL.AUTH, encoding="utf-8").read()
    c.check("Src ({_sx:.1f}, {_sy:.1f}) m" in src_txt,
            "脚本内 Src 为 1 位小数（全章统一口径）",
            "含 `{_sx:.1f}, {_sy:.1f}`")

    rec = {g: DL.recompute(g) for _, g, _, _, _, _ in FIGS}

    # ── B ────────────────────────────────────────────────────────
    c.section("2. epoch 自证与 caption 声明")
    import numpy as np
    for label, g, _, ydep, num, _ in FIGS:
        eps = sorted({int(np.load(p)["epoch"]) for p in rec[g]["npz"].values()})
        c.check(eps == [200], f"{label} 全部 npz epoch == 200 (last)",
                f"实得 {eps}（{len(rec[g]['npz'])} 份 npz）")
        cap = T.caption_of(label) or ""
        c.check("last epoch" in cap, f"{label} caption 声明 last epoch",
                "含 `Profiles are from the last epoch.`")
        c.check("best epoch" not in cap, f"{label} caption 未误写 best epoch",
                "深度线族一律源自 ep200 npz")
        c.check(f"{ydep}" in cap.replace("$", "").replace("\\,", ""),
                f"{label} caption 标明 y={ydep} m", f"含 `{ydep}`")
        c.check("five methods" in cap, f"{label} caption 声明 five methods", "")

    # ★ 与场图族不同：本组的兄弟表 Tables 9/10 也取 last epoch（深度线族一律
    #   ep200），故判据是"图与表 epoch 声明必须一致"，而非场图那种"必然不同"。
    c.note("深度线族的表与图同取 ep200，两侧 epoch 声明须一致；"
           "场图族则相反（表 best / 图 last），判据不能照搬。")
    for label, _, tab, _, _, _ in FIGS:
        cap_f = T.caption_of(label) or ""
        cap_t = T.caption_of(tab) or ""
        both_last = ("last epoch" in cap_f) and ("last epoch" in cap_t)
        c.check(both_last, f"{label} 与兄弟表 {tab} 同声明 last epoch",
                f"图 `{'last' if 'last epoch' in cap_f else '?'}` / "
                f"表 `{'last' if 'last epoch' in cap_t else '?'}`")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 图上 Src 标注：npz 重算 vs PDF 文本层")
    c.note("每个频率面板标题带该频率实际选中样本的 source_pos，"
           "逐频独立选样，四组坐标互不相同，写错不报编译错。")
    for label, g, _, _, _, _ in FIGS:
        txt = pdftext(DL.figure_pdf(g))
        got = re.findall(r"Src \(([0-9.]+), ([0-9.]+)\) m", txt)
        want = [(f"{rec[g]['src'][f][0]:.1f}", f"{rec[g]['src'][f][1]:.1f}")
                for f in FREQS]
        c.check(got == want, f"{label} 4 组 Src 吻合",
                f"PDF {got} / npz {want}")
        got_f = re.findall(r"f = (\d+) Hz", txt)
        c.check(got_f == [str(f) for f in FREQS],
                f"{label} 四个频率面板齐全", f"图上 `{got_f}`")
        for name in ("COMSOL", "DeepONet", "FNO", "KNO", "CNO"):
            c.check(name in txt, f"{label} 图例含 {name}", "")

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 图与表同源（Fig 10↔T9, Fig 11↔T10）")
    c.note("图与兄弟表是同一次 build_group 的两个产物。比对论文图件与"
           "脚本输出目录下同名 PDF 的 md5：相同即证明表里的 MAE 与图上的"
           "曲线出自同一次运行，不可能各自漂移。")
    for label, g, tab, _, _, _ in FIGS:
        src_pdf = DL.figure_pdf(g)
        dst_pdf = os.path.join(paths.FIGDIR, os.path.basename(src_pdf))
        m1, m2 = DL.md5(src_pdf), DL.md5(dst_pdf)
        c.check(m1 is not None and m1 == m2,
                f"{label} 论文图件与脚本产物 md5 相同",
                f"`{(m1 or '-')[:8]}` vs `{(m2 or '-')[:8]}`")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 图与兄弟表的版面归属")
    c.note("每张图与其 MAE 表绑在同一个 minipage 内（表在上、图在下），"
           "这样读者看曲线时表值就在同屏；错位会让图表分页。")
    txt_all = T.tex_text()
    aux = T.labels()
    for label, g, tab, _, _, _ in FIGS:
        pf = txt_all.find("\\label{" + label + "}")
        pt = txt_all.find("\\label{" + tab + "}")
        ok = pt > 0 and pf > pt and (pf - pt) < 3000
        c.check(ok, f"{label} 与兄弟表 {tab} 同处一个 minipage",
                f"表在图之前 {'成立' if ok else '不成立'}"
                f"（间距 {pf - pt if pt > 0 else '-'} 字符）")

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 正文引用")
    span = "\\ref{fig:dl-cmp-rect}--\\ref{fig:dl-cmp-wedge}"
    c.check(span in txt_all, "正文以区间引用覆盖 Fig 10/11",
            f"含 `Figs.~{span}`")
    for label, _, _, _, num, _ in FIGS:
        c.check(aux.get(label, {}).get("num") == num,
                f"{label} 编号为 {num}",
                f"aux `{aux.get(label, {}).get('num', '缺失')}`")

    return c

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
