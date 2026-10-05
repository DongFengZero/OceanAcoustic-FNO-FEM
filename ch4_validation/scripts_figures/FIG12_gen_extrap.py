#!/usr/bin/env python3
"""
Fig 12（fig:gen-grid）核验 — R1

对象：源位置外推场图，两张子图，各 8 行（4 频率 x 2 样本）x 3 列（Ours / COMSOL / Error）：
        (a) fig:gen-r9  = gen_extrap_R9.pdf  = Fig. 12a，Case 39 R9，矩形，depth 外推 y>96 m
        (b) fig:gen-w10 = gen_extrap_W10.pdf = Fig. 12b，Case 42 W10，楔形，range 外推 x>96 m
      余下两个分割（R10 远区、W9 深区）作为补充材料 Fig. S7，由 FIGS1_S7_supplementary 核验。

两幅都由 fig04_05_10_fields/fig04_05_10_fields.py 的 FIG12 列表生成（rows_multi 逐频率取
前 2 个样本，tags=True），行标题 `f = 25 Hz (a),  Src (78.5, 122.3)`，平均误差 `Avg 1.91 dB`
同一行。补充材料的两幅用同一渲染器（figS1_S7_supplementary.py），版式相同。

本组独有的核心判据：图上展示的样本必须**全部落在外推区内**。
caption 称 "on the held-out region"，若某个样本的源坐标落在训练区，
整张图的论点（外推能力）就不成立——这是前面各组都没有的约束。

核验链
  A. 源可追溯      两幅的 npz 与成图脚本；样本数 = 8
  B. epoch 双侧    图取 ep200(last)，兄弟表（tab:gen-overall）取 best epoch
  C. ★ 外推区归属  8 个展示样本的源坐标全在 held-out 区内（阈值与表一致）
  D. Avg 标注      图上 Avg x.xx dB 与 npz 全精度重算逐一吻合
  E. 子图对应      gen-r9/gen-w10 与数据集名、几何、外推类型、阈值对应
  F. caption       取样措辞、last epoch、两种几何、指向 Fig. S7
  G. 余下两幅      R10/W9 不在正文（aux 无登记），图件在补充材料目录
  H. 正文引用      图号 12；正文把 Fig. 12（R9/W10）与 Fig. S7（R10/W9）并列引用
"""
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG12_gen_extrap"
LABEL = "fig:gen-grid"
NUMBER = 12
SIB = "tab:gen-overall"
SRC_SCRIPT = os.path.join(paths.PLOTDIR, "fig04_05_10_fields",
                          "fig04_05_10_fields.py")
SUPPDIR = os.path.join(os.path.dirname(paths.TEX), "Figures", "supplementary")

# (case, 数据集, 子图 label, 子图字母, PDF, 几何, 外推类型, 阈值 m)
SUBS = [
    (39, "R9", "fig:gen-r9", "a", "gen_extrap_R9.pdf", "rectangular", "depth", 96),
    (42, "W10", "fig:gen-w10", "b", "gen_extrap_W10.pdf", "wedge", "range", 96),
]
# 余下两个分割：补充材料 Fig. S7（图件在 Figures/supplementary/）
SUBS_SUPP = [
    (40, "R10", "figS7a_gen_extrap_r10.pdf"),
    (41, "W9", "figS7b_gen_extrap_w9.pdf"),
]


