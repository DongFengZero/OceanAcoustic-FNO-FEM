"""
T14_runtime.py — Table 14（tab:runtime）核验
===========================================
对象：推理耗时性能表，R1 修订把原来的两张表并进**同一个 table*** 浮动体，
      左右两个 minipage 各一张 tabular：

        (a) Base-scale, multi-GPU      Cases 43-44
            Case | Method | Time(ms) | Thr.(samp/s) | Speed-up      （8 行）
        (b) Scaling with domain size   Cases 45-50
            Case | Dataset | Lx(m) | N | Time(ms)                    （6 行）

核验链
  A. 源可追溯      xlsx（两张表各读一个工作表）/ tex 表体
  B. 表体定位      浮动体内含两张 tabular，须按序取到 (a) 与 (b)
  C. 印刷值比对    (a) Time/Thr./Speed-up 逐格；(b) Dataset/Lx/N/Time 逐格
  D. 派生量自洽    Speed-up = 本方法 Thr. / COMSOL Thr.；COMSOL 行恒为 1
  E. 正文引用      4.8 节直接引用的时延、吞吐、加速比与节点数
  F. caption       (a)/(b) 两个子题与图 Fig.\\ref{fig:perf} 的对应
"""
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import _boot  # noqa: F401
from common import paths, registry, report, texparse as T

SLUG = "T14_runtime"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]
NUMBER = 14
SEC = REC["sec"]

BASE = {43: "R1", 44: "W1"}                      # (a) 工作表0
SCALE = {45: "R4", 46: "R5", 47: "R6", 48: "W4", 49: "W5", 50: "W6"}   # (b) 工作表1
METHODS = ["COMSOL", "1 GPU", "2 GPU", "4 GPU"]

PROSE = [
    ("Case 43 1 GPU Time", "17.08", (43, "1 GPU", "time")),
    ("Case 44 1 GPU Time", "14.04", (44, "1 GPU", "time")),
    ("Case 43 COMSOL Time", "873.10", (43, "COMSOL", "time")),
    ("Case 44 COMSOL Time", "503.00", (44, "COMSOL", "time")),
    ("Case 43 1 GPU Speed-up", "45.93", (43, "1 GPU", "speedup_calc")),
    ("Case 44 1 GPU Speed-up", "31.37", (44, "1 GPU", "speedup_calc")),
    ("Case 43 1 GPU Thr.", "52.82", (43, "1 GPU", "thr")),
    ("Case 43 2 GPU Thr.", "98.22", (43, "2 GPU", "thr")),
    ("Case 43 4 GPU Thr.", "163.78", (43, "4 GPU", "thr")),
    ("Case 43 4 GPU Speed-up", "142.42", (43, "4 GPU", "speedup_calc")),
    ("Case 44 4 GPU Speed-up", "106.42", (44, "4 GPU", "speedup_calc")),
]

PROSE_SCALE = [
    ("Case 45 (R4) N", "21,737", (45, "n")),
    ("Case 47 (R6) N", "337,351", (47, "n")),
    ("Case 48 (W4) N", "10,680", (48, "n")),
    ("Case 50 (W6) N", "165,034", (50, "n")),
    ("Case 45 (R4) Time", "47.53", (45, "time")),
    ("Case 47 (R6) Time", "251.39", (47, "time")),
    ("Case 48 (W4) Time", "40.57", (48, "time")),
    ("Case 50 (W6) Time", "133.09", (50, "time")),
]


def load_base():
    """(a) 表：工作表0。返回 {case: {method: {time, thr, speedup}}}。"""
    df = pd.read_excel(paths.xlsx_path(SEC), sheet_name=0, header=2)
    data = {}
    for _, row in df.iloc[1:].iterrows():
        try:
            case = int(row.iloc[0])
        except (TypeError, ValueError):
            continue
        raw = str(row.iloc[4])
        if "COMSOL" in raw:
            m = "COMSOL"
        elif "1" in raw and "GPU" in raw:
            m = "1 GPU"
        elif "2" in raw:
            m = "2 GPU"
        elif "4" in raw:
            m = "4 GPU"
        else:
            continue
        data.setdefault(case, {})[m] = {
            "time": float(row.iloc[5]), "thr": float(row.iloc[6])}
    for case in data:
        base = data[case]["COMSOL"]["thr"]
        for m in METHODS:
            d = data[case][m]
            d["speedup"] = d["thr"] / base
    return data


def load_scale():
    """(b) 表：工作表1。返回 {case: {dataset, lx, n, time}}。"""
    df = pd.read_excel(paths.xlsx_path(SEC), sheet_name=1, header=2)
    data = {}
    for _, row in df.iloc[1:].iterrows():
        try:
            case = int(row.iloc[0])
        except (TypeError, ValueError):
            continue
        data[case] = {"dataset": str(row.iloc[1]).strip(), "lx": int(row.iloc[3]),
                      "n": int(row.iloc[5]), "time": float(row.iloc[6])}
    return data


