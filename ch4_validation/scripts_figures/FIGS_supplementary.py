#!/usr/bin/env python3
"""
FIGS_supplementary.py — 补充材料 Figs. S1-S7 核验（跨文件）

R1 把 5 组场图（原 Fig. 6、7、16、17、22）移出正文，作为补充材料 Figs. S1-S7，
用正文同一套渲染器按印刷尺寸重绘（Validation_Scripts/figS_supplementary）。
本脚本核四件事：

  A. 图上数值 ↔ 原始 npz：每行的声源坐标与平均误差，用成图脚本自身的插值函数
     从 ep200 npz 现场重算，与 PDF 文本层逐字比对（与正文场图核验同口径）。
  B. 印刷尺寸：图宽不超过版心，最小字号 ≥ 6 pt（回复信 3.4 承诺的字号）。
  C. 正文 ↔ 补充材料：正文引用的 S 编号全部存在、每张 S 图都被引用，且出现在
     对应小节（S1-S4 在 4.3、S5-S6 在 4.5、S7 在 4.7）；补充材料里写出的正文
     图/表/节编号与正文 aux 一致。
  D. 回复信：附录 B 的 原图 → S 编号 映射与补充材料一览表一致。
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, report, texparse as T

SLUG = "FIGS_supplementary"
TEXDIR = os.path.dirname(paths.TEX)
SUPP = os.path.join(TEXDIR, "OE_supplementary.tex")
RTR = os.path.join(TEXDIR, "Response_to_Reviewers.tex")
FIGDIR = os.path.join(TEXDIR, "Figures", "supplementary")
GEN = os.path.join(paths.REPO, "Validation_Scripts", "figS_supplementary")
sys.path.insert(0, GEN)
sys.path.insert(0, os.path.join(paths.REPO, "Validation_Scripts"))

# S 编号 -> (图件, 类型, 算例/npz 前缀, 原图号, 正文小节 label, 精度所在表 label)
SFIG = {
    1: ("figS1_case04_r2.pdf", "field", ["Case04"], "6", "sec:forward", "tab:res-rect-mf"),
    2: ("figS2_case10_w2.pdf", "field", ["Case10"], "6", "sec:forward", "tab:res-rect-mf"),
    3: ("figS3_case05_r3.pdf", "field", ["Case05"], "7", "sec:forward", "tab:res-rect-mf"),
    4: ("figS4_case11_w3.pdf", "field", ["Case11"], "7", "sec:forward", "tab:res-rect-mf"),
    5: ("figS5_abl_r1.pdf", "grid", ["Case25_R1_Full", "Case26_R1_no_prior",
                                     "Case27_R1_no_graph", "Case28_R1_no_prior_loss"],
        "16", "sec:ablation", "tab:abl"),
    6: ("figS6_abl_w1.pdf", "grid", ["Case29_W1_Full", "Case30_W1_no_prior",
                                     "Case31_W1_no_graph", "Case32_W1_no_prior_loss"],
        "17", "sec:ablation", "tab:abl"),
    7: ("figS7a_gen_extrap_w9.pdf|figS7b_gen_extrap_w10.pdf", "field2", ["Case41", "Case42"],
        "22", "sec:generalization", "tab:gen-overall"),
}


def pdf_text(path):
    import fitz
    d = fitz.open(path)
    txt = re.sub(r"\s+", " ", "".join(p.get_text() for p in d))
    sizes = [s["size"] for p in d for b in p.get_text("dict")["blocks"]
             for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]
    return txt, d[0].rect.width, min(sizes) if sizes else None


def expand(spec):
    """'S1--S4' / 'S5 and~S6' / 'S7' -> {1,2,3,4} ..."""
    nums = set()
    for a, b in re.findall(r"S(\d)(?:--S(\d))?", spec):
        lo, hi = int(a), int(b or a)
        nums.update(range(lo, hi + 1))
    return nums


def run():
    c = report.Checker(SLUG, "补充材料 Figs. S1-S7（跨文件核验）", "figure",
                       "Figs. S1-S7", "S1-S7")
    c.source("补充材料 tex", SUPP, "图题与正文编号")
    c.source("正文 tex", paths.TEX, "S 引用")
    c.source("回复信 tex", RTR, "附录 B 映射")
    c.source("成图脚本", os.path.join(GEN, "figS_supplementary.py"), "渲染器复用正文 Fig. 4/8/12")

    supp = io.open(SUPP, encoding="utf8").read()
    main = T.tex_text()
    aux = T.labels()

    # ── A + B ───────────────────────────────────────────────────
    import figS_supplementary as G
    FF, PG = G.FF, G.PG
    import numpy as np
    c.section("1. 图上数值 ↔ npz（ep200，成图脚本同一插值）", ("检查项", "重算 / 图上", "结论"))
    c.note("场图：每行『Src (x, y)』与『Avg e dB』；网格图：每行『f Hz (x, y)』与各变体 |Err| 平均。"
           "取样与正文 Fig. 4/8 相同：每频率前两个留出样本。")
    for k, (files, kind, cases, *_rest) in SFIG.items():
        flist = files.split("|")
        texts = []
        for f in flist:
            p = os.path.join(FIGDIR, f)
            c.check(os.path.exists(p), f"S{k} 图件 `{f}` 存在", paths.rel(p))
            if not os.path.exists(p):
                continue
            txt, width, fmin = pdf_text(p)
            texts.append(txt)
            c.check(width <= 494.5 + 0.5, f"S{k} `{f}` 宽度不超过版心 494.5 pt",
                    f"{width:.1f} pt")
            c.check(fmin is not None and fmin >= 5.95, f"S{k} `{f}` 最小字号 ≥ 6 pt",
                    f"{fmin:.2f} pt")
        if kind in ("field", "field2"):
            for f_txt, case in zip(texts, cases):
                bad = []
                for data, idx, left in FF.rows_multi(case, tags=(kind == "field2")):
                    _, _, _, avg, _ = FF.fields(data, idx)
                    src = data["source_pos"][idx]
                    for lit in ("Src (%.1f, %.1f)" % (src[0], src[1]), "Avg %.2f dB" % avg):
                        if lit not in f_txt:
                            bad.append(lit)
                c.check(not bad, f"S{k} {case}：8 行声源与平均误差与重算一致",
                        "全部一致" if not bad else "缺: " + "; ".join(bad[:4]))
        else:
            datas = [np.load(PG.find_npz(cs), allow_pickle=True) for cs in cases]
            bad = []
            for f_hz, idx in PG.ROWS_2S:
                d0 = datas[0]
                src = d0["source_pos"][idx]
                lit = "%d Hz (%.1f, %.1f)" % (f_hz, src[0], src[1])
                if lit not in texts[0]:
                    bad.append(lit)
                gf = PG.interp(d0, "fem_tl", idx)
                for d in datas:
                    e = "%.2f dB" % float(np.nanmean(np.abs(PG.interp(d, "pred_tl", idx) - gf)))
                    if e not in texts[0]:
                        bad.append(e)
            c.check(not bad, f"S{k} 消融网格：8 行声源与 32 个平均误差与重算一致",
                    "全部一致" if not bad else "缺: " + "; ".join(bad[:4]))

    # ── C ──────────────────────────────────────────────────────
    c.section("2. 正文 ↔ 补充材料")
    refs = re.findall(r"Figs?\.~(S\d(?:--S\d)?(?: and~S\d)?)", main)
    cited = set().union(*[expand(r) for r in refs]) if refs else set()
    c.check(cited == set(SFIG), "正文引用的 S 编号恰为 S1-S7（无遗漏、无越界）",
            f"引用 {sorted(cited)}")
    n_caps = len(re.findall(r"\\begin\{figure\}", supp))
    c.check(n_caps == len(SFIG), "补充材料恰有 7 个 figure 环境", f"{n_caps}")
    # 每个 S 引用出现在对应小节内
    secs = [(m.start(), m.group(1)) for m in re.finditer(r"\\label\{(sec:[^}]*)\}", main)]
    def section_at(pos):
        cur = None
        for p0, lab in secs:
            if p0 <= pos:
                cur = lab
        return cur
    for k, (_, _, _, _, sec, _) in SFIG.items():
        hits = [m.start() for m in re.finditer(r"Figs?\.~(S\d(?:--S\d)?(?: and~S\d)?)", main)
                if k in expand(m.group(1)) and "S1--S7" not in m.group(1)]
        where = sorted({section_at(h) for h in hits})
        c.check(sec in where, f"S{k} 在 {sec}（{aux.get(sec, {}).get('num', '?')} 节）被引用",
                f"实际出现于 {where}")
    # 补充材料里写出的正文编号
    expect = {"Fig.~4": "fig:res-128", "Table~6": "tab:res-rect-mf", "Fig.~8": "fig:perf-cmp-r",
              "Table~11": "tab:abl", "Fig.~12": "fig:gen-grid", "Table~13": "tab:gen-overall"}
    for lit, lab in expect.items():
        num = aux.get(lab, {}).get("num")
        c.check(lit in supp and lit.split("~")[1] == num,
                f"补充材料写 `{lit}` ↔ 正文 `{lab}` = {num}", "")
    for lab in ("sec:forward", "sec:ablation", "sec:generalization"):
        num = aux.get(lab, {}).get("num")
        c.check(f"Sec.~{num}" in supp, f"补充材料一览表含 `Sec.~{num}`（{lab}）", "")

    # ── D ──────────────────────────────────────────────────────
    c.section("3. 回复信附录 B ↔ 补充材料")
    rtr = io.open(RTR, encoding="utf8").read()
    for snums, orig in (("S1--S4", "6 + 7"), ("S5--S6", "16 + 17"), ("S7", "22")):
        ok = re.search(re.escape(snums) + r"\s*&\s*" + re.escape(orig) + r"\s*&", rtr) is not None
        c.check(ok, f"附录 B：原图 {orig} → {snums}", "")
        for k in expand(snums):
            # 读补充材料 tex 里一览表的实际行，取末列『Original figure』
            row = re.search(r"^S%d &(.*)\\\\" % k, supp, re.M)
            got = row.group(1).split("&")[-1].strip() if row else None
            ok = got is not None and re.sub(r"\(.\)$", "", got) in orig.split(" + ")
            c.check(ok, f"补充材料一览表 S{k} 原图号 `{got}` ∈ 附录 B 的 `{orig}`", "")
    c.check("Supplementary" not in rtr or "Figs.~S1--S7" in rtr,
            "回复信以 `Figs.~S1--S7` 指称补充材料", "")
    return c


if __name__ == "__main__":
    sys.exit(run().finish())
