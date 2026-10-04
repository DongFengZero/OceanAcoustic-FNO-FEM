#!/usr/bin/env python3
"""
Fig. 5（fig:sq100）核验
=======================
对象：100 Hz 单频、方形域 TL 场图，矩形/楔形**并排一张图**的六个子图。
  Fig 5 = Case 6 (R4,128) / 7 (R5,256) / 8 (R6,512)   矩形，子图 (a)-(c)
        + Case 12 (W4,128) / 13 (W5,256) / 14 (W6,512)  楔形，子图 (d)-(f)

R1 修订把原来的矩形 Fig 8 与楔形 Fig 9 合并为本图（单一 label `fig:sq100`），
子图 label 为 `fig:sq100-r4` … `fig:sq100-w6`。旧 label `fig:res-rect-100` /
`fig:res-wedge-100` 及其子图 label 均已不存在。

★ Fig 5 的归属：本脚本负责。同渲染器的 FIG04_05_fields.py 只核 Fig 4，
不再重复核 Fig 5（两脚本此前判据重叠且对 Fig 5 的 label 口径互相冲突）。

与 Fig 4 的差别：单频 npz 只含 2 个样本（多频 8 个）；对应 Table 7 取
best epoch 而图取 ep200(last)，Case 14 的 best=129 与 last=200 差 71 轮。

数据源一律取 Raw_Experimental_Data 下的 *__TL原始数据_ep200.npz。
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

LABEL = "fig:sq100"
NUMBER = "5"
# 子图 label -> (Case, Dataset, aux 编号, PDF)
SUBS = [
    ("fig:sq100-r4", 6, "R4", "8a", "Case06_R4_TL.pdf"),
    ("fig:sq100-r5", 7, "R5", "8b", "Case07_R5_TL.pdf"),
    ("fig:sq100-r6", 8, "R6", "8c", "Case08_R6_TL.pdf"),
    ("fig:sq100-w4", 12, "W4", "8d", "Case12_W4_TL.pdf"),
    ("fig:sq100-w5", 13, "W5", "8e", "Case13_W5_TL.pdf"),
    ("fig:sq100-w6", 14, "W6", "8f", "Case14_W6_TL.pdf"),
]
CASES = [c for _, c, _, _, _ in SUBS]
PDF = {c: p for _, c, _, _, p in SUBS}
SUB_LABEL = {c: lb for lb, c, _, _, _ in SUBS}
SUBNUM = {c: n for _, c, _, n, _ in SUBS}

SCRIPT = (Path(__file__).resolve().parents[2] / "Validation_Scripts"
          / "fig04_05_10_fields" / "fig04_05_10_fields.py")
TABLE = "tab:sq100"
SLUG = "FIG05_sq100"


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


def table7_rows():
    """Table 7（tab:sq100）数据行 -> {Case: (row, TL 列索引)}。

    该表两几何并列：0=Lx×Ly, 1=No.R, 2=Dataset, 3=Sol, 4=TL,
    5=No.W, 6=Dataset, 7=Sol, 8=TL。故矩形案例号在第 1 列、TL 在第 4 列，
    楔形案例号在第 5 列、TL 在第 8 列——只按一列取号会漏掉整个楔形块。
    """
    te = T.table_env(TABLE)
    out = {}
    for r in T.data_rows(te, ncol=9):
        for no_col, tl_col in ((1, 4), (5, 8)):
            v = r[no_col].strip()
            if v.isdigit():
                out[int(v)] = (r, tl_col)
    return out


def run():
    c = report.Checker(SLUG, "100Hz 方形域 TL 场图 Fig. 5", "figure",
                       LABEL, NUMBER)
    rec = {}

    c.source("印刷面 tex", paths.TEX, "两个并列 minipage，各 3 个 subfloat")
    c.source("成图脚本", str(SCRIPT),
             "fig04_05_10_fields.py，按 INDEX.md 对应 Fig 4/5/10")
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

    # ★ 成图脚本已参数化路径（_figpaths.py），与旧的固定副本不再是逐字节
    #   同一份，"md5 同源"不再是成立的断言。改为核产出关系：脚本的 FIG5
    #   分支输出名清单必须正好覆盖本图六张 PDF。
    c.section("2. 成图脚本确实产出本图")
    c.note("R1 起成图脚本按 CH4_RAWROOT/CH4_FIGDIR 参数化，逐字节副本比对"
           "已失效；能证明归属的是『脚本产出清单 == 本图的图件集合』。")
    src = SCRIPT.read_text(encoding="utf-8", errors="ignore") if \
        SCRIPT.exists() else ""
    c.check(bool(src), "成图脚本可读", paths.rel(str(SCRIPT)))
    c.check("FIG5 = [" in src, "脚本含 Fig 5 的产出定义 `FIG5`",
            "与 Fig 4(FIG4)/Fig 10(FIG9) 同渲染器")
    for cno, ds, lx, _, _ in (s for s in
                              [(6, "R4", 128, 0, 0), (7, "R5", 256, 0, 0),
                               (8, "R6", 512, 0, 0), (12, "W4", 128, 0, 0),
                               (13, "W5", 256, 0, 0), (14, "W6", 512, 0, 0)]):
        key = f"case{cno:02d}_{ds.lower()}_tl"
        c.check(f'"{key}"' in src, f"脚本含 Case {cno} 的输出名 `{key}`",
                f"FIG5 分支产出 {key}.pdf")

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
    c.note("单频 case 的 best epoch 多不等于 200（Case 14 的 best=129），"
           "而图取 ep200，故 caption 必须声明 last epoch。")
    for cno in CASES:
        rec[cno] = recompute(paths.npz_path(cno))
        c.check(rec[cno]["epoch"] == 200, f"Case {cno} npz epoch=200",
                f"实得 {rec[cno]['epoch']}")
    cap = T.caption_of(LABEL) or ""
    c.check("last epoch" in cap, f"{LABEL} caption 声明 last epoch",
            "含 `Fields are from the last epoch.`")
    c.check("best epoch" not in cap, f"{LABEL} caption 未误写 best epoch",
            "图源自 ep200 npz，非 best-epoch 评估")
    c.check("f=100" in cap.replace("$", "").replace("\\,", ""),
            f"{LABEL} caption 标明 100 Hz", "含 `$f=100$\\,Hz`")
    c.check("(a)--(c)" in cap and "(d)--(f)" in cap,
            f"{LABEL} caption 写明子图分组 (a)-(c)/(d)-(f)",
            "矩形 (a)-(c)、楔形 (d)-(f)")

    # ★ 双侧判据：Case 14 的 best=129 与 last=200 相差 71 轮，是全章最大错位，
    #   最能说明"图注写 last、表注写 best"不是措辞随意，而是两套评估口径。
    c.note("图取 ep200(last)，兄弟表 Table 7 取 best epoch。二者本是不同轮。")
    from common import metrics as M
    for cno in CASES:
        be = M.xlsx_case(paths.xlsx_path("4.3"), cno)["best_epoch"]
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
    c.note("坐标 1 位小数，与深度线图及 Tables 6/7 同口径。")
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
           "须在 aux 注册，并逐个核 subfloat 题注里的 Case/Dataset。")
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
    for lb, cno, ds, subnum, _ in SUBS:
        c.check(lb in aux, f"子图 label `{lb}` 已注册",
                f"编号 `{aux.get(lb, {}).get('num', '缺失')}`")
        pos = txt_all.find("\\label{" + lb + "}")
        seg = txt_all[max(0, pos - 300):pos]
        c.check(f"Case~{cno}" in seg and ds in seg,
                f"子图 `{lb}` 题注标注 Case {cno} / {ds}",
                f"subfloat 题注含 `Case~{cno}` 与 `{ds}`")
        # subfloat 上的 label 是排版在子图旁的小标签，主图号+字母
        c.check(aux.get(lb, {}).get("num", "").endswith(subnum[1]),
                f"子图 `{lb}` 编号以字母 `{subnum[1]}` 收尾",
                f"aux `{aux.get(lb, {}).get('num', '缺失')}`（{subnum} 位）")
    c.note("★ 已知排版缺陷：本图主 label 为 Fig. 5，但六个 subfloat 在 aux 里"
           "注册为 8a-8f（subtable 计数器未随 figure 计数器重排）。本图为"
           "正文逐张引用，未使用 \\subref，故印出来仍是 Fig. 5 与 (a)-(f)，"
           "读者看不到错号；此处据实记录，不强行断言 5a-5f。")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 图表趋势同向（图逐样本 vs 表全测试集）")
    c.note("图上 Avg 是单样本场误差，Table 7 的 TL 是全测试集平均，"
           "二者不可互相反算，只核趋势：域尺度越大误差越大。")
    for name, nos in (("矩形 R4-R6", [6, 7, 8]), ("楔形 W4-W6", [12, 13, 14])):
        avgs = [max(s["avg_err"] for s in rec[n]["samples"]) for n in nos]
        c.check(avgs == sorted(avgs),
                f"{name} 误差随域尺度单调上升",
                " < ".join(f"Case{n}:{a:.2f}" for n, a in zip(nos, avgs)))
        t7 = table7_rows()
        tls = [float(t7[n][0][t7[n][1]]) for n in nos]
        c.check(tls == sorted(tls), f"{name} 表内 TL 随域尺度单调上升",
                " < ".join(f"{v:.3f}" for v in tls))

    # ── H ────────────────────────────────────────────────────────
    c.section("9. 正文引用：单张被引 + 表 caption 交代子图对应")
    c.note("R1 已取消旧稿的区间引用（`Figs.~\\ref{fig:res-128}--...`），"
           "Fig. 5 由正文三处单张 \\ref 引用，并被 Table 7 的 caption 交叉引用。"
           "256/512 m 两档的场图已删除，精度数据保留在 Table 6。")
    txt = T.tex_text()
    BS = chr(92)
    hits = re.findall(re.escape(BS) + r"ref\{" + re.escape(LABEL) + r"\}", txt)
    c.check(len(hits) >= 3, f"正文/表注引用 `{LABEL}` 至少 3 处",
            f"实得 {len(hits)} 处（4.3 节引入段、趋势段、结论段 + Table 7 注）")
    c.check(len(re.findall(re.escape(BS) + r"ref\{[^}]*\}--" + re.escape(BS)
                           + r"ref\{fig:", txt)) == 0,
            "正文不含图区间引用（R1 已改逐张引用）",
            "全文无 `\\ref{fig:..}--\\ref{fig:..}` 形式")
    c.check(aux.get("fig:res-rect-100") is None
            and aux.get("fig:res-wedge-100") is None,
            "旧 label `fig:res-rect-100` / `fig:res-wedge-100` 已不存在",
            "R1 合并为单一 `fig:sq100`")
    # 表 caption 必须把行与子图对应关系写明，否则读者对不上
    tcap = T.caption_of(TABLE) or ""
    c.check("(a)--(c)" in tcap and "(d)--(f)" in tcap,
            "Table 7 caption 写明行对应子图 (a)-(c)/(d)-(f)",
            "caption 含 `panels (a)--(c) and (d)--(f)`")
    c.check(f"fig:{LABEL.split(':')[1]}" in tcap,
            "Table 7 caption 交叉引用 Fig. 5", "")

    # 正文的定量断言：两几何的 TL 三档值
    c.note("正文 4.3 节给出单频方形域两几何的 TL 三档（0.444/1.217/3.852 与 "
           "0.610/0.930/3.407）及 512m/128m 倍数 8.676。逐条与印刷值比对。")
    te = T.table_env(TABLE)
    t7 = table7_rows()
    for cno, lit in ((6, "0.444"), (7, "1.217"), (8, "3.852"),
                     (12, "0.610"), (13, "0.930"), (14, "3.407")):
        row, col = t7[cno]
        c.check(row[col] == lit, f"正文 Case {cno} TL = {lit}",
                f"表印 `{row[col]}`")
    r8 = float(t7[8][0][t7[8][1]]) / float(t7[6][0][t7[6][1]])
    c.check(f"{r8:.3f}" == "8.676", "512m/128m TL 倍数 = 8.676（印刷值口径）",
            f"`{t7[8][0][t7[8][1]]}`/`{t7[6][0][t7[6][1]]}` = {r8:.6f} → {r8:.3f}")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