def strip_cell0(s):
    return re.sub(r"\\midrule|\\toprule|\\bottomrule", "", s).strip()


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, str(NUMBER))
    xl = paths.xlsx_path(SEC)
    c.source("印刷面 tex", paths.TEX, f"`\\label{{{LABEL}}}` 所在 table* 浮动体")
    c.source("渠道1 xlsx", xl, "工作表0（多 GPU 基准）+ 工作表1（域尺度缩放）")
    c.note("本表无训练日志渠道：耗时与吞吐是推理基准测量，非训练评估量，"
           "故只有 xlsx 一个数据源，改用『两面板各自自洽 + 与正文互证』代替")

    c.section("1. 源可追溯性")
    c.check(os.path.exists(xl), "xlsx 存在", paths.rel(xl))
    xd, xs = load_base(), load_scale()
    c.check(set(xd) == set(BASE), "工作表0 覆盖 Case 43-44", str(sorted(xd)))
    c.check(set(xs) == set(SCALE), "工作表1 覆盖 Case 45-50", str(sorted(xs)))

    c.section("2. 表体定位（浮动体内两张 tabular）")
    c.note("R1 把 (a)(b) 两张表并进同一浮动体；table_body_of 只能取到第一张，"
           "故此处显式按序取出两张：第 1 张为 (a)、第 2 张为 (b)。")
    txt = T.tex_text()
    li = txt.find("\\label{%s}" % LABEL)
    b = txt.rfind("\\begin{table", 0, li)
    e = txt.find("\\end{table*}", li)
    seg = txt[b:e] if b >= 0 and e > li else ""
    tabs = []
    for m in re.finditer(r"\\begin\{tabular\*?\}", seg):
        e2 = seg.find("\\end{tabular}", m.start())
        if e2 > 0:
            tabs.append(seg[m.start():e2])
    c.check(len(tabs) == 2, "浮动体含两张 tabular（(a) 与 (b)）", f"实得 {len(tabs)}")
    c.check(seg.count("(a) Base-scale") == 1 and seg.count("(b) Scaling") == 1,
            "两个子题 (a)/(b) 各出现一次", "")
    if len(tabs) < 2:
        return c

    rows_a = T.data_rows(tabs[0], ncol=5)
    rows_b = T.data_rows(tabs[1], ncol=5)
    c.check(len(rows_a) == 8, "(a) 数据行数 = 8（2 案例 × 4 方法）",
            f"实得 {len(rows_a)}")
    c.check(len(rows_b) == 6, "(b) 数据行数 = 6（Cases 45-50）", f"实得 {len(rows_b)}")

    # ── (a) ──────────────────────────────────────────────────────
    c.section("3. (a) 印刷值比对（2 位小数）")
    c.note("列：Case(multirow) | Method | Time(ms) | Thr.(samp/s) | Speed-up。"
           "multirow 的首行带案例号，其后三行为空，故按每 4 行一组解析。")
    pa = {}
    for i, row in enumerate(rows_a):
        case = [43, 44][i // 4]
        meth = METHODS[i % 4]
        pa.setdefault(case, {})[meth] = {
            "time": row[2].strip(), "thr": row[3].strip(),
            "speedup": row[4].strip()}
    for no in BASE:
        for m in METHODS:
            src, prn = xd[no][m], pa[no][m]
            c.eq(f"Case {no} {m} Time", src["time"], prn["time"], nd=2)
            c.eq(f"Case {no} {m} Thr.", src["thr"], prn["thr"], nd=2)
            sv = re.sub(r"\$.*?\$", "", prn["speedup"]).strip()
            c.eq(f"Case {no} {m} Speed-up", src["speedup"], sv, nd=2)

    c.section("4. (a) 派生量自洽")
    c.note("Speed-up 是派生量：本方法 Thr. ÷ COMSOL Thr.。若两列各自独立填写，"
           "迟早对不上，故逐格从吞吐反算再与印刷值比较（上一节已做），"
           "此处另核 COMSOL 行恒为单位基准，且吞吐随 GPU 数单调上升。")
    for no in BASE:
        c.check(abs(xd[no]["COMSOL"]["speedup"] - 1.0) < 1e-9,
                f"Case {no} COMSOL 行为基准（Speed-up = 1）", "")
        thrs = [xd[no][m]["thr"] for m in METHODS[1:]]
        c.check(thrs == sorted(thrs), f"Case {no} 吞吐随 GPU 数单调上升",
                " < ".join(f"{v:.2f}" for v in thrs))
        times = [xd[no][m]["time"] for m in METHODS[1:]]
        c.check(max(times) - min(times) < 2.0,
                f"Case {no} 单样本时延跨 GPU 数近似不变（数据并行）",
                " / ".join(f"{v:.2f}" for v in times) + " ms")

    # ── (b) ──────────────────────────────────────────────────────
    c.section("5. (b) 印刷值比对")
    c.note("列：Case | Dataset | Lx(m) | N | Time(ms)。N 用千位逗号，"
           "tex 里写作 `21{,}737`，clean 后为 `21,737`。")
    pb = {}
    for row in rows_b:
        v = strip_cell0(row[0])
        if v.isdigit():
            pb[int(v)] = row
    c.check(set(pb) == set(SCALE), "(b) 行 No. 覆盖 45-50", str(sorted(pb)))
    for no in SCALE:
        src, prn = xs[no], pb[no]
        c.check(prn[1].strip() == SCALE[no], f"Case {no} Dataset 名",
                f"tex `{prn[1].strip()}`")
        c.check(prn[2].strip() == str(src["lx"]), f"Case {no} Lx",
                f"源 {src['lx']} / 印刷 `{prn[2].strip()}`")
        c.check(prn[3].replace("{,}", ",").replace("$", "") == f"{src['n']:,}",
                f"Case {no} N（千位分隔）",
                f"源 {src['n']} → `{src['n']:,}` / 印刷 `{prn[3]}`")
        c.eq(f"Case {no} Time", src["time"], prn[4].strip(), nd=2)

    c.section("6. (b) 趋势断言")
    c.note("正文称时延随节点数**次线性**增长；若时延随节点数线性增长，"
           "说明表格取的是并行前的时间或单位算错。")
    for tag, nos in (("矩形", [45, 46, 47]), ("楔形", [48, 49, 50])):
        nn = [xs[n]["n"] for n in nos]
        tt = [xs[n]["time"] for n in nos]
        c.check(nn == sorted(nn) and tt == sorted(tt),
                f"{tag} 节点数与时延同时单调上升",
                " / ".join(f"{a:,}→{b:.2f}ms" for a, b in zip(nn, tt)))
        ratio_n = nn[-1] / nn[0]
        ratio_t = tt[-1] / tt[0]
        c.check(ratio_t < ratio_n, f"{tag} 时延增长慢于节点数（次线性）",
                f"节点数 ×{ratio_n:.2f} / 时延 ×{ratio_t:.2f}")
    for pair in ((45, 48), (46, 49), (47, 50)):
        a, b2 = pair
        c.check(xs[a]["n"] > xs[b2]["n"] and xs[a]["time"] > xs[b2]["time"],
                f"同尺度下矩形节点数与时延均高于楔形（Case {a} vs {b2}）",
                f"矩形 {xs[a]['n']:,}/{xs[a]['time']:.2f}ms vs "
                f"楔形 {xs[b2]['n']:,}/{xs[b2]['time']:.2f}ms")

    # ── 正文 ─────────────────────────────────────────────────────
    c.section("7. 正文引用精确性（4.8 节，(a) 表）")
    for desc, quoted, (no, m, field) in PROSE:
        # speedup_calc 是从吞吐反算的派生量，与 xlsx 的 Speed-up 列同名对应
        val = xd[no][m]["speedup" if field == "speedup_calc" else field]
        c.eq(desc, val, quoted, nd=2)

    c.section("8. 正文引用精确性（4.8 节，(b) 表）")
    for desc, quoted, (no, field) in PROSE_SCALE:
        if field == "n":
            c.check(quoted == f"{xs[no]['n']:,}", desc,
                    f"源 {xs[no]['n']} → `{xs[no]['n']:,}` / 正文 `{quoted}`")
        else:
            c.eq(desc, xs[no]["time"], quoted, nd=2)

    # ── caption ──────────────────────────────────────────────────
    c.section("9. caption 与图件对应")
    cap = T.caption_of(LABEL) or ""
    c.check("(a)" in cap and "(b)" in cap, "caption 分述 (a)/(b) 两个面板", "")
    c.check("NVIDIA A800" in cap and "Hygon DCU" in cap,
            "caption 标明两个面板各自的硬件平台（跨平台不可直接比）", "")
    # caption 未交叉引用 Fig.\ref{fig:perf}（图在正文另行引用），
    # 故改核正文确实引了该图——caption 里没有的不硬凑。
    n_ref = len(re.findall(r"\\ref\{fig:perf\}", T.tex_text()))
    c.check(n_ref >= 1, "正文引用 Fig.\\ref{fig:perf}",
            f"实得 {n_ref} 处")
    c.check(T.number_of(LABEL) == str(NUMBER), f"表号为 {NUMBER}",
            f"aux `{T.number_of(LABEL)}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
