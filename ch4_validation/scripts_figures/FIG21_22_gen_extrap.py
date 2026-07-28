#!/usr/bin/env python3
"""
Fig 21/22（fig:gen-grid / fig:gen-grid-wedge）核验

对象：源位置外推场图，各 2 个子图。
  Fig 21 = gen_extrap_R9.pdf (21a) + gen_extrap_R10.pdf (21b)  矩形
  Fig 22 = gen_extrap_W9.pdf (22a) + gen_extrap_W10.pdf (22b)  楔形

本组独有的核心判据：图上展示的样本必须**全部落在外推区内**。
caption 称 "on the held-out region"，若某个样本的源坐标落在训练区，
整张图的论点（外推能力）就不成立——这是前面各组都没有的约束。

其余沿用场图族链路：Avg 误差复现、epoch 双侧判据、外推区阈值与
Table 19 的 Extrap. region 列一致、子图 label 与阈值对应。

数据源：Raw_Experimental_Data/4.7 下各 case 的 ep200 npz。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG21_22_gen_extrap"
SCRIPT_AUTH = Path(r"D:\Data\regen_gen_extrap_bigfont.py")
SCRIPT_REPO = Path(r"D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts"
                   r"\regen_gen_extrap_bigfont.py")

# (图 label, 图号, [(case, 数据集, 子图 label, PDF, 外推类型, 阈值), ...])
FIGS = [
    ("fig:gen-grid", "21", [
        (39, "R9", "fig:gen-r9", "gen_extrap_R9.pdf", "depth", 96),
        (40, "R10", "fig:gen-r10", "gen_extrap_R10.pdf", "range", 96),
    ]),
    ("fig:gen-grid-wedge", "22", [
        (41, "W9", "fig:gen-w9", "gen_extrap_W9.pdf", "depth", 48),
        (42, "W10", "fig:gen-w10", "gen_extrap_W10.pdf", "range", 96),
    ]),
]
SUBS = [s for _, _, subs in FIGS for s in subs]


def md5(p):
    import hashlib
    try:
        return hashlib.md5(Path(p).read_bytes()).hexdigest()
    except Exception:
        return None


def pdf_avgs(pdf_path):
    """PDF 内 "Avg:x.xx dB" 标注。必须 -raw（-layout 会咬合多行标题）。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return re.findall(r"Avg:([0-9.]+) dB", out.stdout)
    except Exception:
        return []


