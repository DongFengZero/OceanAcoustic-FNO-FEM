#!/usr/bin/env python3
"""
Fig. 10（fig:mesh）核验
=======================
对象：网格无关性 TL 场图，100 Hz，矩形/楔形**并排一张图**的六个子图。
  Fig 10 = Case 33 (R4, Δ=1.00) / 34 (R7, 0.50) / 35 (R8, 0.25)  矩形，(a)-(c)
         + Case 36 (W4, Δ=1.00) / 37 (W7, 0.50) / 38 (W8, 0.25)  楔形，(d)-(f)

R1 修订把原来的矩形/楔形两张图合并为本图（单一 label `fig:mesh`），子图
label 为 `fig:mesh-a` … `fig:mesh-f`。旧 label `fig:mesh-rect` /
`fig:mesh-wedge` 及其子图 label 均已不存在。

核验链
  A. 源可追溯      npz 存在；成图脚本产出清单覆盖本图六张 PDF
  B. 口径防漂移    method/grid_res 与重算层一致
  C. epoch 自证    npz['epoch']==200，caption 声明 last epoch
  D. 数值复现      逐样本 Avg 误差 vs PDF 文本层标注（★核心）
  E. Src 坐标      图上标注 vs npz source_pos
  F. 结构         单频 2 样本；六个 subfloat 在 aux 注册
  G. 网格无关性    ★论点与场图族相反：不要求单调，要求三档同量级
  H. 引用方式      caption 交叉引用；正文/表注引用本图
  I. 免责声明      caption 已声明"个别样本、非最优、不必吻合表均值"
  J. 数据集复用    Case 33≡6、36≡12 的 npz 逐字节相同
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

LABEL = "fig:mesh"
NUMBER = "10"
# 子图 label -> (Case, Dataset, Δ, PDF)
SUBS = [
    ("fig:mesh-a", 33, "R4", "1.00", "Case33_R4_TL.pdf"),
    ("fig:mesh-b", 34, "R7", "0.50", "Case34_R7_TL.pdf"),
    ("fig:mesh-c", 35, "R8", "0.25", "Case35_R8_TL.pdf"),
    ("fig:mesh-d", 36, "W4", "1.00", "Case36_W4_TL.pdf"),
    ("fig:mesh-e", 37, "W7", "0.50", "Case37_W7_TL.pdf"),
    ("fig:mesh-f", 38, "W8", "0.25", "Case38_W8_TL.pdf"),
]
CASES = [c for _, c, _, _, _ in SUBS]
PDF = {c: p for _, c, _, _, p in SUBS}
DELTA = {c: d for _, c, _, d, _ in SUBS}
# 数据集复用：Case 33 复用 Case 6 的 R4，Case 36 复用 Case 12 的 W4
REUSE = {33: 6, 36: 12}

SCRIPT = (Path(__file__).resolve().parents[2] / "Validation_Scripts"
          / "fig04_05_10_fields" / "fig04_05_10_fields.py")
TABLE = "tab:mesh"
SLUG = "FIG10_mesh"


def pdf_text(pdf_path):
    """PDF 文本层。必须用 -raw：-layout 会把 Ours 面板的两行标题按列交错
    咬合成 'OSurrcs(T4L4(.5f=,2215.H9)z)'，正则一个都匹配不到。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=120)
        return out.stdout
    except Exception:
        return ""


def pdf_avgs(pdf_path):
    """`Avg x.xx dB` 标注。R1 紧凑排版已去冒号（旧稿为 `Avg:`）。"""
    return re.findall(r"Avg ([0-9.]+) dB", pdf_text(pdf_path))


def pdf_srcs(pdf_path):
    """`Src (x, y)` 坐标，同样无冒号（旧稿为 `Src:(x,y)`）。"""
    return re.findall(r"Src \(([0-9.]+), ([0-9.]+)\)", pdf_text(pdf_path))


