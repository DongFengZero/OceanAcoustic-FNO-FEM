#!/usr/bin/env python3
"""
Fig 12（fig:gen-grid）核验 — R1

对象：源位置外推场图，**矩形两张子图**，各 8 行（4 频率 x 2 样本）x 3 列
      （Ours / COMSOL / Error）：
        (a) fig:gen-r9  = gen_extrap_R9.pdf  = Fig. 12a，Case 39 R9，depth 外推 y>96 m
        (b) fig:gen-r10 = gen_extrap_R10.pdf = Fig. 12b，Case 40 R10，range 外推 x>96 m

★ R1 把楔形两幅（W9/W10，旧 fig:gen-grid-wedge = Fig 22）**移入补充材料**
  （正文以 `Fig.~S5` 引用），故 main text 只剩矩形这一张。本脚本只核正文
  实际包含的两幅；W9/W10 的核验项显式豁免并说明去向。

本组独有的核心判据：图上展示的样本必须**全部落在外推区内**。
caption 称 "on the held-out region"，若某个样本的源坐标落在训练区，
整张图的论点（外推能力）就不成立——这是前面各组都没有的约束。

★ 成图脚本分两处（R1 起入库）：
    · 矩形 R9/R10（本图两幅）由 fig04_05_10_fields/fig04_05_10_fields.py 生成
      （FIG11 列表，rows_multi 逐频率取前 2 个样本，tags=True）
    · 楔形 W9/W10 由 fig12_gen_extrap/fig12_gen_extrap.py 生成
  两处的标注格式不同：
    R9/R10 行标题 `f = 25 Hz (a), Src (78.5, 122.3) Avg 1.91 dB`（同行）
    W9/W10 行标题 `(f=25Hz, a)` / `Src (121.5, 68.0)` / `(Avg 1.68 dB)`（三行）

核验链
  A. 源可追溯      两幅的 npz 与成图脚本；样本数 = 8
  B. epoch 双侧    图取 ep200(last)，兄弟表 Table 13 取 best epoch
  C. ★ 外推区归属  8 个展示样本的源坐标全在 held-out 区内（阈值与表一致）
  D. Avg 标注      图上 Avg x.xx dB 与 npz 全精度重算逐一吻合
  E. 子图对应      gen-r9/gen-r10 与数据集名、外推类型、阈值对应
  F. caption       取样措辞、last epoch、无 wedge 残留
  G. 正文引用      图号 12；正文以 `Fig.~\\ref{fig:gen-grid} and Fig.~S5` 引用
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
SRC_SCRIPT_W = os.path.join(paths.PLOTDIR, "fig12_gen_extrap",
                            "fig12_gen_extrap.py")

# (case, 数据集, 子图 label, 子图字母, PDF, 外推类型, 阈值 m)
SUBS = [
    (39, "R9", "fig:gen-r9", "a", "gen_extrap_R9.pdf", "depth", 96),
    (40, "R10", "fig:gen-r10", "b", "gen_extrap_R10.pdf", "range", 96),
]
# R1 已移入补充材料（正文 `Fig.~S5`），本脚本不核其正文编号
SUBS_SUPP = [
    (41, "W9", "gen_extrap_W9.pdf"),
    (42, "W10", "gen_extrap_W10.pdf"),
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
    """PDF 内 `Avg x.xx dB` / `(Avg x.xx dB)` 两种标注，按出现顺序。

    R9/R10 的行标题把频率/声源/平均误差排在同一行（`... Avg 1.91 dB`），
    W9/W10 则把 `(Avg 1.68 dB)` 单独成行。本函数两种都吃，顺序即 8 行序。
    """
    t = pdftext(pdf_path)
    return re.findall(r"Avg ([0-9.]+) dB", t)


def flat(s):
    return re.sub(r"\s+", " ", (s or "")).replace("$", "").replace(chr(92) + ",", "")


def run():
    sys.path.insert(0, str(Path(__file__).parent))
    from _recompute_field import recompute
    from common import metrics as M

    c = report.Checker(SLUG, "源位置外推场图 Fig 12（矩形 R9/R10）", "figure",
                       LABEL, str(NUMBER))

    c.source("印刷面 tex", paths.TEX,
             f"`\\label{{{LABEL}}}` 所在 figure*，含 2 个 subfloat（R9 | R10）")
    c.source("成图脚本（矩形两幅）", SRC_SCRIPT,
             "fig04_05_10_fields.py 的 FIG11 列表生成 gen_extrap_r9/r10")
    c.source("兄弟表", paths.TEX, f"`\\label{{{SIB}}}` = Table 13（best epoch）")
    for no, ds, _, _, _, _, _ in SUBS:
        c.source(f"数据源 npz (Case {no} {ds})", paths.npz_path(no),
                 "Raw_Experimental_Data/4.7，ep200")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯与样本数")
    c.check(os.path.exists(SRC_SCRIPT), "成图脚本（矩形两幅）已入库",
            paths.rel(SRC_SCRIPT))
    c.check(os.path.exists(SRC_SCRIPT_W), "成图脚本（楔形两幅）已入库（供补充材料）",
            paths.rel(SRC_SCRIPT_W))
    src_txt = open(SRC_SCRIPT, encoding="utf-8").read()
    # R9/R10 的行标题在 fig04_05_10_fields.py 的 rows_multi() 里拼装：
    #   "f = %d Hz%s,  Src (%.1f, %.1f)"  (tags=True -> " (a)"/" (b)")
    # 平均误差则由图内 "Avg %.2f dB" 标注。
    c.check('"f = %d Hz%s,  Src (%.1f, %.1f)"' in src_txt,
            "脚本内 R9/R10 行标题格式为 `f = NN Hz (a/b),  Src (x.x, y.y)`", "")
    c.check('"Avg %.2f dB" % avg' in src_txt,
            "脚本内平均误差标注为 `Avg %.2f dB`（2 位小数）", "")
    c.note("★ 本组成图脚本有两处，格式不同：R9/R10（正文 Fig 12）由 "
           "fig04_05_10_fields.py 生成，行标题 `f = 25 Hz (a),  Src (78.5, "
           "122.3)` 且平均误差排在同一行（`Avg 1.91 dB`）；W9/W10（补充材料）"
           "由 fig12_gen_extrap.py 生成，行标题拆三行（`(f=25Hz, a)` / "
           "`Src (121.5, 68.0)` / `(Avg 1.68 dB)`）。两处的 regex 不能混用。")

    rec = {no: recompute(paths.npz_path(no)) for no, _, _, _, _, _, _ in SUBS}
    for no, ds, _, _, pdf, _, _ in SUBS:
        c.check(rec[no]["n"] == 8, f"Case {no} {ds} npz 样本数 = 8",
                f"4 频率 x 2 样本，实得 {rec[no]['n']}")
        c.check(os.path.exists(os.path.join(paths.FIGDIR, pdf)),
                f"{pdf} 存在", pdf)

    # ── B ────────────────────────────────────────────────────────
    c.section("3. epoch 双侧判据与 caption 声明")
    c.note("图取 ep200(last)，兄弟表 Table 13 取 best epoch，本是两套口径。"
           "故除『caption 含 last』外，还须断言『caption 未误写 best』。")
    cap = flat(T.caption_of(LABEL))
    c.check("Fields are from the last epoch" in cap,
            "caption 声明 last epoch", "")
    c.check("best epoch" not in cap, "caption 未误写 best epoch", "")
    for no, ds, _, _, _, _, _ in SUBS:
        eps = {int(__import__("numpy").load(paths.npz_path(no))["epoch"])}
        c.check(eps == {200}, f"Case {no} {ds} npz epoch == 200 (last)",
                f"实得 {sorted(eps)}")
        be = M.xlsx_case(paths.xlsx_path("4.7"), no)["best_epoch"]
        c.check(be is not None, f"Case {no} best epoch 可读",
                f"best={be}, last=200, "
                + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── C ────────────────────────────────────────────────────────
    c.section("4. ★ 展示样本必须全部落在外推区内")
    c.note("caption 称『on the held-out region』。若有任一展示样本的源坐标"
           "落在训练区内，整张图的论点（外推能力）就不成立——这是本组独有的"
           "约束，前面各组都没有。逐样本核 8 个源坐标的区域归属。")
    tbl = T.table_body_of(SIB)[0] or ""
    rows = [r for r in T.data_rows(tbl, ncol=13) if r and r[0].isdigit()]
    c.check(len(rows) == 4, f"Table 13 解析到 4 行（R9/R10/W9/W10）",
            f"实得 {len(rows)}")
    for no, ds, _, _, _, kind, thr in SUBS:
        bad = []
        for s in rec[no]["samples"]:
            x, y = s["src"]
            inside = (y > thr) if kind == "depth" else (x > thr)
            if not inside:
                bad.append(f"({x:.1f},{y:.1f})")
        c.check(not bad,
                f"Case {no} {ds} 8 个样本全在外推区（{kind} > {thr} m）内",
                "全部合规" if not bad else "越界: " + ", ".join(bad))
        # 阈值须与 Table 13 的 Extrap. region 列同值
        r = next((r for r in rows if r[0] == str(no)), None)
        c.check(r is not None, f"Table 13 含 Case {no} 行", "")
        if r is not None:
            c.check(f"{thr}" in r[2], f"Table 13 的 {ds} 阈值与图一致（{thr} m）",
                    f"表列 `{r[2]}` / 图 {kind} > {thr}")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    c.note("R9/R10 的 `Avg x.xx dB` 与频率/声源同排一行；重算给全精度，"
           "判定用舍入到 2 位的印刷值。")
    for no, ds, _, _, pdf, _, _ in SUBS:
        got = pdf_avgs(os.path.join(paths.FIGDIR, pdf))
        want = [f"{s['avg_err']:.2f}" for s in rec[no]["samples"]]
        c.check(got == want, f"Case {no} {ds} 8 个 Avg 逐一吻合",
                "全部吻合" if got == want else f"PDF {got} / npz 重算 {want}")
        c.check(len(got) == 8, f"Case {no} {ds} 图上解析到 8 个 Avg 标注",
                f"实得 {len(got)}")
        txt = pdftext(os.path.join(paths.FIGDIR, pdf))
        got_src = re.findall(r"Src \(([0-9.]+), ([0-9.]+)\)", txt)
        want_src = [("%.1f" % s["src"][0], "%.1f" % s["src"][1])
                    for s in rec[no]["samples"]]
        c.check(got_src == want_src, f"Case {no} {ds} 8 个 Src 坐标吻合",
                f"PDF {got_src} / npz {want_src}")
        got_f = re.findall(r"f = (\d+) Hz \(([ab])\)", txt)
        c.check([f for f, _ in got_f] == ["25", "25", "50", "50", "75", "75",
                                          "100", "100"],
                f"Case {no} {ds} 8 行频率序 = 每频率 2 样本",
                f"图上 `{got_f}`")
        c.check([t for _, t in got_f] == ["a", "b"] * 4,
                f"Case {no} {ds} 行标签的样本字母为 a/b 交替",
                "每频率两个样本标 (a)/(b)")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 子图 label 与数据集名 / 外推类型 / 阈值对应")
    aux = T.labels()
    txt = T.tex_text()
    for no, ds, sub_lb, letter, _, kind, thr in SUBS:
        n_sub = aux.get(sub_lb, {}).get("num", "缺失")
        c.check(n_sub.startswith(str(NUMBER)),
                f"子图 `{sub_lb}` 编号前缀为 {NUMBER}", f"aux `{n_sub}`")
        c.check(n_sub.endswith(letter),
                f"子图 `{sub_lb}` 是 Fig. {NUMBER}{letter}", f"aux `{n_sub}`")
        i = txt.find(chr(92) + "label{" + sub_lb + "}")
        b = txt.rfind(chr(92) + "subfloat[", 0, i)
        e = txt.find("]", b)
        title = flat(txt[b + len(chr(92) + "subfloat["):e]) if b >= 0 else ""
        c.check(ds in title, f"子图 `{sub_lb}` 题注含数据集名 {ds}",
                f"题注 `{title}`")
        # tex 题注对深度外推用 "deep"（非 "depth"），Table 13 的 Extrap.
        # region 列用 "depth"。两者指同一划分，措辞按各自惯例。
        kw = "deep" if kind == "depth" else "range"
        c.check(kw in title, f"子图 `{sub_lb}` 题注标明 {kw} extrapolation",
                f"题注 `{title}`；tex 用 `{kw}`，Table 13 同一划分记作 `{kind}`")
        c.check(str(thr) in title, f"子图 `{sub_lb}` 题注标明阈值 {thr} m",
                f"题注 `{title}`")

    # ── E2 ───────────────────────────────────────────────────────
    c.section("7. caption 的取样措辞与实际机制相符")
    c.note("本组按索引顺序取每频率前 2 个样本（非择优），故 caption 应写 "
           "the first two，不应含混称 representative。")
    c.check("first two" in cap, "caption 写明取每频率前两个样本",
            "含 `the first two held-out samples`")
    c.check("representative" not in cap, "caption 未含混使用 representative", "")
    c.check("labelled a/b" in cap, "caption 说明行以 a/b 标样本", "")
    c.check("rectangular" in cap.lower(), "caption 声明矩形几何", "")

    # ── E3 ───────────────────────────────────────────────────────
    c.section("8. R1 版式变动：楔形两幅已移入补充材料")
    c.note("★ R1 把 W9/W10 两幅（旧 fig:gen-grid-wedge = Fig 22）移入补充材料，"
           "正文以 `Fig.~S5` 引用。故 main text 只剩矩形一张；相关核验项"
           "（旧 Fig 22 编号、gen-w9/gen-w10 子图号、wedge caption 的 last "
           "epoch）在 R1 已无对象，逐条豁免如下。W9/W10 的 PDF 与其脚本仍在"
           "仓库内，供补充材料核对。")
    for lb in ("fig:gen-grid-wedge", "fig:gen-w9", "fig:gen-w10"):
        c.check(aux.get(lb) is None, f"`{lb}` 已不在正文（aux 无登记）",
                "R1 移入补充材料")
    c.exempt("旧 Fig 22（fig:gen-grid-wedge）编号 == 22",
             "该浮动体在 R1 已整段注释移入补充材料，aux 无登记")
    c.exempt("子图 fig:gen-w9 / fig:gen-w10 编号为 22a/22b",
             "两幅随楔形图移入补充材料，main text 不再引用其 label")
    c.check(chr(92) + "label{fig:gen-grid-wedge}" in txt,
            "移入补充材料的楔形浮动体以注释形式留在 tex 末尾（可回溯）",
            "tex 内含注释掉的 \\label{fig:gen-grid-wedge}")
    for no, ds, pdf in SUBS_SUPP:
        c.check(os.path.exists(os.path.join(paths.FIGDIR, pdf)),
                f"补充材料图件 {pdf} 仍在 Figures/results/", ds)

    # ── F ────────────────────────────────────────────────────────
    c.section("9. 正文引用")
    c.note("正文 4.7 节以 `Fig.~\\ref{fig:gen-grid} and Fig.~S5` 并列引用矩形"
           "（正文）与楔形（补充）两张图，非区间引用，且第二张已改为硬写的 "
           "`Fig.~S5`（补充材料图号）。")
    c.check(chr(92) + "ref{" + LABEL + "}" in txt,
            "正文引用 Fig. 12", "")
    c.check("Fig.~S5" in txt, "正文以 `Fig.~S5` 引用移入补充材料的楔形图", "")
    pair = chr(92) + "ref{" + LABEL + "} and Fig.~S5"
    c.check(pair in txt, "正文以 `Fig.~\\ref{fig:gen-grid} and Fig.~S5` 并列引用",
            f"含 `{pair}`")
    c.exempt("正文并列引用 Fig 21 与 Fig 22（`\\ref{{fig:gen-grid}} and "
             "\\ref{{fig:gen-grid-wedge}}`）",
             "R1 的楔形图已移入补充材料，正文改写为 `Fig.~S5` 硬引用，"
             "不再有 fig:gen-grid-wedge 的 \\ref")
    hits = T.sentences_with(r"held-out extrapolation region", txt)
    c.check(bool(hits), "正文描述该组图的内容",
            f"tex 行 {T.line_of(hits[0][0], txt)}" if hits else "未找到")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
