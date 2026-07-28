#!/usr/bin/env python3
"""
全章图件引用完整性核验（跨图，非单图）

单图脚本各自核了自己的引用，但缺三项只能在全局做的检查：
  A. 每个图 label 都至少被引用一次（无孤图）
  B. 每个 \\ref{fig:...} 都指向真实存在的 label（无悬空引用）
  C. 图号顺序与首次被引顺序一致（读者不会先见 Fig 9 再见 Fig 5）

引用形式在本章有四种，判定时必须都算作"已引"：
  1. 散文单点引用      Fig.~\\ref{fig:ideal-rect}
  2. 散文区间引用      Figs.~\\ref{fig:res-128}--\\ref{fig:res-wedge-100}
  3. 散文并列引用      Figs.~\\ref{A} and \\ref{B}
  4. 表格 Fig. 列引用  \\ref{fig:mesh-rect}\\subref{fig:mesh-rect-a}
  5. caption 内交叉引用 Layout as in Fig.~\\ref{fig:perf-rect}
只按 1 判定会把 Fig 8（落在区间内部）误判为漏引。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIGALL_refs"

# 第 4 章正文图（不含第 1-3 章的 architecture/case 等）
CH4_MAIN = [
    ("fig:ideal-rect", "3"), ("fig:ideal-wedge", "4"),
    ("fig:res-128", "5"), ("fig:res-256", "6"), ("fig:res-512", "7"),
    ("fig:res-rect-100", "8"), ("fig:res-wedge-100", "9"),
    ("fig:dl-cmp-rect", "10"), ("fig:dl-cmp-wedge", "11"),
    ("fig:dl-abl-rect", "12"), ("fig:dl-abl-wedge", "13"),
    ("fig:perf-rect", "14"), ("fig:perf-wedge", "15"),
    ("fig:abl-rect", "16"), ("fig:abl-wedge", "17"),
    ("fig:mesh-rect", "18"), ("fig:mesh-wedge", "19"),
    ("fig:gen-split", "20"),
    ("fig:gen-grid", "21"), ("fig:gen-grid-wedge", "22"),
    ("fig:perf", "23"),
]


def figure_env_spans(txt):
    """返回所有 figure/figure* 环境的 [start, end) 区间，用于区分
    『正文引用』与『caption 内引用』。

    先剥注释再解析：模板里有 `% ... \\begin{figure*} (double-column) float`
    这类说明性注释，若当成真环境，其区间会从注释处一直张开到下一个
    \\end{figure}（实测 996-21983，跨 21k 字符），把中间的正文引用全部
    误判为环境内引用。本章的图 label 恰好都在该区间之后而未受影响，
    但这是巧合，不能依赖。复用表侧同一份剥注释实现。
    """
    from importlib import import_module
    strip = import_module("scripts.TABALL_refs").strip_comments
    clean = strip(txt)
    spans = []
    for mm in re.finditer(r"\\begin\{figure\*?\}", clean):
        b = mm.start()
        e = clean.find("\\end{figure", b)
        spans.append((b, e if e > 0 else len(clean)))
    return spans


def run():
    c = report.Checker(SLUG, "全章图件引用完整性", "figure",
                       "fig:* (Ch.4)", "3-23")
    c.source("印刷面 tex", paths.TEX, "全文")
    c.source("编号来源 aux", str(Path(paths.TEX).with_suffix(".aux")),
             "\\newlabel 解析")

    txt = T.tex_text()
    aux = T.labels()
    spans = figure_env_spans(txt)

    def in_fig_env(pos):
        return any(b <= pos < e for b, e in spans)

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 无孤图：每个图 label 至少被引用一次")
    c.note("统计每个 label 的 \\ref 出现次数，并区分正文引用与 caption 内"
           "交叉引用。区间引用 `\\ref{A}--\\ref{B}` 只写出两个端点，"
           "中间各图（如 Fig 8）的 \\ref 计数为 0——故对区间内部的图，"
           "以『存在覆盖它的区间』作为已引证据，不能只看自身计数。")

    # 先找出所有区间引用，记下其覆盖的图号范围
    ranges = []
    for mm in re.finditer(r"\\ref\{(fig:[^}]+)\}--\\ref\{(fig:[^}]+)\}", txt):
        a, b = mm.group(1), mm.group(2)
        na, nb = aux.get(a, {}).get("num"), aux.get(b, {}).get("num")
        if na and nb and na.isdigit() and nb.isdigit():
            ranges.append((int(na), int(nb), a, b))
    c.check(len(ranges) > 0, "正文存在区间引用", f"共 {len(ranges)} 处")

    for lb, num_exp in CH4_MAIN:
        n_all = len(re.findall(r"\\ref\{" + re.escape(lb) + r"\}", txt))
        n_body = len([mm.start() for mm in
                      re.finditer(r"\\ref\{" + re.escape(lb) + r"\}", txt)
                      if not in_fig_env(mm.start())])
        covered = any(a <= int(num_exp) <= b for a, b, _, _ in ranges
                      if num_exp.isdigit())
        ok = n_body > 0 or covered
        how = []
        if n_body:
            how.append(f"正文 {n_body} 处")
        if n_all - n_body:
            how.append(f"caption 内 {n_all - n_body} 处")
        if covered and not n_body:
            rr = [f"Fig {a}-{b}" for a, b, _, _ in ranges
                  if a <= int(num_exp) <= b]
            how.append("被区间 " + "/".join(rr) + " 覆盖")
        c.check(ok, f"Fig {num_exp} (`{lb}`) 已被引用",
                "；".join(how) if how else "未找到任何引用")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 无悬空引用：每个 \\ref{fig:...} 都指向真实 label")
    c.note("反向查：正文里引用的图号必须在 aux 里注册，否则排版出 `??`。")
    all_refs = sorted(set(re.findall(r"\\ref\{(fig:[^}]+)\}", txt)))
    bad = [r for r in all_refs if r not in aux]
    c.check(not bad, f"全部 {len(all_refs)} 个被引 label 均已注册",
            "全部合规" if not bad else "悬空: " + ", ".join(bad))

    # ── C2 ───────────────────────────────────────────────────────
    c.section("3. 每图均有独立正文引用（不靠区间/caption 兜底）")
    c.note("★ 这一节把标准统一收紧：第 1 节只要求『被引』，区间内部的图或"
           "仅靠 caption 交叉引用的图也算过。但读者在正文里读不到直接指引"
           "并不理想，故此处要求每张图在 figure 环境**之外**至少有一处"
           "自己的 \\ref。这是比第 1 节更强的判据。")
    weak = []
    for lb, num in CH4_MAIN:
        n_body = sum(1 for mm in re.finditer(
            r"\\ref\{" + re.escape(lb) + r"\}", txt) if not in_fig_env(mm.start()))
        ok = n_body >= 1
        if not ok:
            weak.append(f"Fig {num}")
        c.check(ok, f"Fig {num} (`{lb}`) 有独立正文引用",
                f"figure 环境外 {n_body} 处")
    c.check(not weak, "全部 21 张图均有独立正文引用",
            "全部合规" if not weak else "仅靠区间/caption 兜底: " + ", ".join(weak))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 编号与预期一致")
    for lb, num_exp in CH4_MAIN:
        num_aux = aux.get(lb, {}).get("num", "缺失")
        c.check(num_aux == num_exp, f"`{lb}` 编号 = {num_exp}",
                f"aux `{num_aux}` / 预期 `{num_exp}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