def run():
    sys.path.insert(0, str(Path(__file__).parent))
    from _recompute_field import recompute, METHOD, GRID_RES
    from common import metrics as M

    c = report.Checker(SLUG, "源位置外推场图 Fig 21/22", "figure",
                       "fig:gen-grid / fig:gen-grid-wedge", "21/22")
    c.source("印刷面 tex", paths.TEX, "两个 figure* 环境，各 2 个 subfloat")
    c.source("成图脚本（权威）", str(SCRIPT_AUTH), "regen_gen_extrap_bigfont.py")
    for no, ds, _, _, _, _ in SUBS:
        c.source(f"数据源 npz (Case {no} {ds})", paths.npz_path(no),
                 "Raw_Experimental_Data/4.7，ep200")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯与口径防漂移")
    ma, mc = md5(SCRIPT_AUTH), md5(SCRIPT_REPO)
    c.check(ma is not None and ma == mc, "成图脚本两份副本 md5 同源",
            f"权威 `{(ma or '-')[:8]}` / repo `{(mc or '-')[:8]}`")
    src_txt = open(SCRIPT_AUTH, encoding="utf-8").read()
    c.check("Src:({src[0]:.1f},{src[1]:.1f})" in src_txt,
            "脚本内 Src 为 1 位小数（全章统一口径）", "")
    rec = {no: recompute(paths.npz_path(no)) for no, _, _, _, _, _ in SUBS}
    for no, ds, _, pdf, _, _ in SUBS:
        c.check(rec[no]["n"] == 8, f"Case {no} {ds} npz 样本数 = 8",
                f"4 频率 x 2 样本，实得 {rec[no]['n']}")
        c.check(os.path.exists(os.path.join(paths.FIGDIR, pdf)),
                f"{pdf} 存在", pdf)

    # ── B ────────────────────────────────────────────────────────
    c.section("2. epoch 双侧判据")
    c.note("图取 ep200(last)，兄弟表 Table 19 取 best epoch，本是两套口径。"
           "故除『caption 含 last』外，还须断言『caption 未误写 best』。")
    for label, num, subs in FIGS:
        cap = T.caption_of(label) or ""
        c.check("last epoch" in cap, f"{label} caption 声明 last epoch", "")
        c.check("best epoch" not in cap, f"{label} caption 未误写 best epoch", "")
    for no, ds, _, _, _, _ in SUBS:
        eps = {int(__import__("numpy").load(paths.npz_path(no))["epoch"])}
        c.check(eps == {200}, f"Case {no} {ds} npz epoch == 200 (last)",
                f"实得 {sorted(eps)}")
        be = M.xlsx_case(paths.xlsx_path("4.7"), no)["best_epoch"]
        c.check(be is not None, f"Case {no} best epoch 可读",
                f"best={be}, last=200, "
                + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── C ────────────────────────────────────────────────────────
    c.section("3. ★ 展示样本必须全部落在外推区内")
    c.note("caption 称『on the held-out region』。若有任一展示样本的源坐标"
           "落在训练区内，整张图的论点（外推能力）就不成立——这是本组独有"
           "的约束，前面各组都没有。逐样本核 8 个源坐标的区域归属。")
    for no, ds, _, _, kind, thr in SUBS:
        bad = []
        for s in rec[no]["samples"]:
            x, y = s["src"]
            inside = (y > thr) if kind == "depth" else (x > thr)
            if not inside:
                bad.append(f"({x:.1f},{y:.1f})")
        c.check(not bad,
                f"Case {no} {ds} 8 个样本全在外推区（{kind} > {thr} m）内",
                "全部合规" if not bad else "越界: " + ", ".join(bad))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    for no, ds, _, pdf, _, _ in SUBS:
        got = pdf_avgs(os.path.join(paths.FIGDIR, pdf))
        want = [f"{s['avg_err']:.2f}" for s in rec[no]["samples"]]
        c.check(got == want, f"Case {no} {ds} 8 个 Avg 逐一吻合",
                f"PDF {got} / npz 重算 {want}")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 子图 label 与外推类型/阈值对应")
    aux = T.labels()
    txt = T.tex_text()
    for label, num, subs in FIGS:
        c.check(aux.get(label, {}).get("num") == num,
                f"{label} 编号为 {num}", f"aux `{aux.get(label, {}).get('num')}`")
        for no, ds, sub_lb, _, kind, thr in subs:
            # 子图 label 已在 aux 注册，且编号为 21a/21b/22a/22b 形式
            n_sub = aux.get(sub_lb, {}).get("num", "缺失")
            c.check(n_sub.startswith(num) and n_sub[len(num):] in ("a", "b"),
                    f"子图 `{sub_lb}` 编号为 {num}a/{num}b 之一",
                    f"aux `{n_sub}`")
            # subfloat 题注须标明数据集名与外推类型/阈值
            i = txt.find("\\label{" + sub_lb + "}")
            seg = txt[max(0, i - 400):i]
            c.check(ds in seg, f"子图 `{sub_lb}` 题注含数据集名 {ds}", "")
            # tex 题注对深度外推用 "deep"（非 "depth"），Table 19 的
            # Extrap. region 列用 "depth"。两者指同一划分，措辞按各自惯例。
            kw = "deep" if kind == "depth" else "range"
            c.check(kw in seg,
                    f"子图 `{sub_lb}` 题注标明 {kw} extrapolation",
                    f"tex 用 `{kw}`，Table 19 同一划分记作 `{kind}`")
            c.check(str(thr) in seg,
                    f"子图 `{sub_lb}` 题注标明阈值 {thr} m", "")

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 正文引用")
    c.note("正文 4.7 节以 `Figs.~\\ref{fig:gen-grid} and \\ref{fig:gen-grid-wedge}` "
           "并列引用两张图，非区间引用。")
    pair = ("\\ref{fig:gen-grid} and \\ref{fig:gen-grid-wedge}")
    c.check(pair in txt, "正文并列引用 Fig 21 与 Fig 22", f"含 `Figs.~{pair}`")
    hits = T.sentences_with(r"reports the field accuracy on the held-out", txt)
    c.check(bool(hits), "正文描述该组图的内容",
            f"tex 行 {T.line_of(hits[0][0], txt)}" if hits else "未找到")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