def pdftext(pdf_path):
    """PDF 文本层，必须 -raw（-layout 会把多行标题按列咬合）。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return out.stdout
    except Exception:
        return ""


def pdf_avgs(pdf_path):
    """PDF 内 `Avg x.xx dB` 标注，按出现顺序（即 8 行序）。"""
    return re.findall(r"Avg ([0-9.]+) dB", pdftext(pdf_path))


def flat(s):
    return re.sub(r"\s+", " ", (s or "")).replace("$", "").replace(chr(92) + ",", "")


def run():
    sys.path.insert(0, str(Path(__file__).parent))
    from _recompute_field import recompute
    from common import metrics as M

    n_sib = T.number_of(SIB)
    c = report.Checker(SLUG, "源位置外推场图 Fig 12（矩形 R9 深区 + 楔形 W10 远区）", "figure",
                       LABEL, str(NUMBER))

    c.source("印刷面 tex", paths.TEX,
             f"`\\label{{{LABEL}}}` 所在 figure*，含 2 个 subfloat（R9 | W10）")
    c.source("成图脚本", SRC_SCRIPT, "fig04_05_10_fields.py 的 FIG12 列表生成 gen_extrap_r9/w10")
    c.source("兄弟表", paths.TEX, f"`\\label{{{SIB}}}` = Table {n_sib}（best epoch）")
    for no, ds, *_ in SUBS:
        c.source(f"数据源 npz (Case {no} {ds})", paths.npz_path(no),
                 "Raw_Experimental_Data/4.7，ep200")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯与样本数")
    c.check(os.path.exists(SRC_SCRIPT), "成图脚本已入库", paths.rel(SRC_SCRIPT))
    src_txt = open(SRC_SCRIPT, encoding="utf-8").read()
    c.check('FIG12 = [("Case39", "gen_extrap_r9"), ("Case42", "gen_extrap_w10")]' in src_txt,
            "脚本 FIG12 列表 = Case39→gen_extrap_r9, Case42→gen_extrap_w10", "")
    c.check('"f = %d Hz%s,  Src (%.1f, %.1f)"' in src_txt,
            "脚本内行标题格式为 `f = NN Hz (a/b),  Src (x.x, y.y)`", "")
    c.check('"Avg %.2f dB" % avg' in src_txt,
            "脚本内平均误差标注为 `Avg %.2f dB`（2 位小数）", "")

    rec = {no: recompute(paths.npz_path(no)) for no, *_ in SUBS}
    for no, ds, _, _, pdf, *_ in SUBS:
        c.check(rec[no]["n"] == 8, f"Case {no} {ds} npz 样本数 = 8",
                f"4 频率 x 2 样本，实得 {rec[no]['n']}")
        c.check(os.path.exists(os.path.join(paths.FIGDIR, pdf)), f"{pdf} 存在", pdf)

    # ── B ────────────────────────────────────────────────────────
    c.section("3. epoch 双侧判据与 caption 声明")
    c.note(f"图取 ep200(last)，兄弟表 Table {n_sib} 取 best epoch，本是两套口径。"
           "故除『caption 含 last』外，还须断言『caption 未误写 best』。")
    cap = flat(T.caption_of(LABEL))
    c.check("Fields are from the last epoch" in cap, "caption 声明 last epoch", "")
    c.check("best epoch" not in cap, "caption 未误写 best epoch", "")
    for no, ds, *_ in SUBS:
        eps = {int(__import__("numpy").load(paths.npz_path(no))["epoch"])}
        c.check(eps == {200}, f"Case {no} {ds} npz epoch == 200 (last)", f"实得 {sorted(eps)}")
        be = M.xlsx_case(paths.xlsx_path("4.7"), no)["best_epoch"]
        c.check(be is not None, f"Case {no} best epoch 可读",
                f"best={be}, last=200, " + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── C ────────────────────────────────────────────────────────
    c.section("4. ★ 展示样本必须全部落在外推区内")
    c.note("caption 称『on the held-out region』。若有任一展示样本的源坐标"
           "落在训练区内，整张图的论点（外推能力）就不成立。逐样本核 8 个源坐标的区域归属。")
    tbl = T.table_body_of(SIB)[0] or ""
    rows = [r for r in T.data_rows(tbl, ncol=13) if r and r[0].isdigit()]
    c.check(len(rows) == 4, f"Table {n_sib} 解析到 4 行（R9/R10/W9/W10）", f"实得 {len(rows)}")
    for no, ds, _, _, _, _, kind, thr in SUBS:
        bad = []
        for s in rec[no]["samples"]:
            x, y = s["src"]
            inside = (y > thr) if kind == "depth" else (x > thr)
            if not inside:
                bad.append(f"({x:.1f},{y:.1f})")
        c.check(not bad, f"Case {no} {ds} 8 个样本全在外推区（{kind} > {thr} m）内",
                "全部合规" if not bad else "越界: " + ", ".join(bad))
        r = next((r for r in rows if r[0] == str(no)), None)
        c.check(r is not None, f"Table {n_sib} 含 Case {no} 行", "")
        if r is not None:
            c.check(f"{thr}" in r[2], f"Table {n_sib} 的 {ds} 阈值与图一致（{thr} m）",
                    f"表列 `{r[2]}` / 图 {kind} > {thr}")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    c.note("`Avg x.xx dB` 与频率/声源同排一行；重算给全精度，判定用舍入到 2 位的印刷值。")
    for no, ds, _, _, pdf, *_ in SUBS:
        got = pdf_avgs(os.path.join(paths.FIGDIR, pdf))
        want = [f"{s['avg_err']:.2f}" for s in rec[no]["samples"]]
        c.check(got == want, f"Case {no} {ds} 8 个 Avg 逐一吻合",
                "全部吻合" if got == want else f"PDF {got} / npz 重算 {want}")
        c.check(len(got) == 8, f"Case {no} {ds} 图上解析到 8 个 Avg 标注", f"实得 {len(got)}")
        txt = pdftext(os.path.join(paths.FIGDIR, pdf))
        got_src = re.findall(r"Src \(([0-9.]+), ([0-9.]+)\)", txt)
        want_src = [("%.1f" % s["src"][0], "%.1f" % s["src"][1]) for s in rec[no]["samples"]]
        c.check(got_src == want_src, f"Case {no} {ds} 8 个 Src 坐标吻合",
                f"PDF {got_src} / npz {want_src}")
        got_f = re.findall(r"f = (\d+) Hz \(([ab])\)", txt)
        c.check([f for f, _ in got_f] == ["25", "25", "50", "50", "75", "75", "100", "100"],
                f"Case {no} {ds} 8 行频率序 = 每频率 2 样本", f"图上 `{got_f}`")
        c.check([t for _, t in got_f] == ["a", "b"] * 4,
                f"Case {no} {ds} 行标签的样本字母为 a/b 交替", "每频率两个样本标 (a)/(b)")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 子图 label 与数据集名 / 几何 / 外推类型 / 阈值对应")
    aux = T.labels()
    txt = T.tex_text()
    for no, ds, sub_lb, letter, _, geom, kind, thr in SUBS:
        n_sub = aux.get(sub_lb, {}).get("num", "缺失")
        c.check(n_sub.startswith(str(NUMBER)), f"子图 `{sub_lb}` 编号前缀为 {NUMBER}", f"aux `{n_sub}`")
        c.check(n_sub.endswith(letter), f"子图 `{sub_lb}` 是 Fig. {NUMBER}{letter}", f"aux `{n_sub}`")
        i = txt.find(chr(92) + "label{" + sub_lb + "}")
        b = txt.rfind(chr(92) + "subfloat[", 0, i)
        e = txt.find("]", b)
        title = flat(txt[b + len(chr(92) + "subfloat["):e]) if b >= 0 else ""
        c.check(ds in title, f"子图 `{sub_lb}` 题注含数据集名 {ds}", f"题注 `{title}`")
        c.check(geom in title, f"子图 `{sub_lb}` 题注标明几何 {geom}", f"题注 `{title}`")
        kw = "deep" if kind == "depth" else "range"
        c.check(kw in title, f"子图 `{sub_lb}` 题注标明 {kw} extrapolation",
                f"题注 `{title}`；tex 用 `{kw}`，Table {n_sib} 同一划分记作 `{kind}`")
        c.check(str(thr) in title, f"子图 `{sub_lb}` 题注标明阈值 {thr} m", f"题注 `{title}`")

    # ── F ────────────────────────────────────────────────────────
    c.section("7. caption 的取样措辞与实际机制相符")
    c.note("本组按索引顺序取每频率前 2 个样本（非择优），故 caption 应写 the first two，"
           "不应含混称 representative；两幅分属两种几何，caption 须两者都点明，并指向 Fig. S7。")
    c.check("first two" in cap, "caption 写明取每频率前两个样本", "含 `the first two held-out samples`")
    c.check("representative" not in cap, "caption 未含混使用 representative", "")
    c.check("labelled a/b" in cap, "caption 说明行以 a/b 标样本", "")
    c.check("rectangular" in cap.lower() and "wedge" in cap.lower(), "caption 同时点明矩形与楔形", "")
    c.check("R9" in cap and "W10" in cap, "caption 标出 R9 与 W10", "")
    c.check("Fig.~S7" in (T.caption_of(LABEL) or "") and "R10" in cap and "W9" in cap,
            "caption 指出余下两幅（R10, W9）在 Fig.~S7", "")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 余下两个分割（R10/W9）在补充材料")
    for lb in ("fig:gen-grid-wedge", "fig:gen-r10", "fig:gen-w9"):
        c.check(aux.get(lb) is None, f"`{lb}` 不在正文（aux 无登记）", "R10/W9 两幅在补充材料 Fig. S7")
    c.check(chr(92) + "label{fig:gen-grid-wedge}" not in txt,
            "旧楔形浮动体的注释残留已清除", "")
    for no, ds, pdf in SUBS_SUPP:
        c.check(os.path.exists(os.path.join(SUPPDIR, pdf)),
                f"补充材料图件 {pdf}（Case {no} {ds}）存在", paths.rel(os.path.join(SUPPDIR, pdf)))

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 正文引用")
    c.check(chr(92) + "ref{" + LABEL + "}" in txt, "正文引用 Fig. 12", "")
    want = (chr(92) + "ref{" + LABEL + "} shows the rectangular deep split (R9) and the wedge "
            "far-range split (W10), and Fig.~S7 of the Supplementary Material the remaining two (R10, W9)")
    c.check(want in txt, "正文 4.7 节把 Fig. 12（R9/W10）与 Fig. S7（R10/W9）并列引用", "")
    hits = T.sentences_with(r"held-out extrapolation region", txt)
    c.check(bool(hits), "正文描述该组图的内容",
            f"tex 行 {T.line_of(hits[0][0], txt)}" if hits else "未找到")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