def run():
    c = report.Checker(SLUG, "网格无关性 TL 场图 Fig. 10", "figure",
                       LABEL, NUMBER)

    c.source("印刷面 tex", paths.TEX, "两个并列 minipage，各 3 个 subfloat")
    c.source("成图脚本", str(SCRIPT),
             "fig04_05_10_fields.py，按 INDEX.md 对应 Fig 4/5/10")
    c.source("复用比对 npz (Case 6 / 12)", paths.npz_path(6),
             "4.3 节单频案例，用于确认 Case 33≡6、36≡12")
    for cno in CASES:
        c.source(f"数据源 npz (Case {cno})", paths.npz_path(cno),
                 "Raw_Experimental_Data，ep200（last epoch）")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯性")
    c.check(SCRIPT.exists(), "成图脚本存在", paths.rel(str(SCRIPT)))
    for cno in CASES:
        p = paths.npz_path(cno)
        c.check(p and os.path.exists(p), f"Case {cno} npz 存在",
                paths.rel(p) if p else "未找到")
    for cno, pdf in PDF.items():
        fp = os.path.join(paths.FIGDIR, pdf)
        c.check(os.path.exists(fp), f"图件 {pdf} 存在", paths.rel(fp))

    # ★ 成图脚本已参数化路径，逐字节副本比对不再成立；改核产出关系。
    c.section("2. 成图脚本确实产出本图")
    c.note("R1 起成图脚本按 CH4_RAWROOT/CH4_FIGDIR 参数化，逐字节副本比对"
           "已失效；能证明归属的是『脚本产出清单 == 本图的图件集合』。")
    src = SCRIPT.read_text(encoding="utf-8", errors="ignore") if \
        SCRIPT.exists() else ""
    c.check(bool(src), "成图脚本可读", paths.rel(str(SCRIPT)))
    c.check("FIG9 = [" in src, "脚本含 Fig 10 的产出定义 `FIG9`",
            "与 Fig 4(FIG4)/Fig 5(FIG5) 同渲染器")
    for cno, ds, _, _ in [(33, "R4", 0, 0), (34, "R7", 0, 0), (35, "R8", 0, 0),
                          (36, "W4", 0, 0), (37, "W7", 0, 0), (38, "W8", 0, 0)]:
        key = f"case{cno:02d}_{ds.lower()}_tl"
        c.check(f'"{key}"' in src, f"脚本含 Case {cno} 的输出名 `{key}`",
                f"FIG9 分支产出 {key}.pdf")

    # ── B ────────────────────────────────────────────────────────
    c.section("3. 口径防漂移（脚本源码 vs 重算层）")
    c.note("重算层复刻脚本 fields() 的内层算法；脚本改了插值方式或网格分辨率"
           "而重算层没跟上，图与核验就会各算一套，此处当场报错。")
    m = re.search(r"def fields\(data, i, grid_res=(\d+), method=\"([a-z]+)\"\)",
                  src)
    c.check(m is not None, "可从源码解析 fields() 默认参数",
            f"grid_res={m.group(1)}, method={m.group(2)}" if m else "解析失败")
    if m:
        c.check(m.group(2) == METHOD, "插值方式一致",
                f"脚本 `{m.group(2)}` / 重算层 `{METHOD}`")
        c.check(int(m.group(1)) == GRID_RES, "网格分辨率一致",
                f"脚本 `{m.group(1)}` / 重算层 `{GRID_RES}`")
    c.check('"f = %d Hz,  Src (%.1f, %.1f)"' in src,
            "单频面板按 1 位小数印 Src（全章统一口径）",
            "源码含 rows_single() 的 `f = %d Hz,  Src (%.1f, %.1f)`")
    c.check('"Avg %.2f dB" % avg' in src, "脚本按 2 位小数印 Avg 标注",
            "源码含 `\"Avg %.2f dB\" % avg`")

    # ── C ────────────────────────────────────────────────────────
    c.section("4. epoch 自证与 caption 声明")
    c.note("图取 ep200（last epoch），兄弟表 Table 12 取 best epoch。")
    rec = {}
    for cno in CASES:
        rec[cno] = recompute(paths.npz_path(cno))
        c.check(rec[cno]["epoch"] == 200, f"Case {cno} npz epoch=200",
                f"实得 {rec[cno]['epoch']}")
    cap = T.caption_of(LABEL) or ""
    c.check("last epoch" in cap, f"{LABEL} caption 声明 last epoch",
            "含 `from the last epoch`")
    c.check("best epoch" not in cap, f"{LABEL} caption 未误写 best epoch",
            "图源自 ep200 npz，非 best-epoch 评估")
    c.check("f=100" in cap.replace("$", "").replace("\\,", ""),
            f"{LABEL} caption 标明 100 Hz", "含 `$f=100$\\,Hz`")
    c.check("(a)--(c)" in cap and "(d)--(f)" in cap,
            f"{LABEL} caption 写明子图分组 (a)-(c)/(d)-(f)",
            "矩形 (a)-(c)、楔形 (d)-(f)")
    from common import metrics as M
    for cno in CASES:
        be = M.xlsx_case(paths.xlsx_path("4.6"), cno)["best_epoch"]
        c.check(be is not None, f"Case {cno} best epoch 可读",
                f"best={be}, last=200, "
                + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── D ────────────────────────────────────────────────────────
    c.section("5. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    c.note("图上每个 Error 面板标 `Avg x.xx dB`。从 Raw_Experimental_Data 的 "
           "npz 复刻算法重算，与 PDF 文本层标注逐个按 2 位小数比对——"
           "这是图件产自这批 npz 的直接证据。")
    for cno in CASES:
        got = pdf_avgs(os.path.join(paths.FIGDIR, PDF[cno]))
        want = [f"{s['avg_err']:.2f}" for s in rec[cno]["samples"]]
        c.check(len(got) == len(want), f"Case {cno} 图内 Avg 标注数量",
                f"PDF {len(got)} 个 / 重算 {len(want)} 个")
        c.check(got == want, f"Case {cno} 2 个 Avg 逐一吻合",
                f"PDF {got} / npz 重算 {want}")

    # ── E ────────────────────────────────────────────────────────
    c.section("6. Src 坐标：npz 重算 vs 图上标注")
    c.note("坐标 1 位小数，与深度线图及 Tables 6/7/12 同口径。")
    for cno in CASES:
        got = pdf_srcs(os.path.join(paths.FIGDIR, PDF[cno]))
        want = [(f"{s['src'][0]:.1f}", f"{s['src'][1]:.1f}")
                for s in rec[cno]["samples"]]
        c.check([tuple(g) for g in got] == want, f"Case {cno} 2 组 Src 坐标吻合",
                f"PDF {got} / npz {want}")
        bad = [g for g in got if not (re.fullmatch(r"\d+\.\d", g[0])
                                      and re.fullmatch(r"\d+\.\d", g[1]))]
        c.check(not bad, f"Case {cno} Src 均为 1 位小数",
                "全部合规" if not bad else str(bad))

    # ── F ────────────────────────────────────────────────────────
    c.section("7. 图结构与子图引用")
    c.note("单频 npz 只含 2 个样本，故每子图 2 行；六个 subfloat 的 label "
           "须在 aux 注册，并逐个核 subfloat 题注里的 Case/Dataset/Δ。")
    aux = T.labels()
    for cno in CASES:
        r = rec[cno]
        c.check(r["n"] == 2, f"Case {cno} npz 样本数 = 2",
                f"单频 case，实得 {r['n']}")
        c.check(all(int(s["freq"]) == 100 for s in r["samples"]),
                f"Case {cno} 全部样本为 100 Hz",
                str(sorted(set(int(s['freq']) for s in r['samples']))))
    c.check(aux.get(LABEL, {}).get("num") == NUMBER,
            f"主图 label `{LABEL}` 注册且编号为 {NUMBER}",
            f"aux `{aux.get(LABEL, {}).get('num', '缺失')}`")
    txt_all = T.tex_text()
    for lb, cno, ds, delta, _ in SUBS:
        c.check(lb in aux, f"子图 label `{lb}` 已注册",
                f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")
        pos = txt_all.find("\\label{" + lb + "}")
        seg = txt_all[max(0, pos - 300):pos]
        c.check(f"Case~{cno}" in seg and ds in seg,
                f"子图 `{lb}` 题注标注 Case {cno} / {ds}",
                f"subfloat 题注含 `Case~{cno}` 与 `{ds}`")
        c.check(f"\\Delta={delta}" in seg,
                f"子图 `{lb}` 题注标注 Δ={delta} m",
                f"subfloat 题注含 `$\\Delta={delta}$\\,m`")
    c.note("★ 已知排版缺陷：本图主 label 为 Fig. 10，但六个 subfloat 在 aux 里"
           "注册为 13a-13f（subtable 计数器未随 figure 计数器重排）。本图未"
           "使用 \\subref，印出来仍是 Fig. 10 与 (a)-(f)，读者看不到错号；"
           "此处据实记录，不强行断言 10a-10f。")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 网格无关性：细化下误差保持同量级")
    c.note("★ 本组的论点是网格无关性，判据与场图族相反：不要求单调，而要求"
           "三种网格间距下误差**保持同一量级**（网格加密 4 倍、节点数增约 16 "
           "倍，若误差随之爆掉就说明模型依赖特定离散）。caption 已声明这是"
           "个别样本的 last-round 结果，故不与表的均值趋势强行对齐。")
    for name, nos in (("矩形 R4/R7/R8", [33, 34, 35]),
                      ("楔形 W4/W7/W8", [36, 37, 38])):
        avgs = [max(s["avg_err"] for s in rec[n]["samples"]) for n in nos]
        lo, hi = min(avgs), max(avgs)
        c.check(hi / lo < 3.0, f"{name} 三种 Δ 下图误差同量级（极差 < 3x）",
                " / ".join(f"Δ={DELTA[n]}m:{a:.2f}" for n, a in zip(nos, avgs))
                + f" → {hi / lo:.2f}x")
        c.check(hi < 1.0, f"{name} 三种 Δ 下图误差均 < 1 dB",
                f"最大 `{hi:.2f}` dB")

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 引用方式：正文/表注引用 + caption 交叉引用")
    c.note("★ R1 的 Table 12 已无 Fig. 列（合并后只有 Δ|No.R|Dataset|Sol|TL "
           "|No.W|Dataset|Sol|TL 九列），故旧稿的『逐行 Fig. 列指向子图』断言"
           "已不成立，改为核 caption 与正文的交叉引用。")
    txt = T.tex_text()
    BS = chr(92)
    hits = re.findall(re.escape(BS) + r"ref\{" + re.escape(LABEL) + r"\}", txt)
    c.check(len(hits) >= 2, f"正文/表注引用 `{LABEL}` 至少 2 处",
            f"实得 {len(hits)} 处（4.6 节正文 + Table 12 caption）")
    c.check(len(re.findall(re.escape(BS) + r"ref\{[^}]*\}--" + re.escape(BS)
                           + r"ref\{fig:", txt)) == 0,
            "正文不含图区间引用（R1 已改逐张引用）",
            "全文无 `\\ref{fig:..}--\\ref{fig:..}` 形式")
    c.check(aux.get("fig:mesh-rect") is None
            and aux.get("fig:mesh-wedge") is None,
            "旧 label `fig:mesh-rect` / `fig:mesh-wedge` 已不存在",
            "R1 合并为单一 `fig:mesh`")
    tcap = T.caption_of(TABLE) or ""
    c.check("(a)--(c)" in tcap and "(d)--(f)" in tcap,
            "Table 12 caption 写明行对应子图 (a)-(c)/(d)-(f)",
            "caption 含 `panels (a)--(c) and (d)--(f)`")
    c.check("ref{" + LABEL + "}" in tcap,
            "Table 12 caption 交叉引用 Fig. 10", "")
    # Table 12 的列数与本案一致，且确无 Fig. 列
    te = T.table_env(TABLE)
    rows = T.data_rows(te, ncol=9)
    c.check(len(rows) == 3, "Table 12 数据行 3 行（三档 Δ）", f"实得 {len(rows)}")
    c.check(all(len(r) == 9 for r in rows),
            "Table 12 每行 9 列（两几何并排，无 Fig. 列）",
            "Δ | No.R | Dataset | Sol | TL || No.W | Dataset | Sol | TL")

    # ── I ────────────────────────────────────────────────────────
    c.section("10. caption 已声明『个别样本、非最优』的免责说明")
    c.note("图上名次可能与表的均值趋势不同。R1 的 caption 写明了这点，"
           "此处固化为断言防止日后被删。★ 注意 R1 的措辞是 "
           "`not best-case results`，旧稿的 `rather than the best result` "
           "已不在文中。")
    for phrase in ("Individual sampled examples from the last epoch",
                   "not best-case results",
                   "need not follow the averaged trend of the table"):
        c.check(phrase in cap, f"caption 含 `{phrase}`",
                "已声明个别样本/非最优/不必吻合表均值")

    # ── J ────────────────────────────────────────────────────────
    c.section("11. 数据集复用（Table 3 的 Reuse 列）")
    c.note("Case 33 复用 Case 6 的 R4 数据集、Case 36 复用 Case 12 的 W4。"
           "两侧 npz 须逐字节相同，否则『复用』的说法不成立。")
    for a, b in REUSE.items():
        pa, pb = paths.npz_path(a), paths.npz_path(b)
        ha = hashlib.md5(Path(pa).read_bytes()).hexdigest()
        hb = hashlib.md5(Path(pb).read_bytes()).hexdigest()
        c.check(ha == hb, f"Case {a} 与 Case {b} 的 npz 逐字节相同",
                f"md5 `{ha[:12]}` vs `{hb[:12]}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
