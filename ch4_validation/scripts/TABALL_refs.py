#!/usr/bin/env python3
"""
全章表格引用完整性核验（跨表，非单表）

单表脚本各自核了自己的数值与正文引用，但缺三项只能在全局做的检查：
  A. 每个表 label 都至少被引用一次（无孤表）
  B. 每个 \\ref{tab:...} 都指向真实存在的 label（无悬空引用）
  C. 每张表都有**独立正文引用**（不靠区间或 table 环境内交叉引用兜底）

引用形式在本章有四种，判定时都算「已引」：
  1. 散文单点   Table~\\ref{tab:ideal-overall}
  2. 散文区间   Tables~\\ref{tab:dl-cmp-rect}--\\ref{tab:dl-cmp-wedge}
  3. 散文并列   Tables~\\ref{A}, \\ref{B}, and \\ref{C}
  4. 环境内交叉 caption 里的 as in Table~\\ref{...}
只按 1 判定会把区间内部的表误判为漏引。

Tables 1/2 属方法章（method-comparison / method-symbols），一并核引用，
但不计入第 4 章数值链。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "TABALL_refs"

# 全部表 label 与预期编号。Tables 1/2 属方法章，3-21 属第 4 章。
ALL_TABS = [
    ("tab:method-comparison", "1"), ("tab:method-symbols", "2"),
    ("tab:datasets", "3"),
    ("tab:ideal-overall", "4"), ("tab:ideal-depthline", "5"),
    ("tab:res-rect-mf", "6"), ("tab:res-rect-100", "7"),
    ("tab:res-wedge-100", "8"),
    ("tab:dl-cmp-rect", "9"), ("tab:dl-cmp-wedge", "10"),
    ("tab:dl-abl-rect", "11"), ("tab:dl-abl-wedge", "12"),
    ("tab:perf-rect", "13"), ("tab:perf-wedge", "14"),
    ("tab:abl-rect", "15"), ("tab:abl-wedge", "16"),
    ("tab:mesh-rect", "17"), ("tab:mesh-wedge", "18"),
    ("tab:gen-overall", "19"),
    ("tab:runtime", "20"), ("tab:runtime-scale", "21"),
]
CH4 = [t for t in ALL_TABS if int(t[1]) >= 3]


def strip_comments(txt):
    """把 LaTeX 注释替换成等长空格（保持所有偏移量不变）。

    必须先做这一步：模板里有 `% ... \\begin{figure*} (double-column) float`
    这样的说明性注释，若当成真环境，其区间会从注释处一直张开到下一个
    \\end{figure}，把中间所有正文引用误判为「环境内引用」。
    用等长空格而非删除，是为了让 span 位置仍可与原文偏移对齐。
    """
    out = []
    for line in txt.split("\n"):
        i, esc = -1, False
        for k, ch in enumerate(line):
            if ch == "\\":
                esc = not esc
                continue
            if ch == "%" and not esc:
                i = k
                break
            esc = False
        out.append(line if i < 0 else line[:i] + " " * (len(line) - i))
    return "\n".join(out)


def env_spans(txt):
    """table/table*/figure/figure* 环境区间。

    表可以排在 figure* 里（本章 Tables 4/5、9-12、13-16、17/18 都是
    captionof{table} 嵌在 figure* 内的并列版式），故两类环境都要算，
    否则那些表的 caption 内交叉引用会被误判成正文引用。
    """
    clean = strip_comments(txt)
    spans = []
    for pat, endpat in ((r"\\begin\{table\*?\}", "\\end{table"),
                        (r"\\begin\{figure\*?\}", "\\end{figure")):
        for mm in re.finditer(pat, clean):
            b = mm.start()
            e = clean.find(endpat, b)
            spans.append((b, e if e > 0 else len(clean)))
    return spans


def run():
    c = report.Checker(SLUG, "全章表格引用完整性", "table",
                       "tab:* (all)", "1-21")
    c.source("印刷面 tex", paths.TEX, "全文")
    c.source("编号来源 aux", str(Path(paths.TEX).with_suffix(".aux")),
             "\\newlabel 解析")

    txt = T.tex_text()
    aux = T.labels()
    spans = env_spans(txt)

    def in_env(pos):
        return any(b <= pos < e for b, e in spans)

    # 区间引用：记录覆盖的编号范围
    ranges = []
    for mm in re.finditer(r"\\ref\{(tab:[^}]+)\}--\\ref\{(tab:[^}]+)\}", txt):
        a, b = mm.group(1), mm.group(2)
        na = aux.get(a, {}).get("num")
        nb = aux.get(b, {}).get("num")
        if na and nb and na.isdigit() and nb.isdigit():
            ranges.append((int(na), int(nb)))

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 无孤表：每个 label 至少被引用一次")
    c.note("区间引用只写两个端点，中间各表的自身 \\ref 计数为 0，"
           "故对区间内部的表以『存在覆盖它的区间』作为已引证据。")
    for lb, num in ALL_TABS:
        hits = [mm.start() for mm in
                re.finditer(r"\\ref\{" + re.escape(lb) + r"\}", txt)]
        n_body = sum(1 for p in hits if not in_env(p))
        n_env = len(hits) - n_body
        covered = [(a, b) for a, b in ranges
                   if a < int(num) < b]
        ok = len(hits) > 0 or bool(covered)
        detail = f"正文 {n_body} 处"
        if n_env:
            detail += f"；环境内 {n_env} 处"
        if covered:
            detail += "；被区间 " + ", ".join(
                f"Table {a}-{b}" for a, b in covered) + " 覆盖"
        c.check(ok, f"Table {num} (`{lb}`) 已被引用", detail)

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 无悬空引用：每个 \\ref 都指向真实 label")
    known = {lb for lb, _ in ALL_TABS}
    bad = []
    for mm in re.finditer(r"\\ref\{(tab:[^}]+)\}", txt):
        lb = mm.group(1)
        if lb not in known or lb not in aux:
            bad.append(lb)
    c.check(not bad, "全部 \\ref{tab:...} 的 label 均已注册",
            "全部合规" if not bad else "悬空: " + ", ".join(sorted(set(bad))))

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 每表均有独立正文引用（不靠区间/环境内兜底）")
    c.note("★ 比第 1 节更强：要求每张表在 table/figure 环境**之外**至少有"
           "一处自己的 \\ref。仅靠区间覆盖或 caption 交叉引用的表，读者在"
           "正文里读不到直接指引。")
    weak = []
    for lb, num in ALL_TABS:
        n_body = sum(1 for mm in re.finditer(
            r"\\ref\{" + re.escape(lb) + r"\}", txt) if not in_env(mm.start()))
        ok = n_body >= 1
        if not ok:
            weak.append(f"Table {num}")
        c.check(ok, f"Table {num} (`{lb}`) 有独立正文引用",
                f"环境外 {n_body} 处")
    c.check(not weak, f"全部 {len(ALL_TABS)} 张表均有独立正文引用",
            "全部合规" if not weak else "仅靠兜底: " + ", ".join(weak))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 编号与预期一致")
    for lb, num_exp in ALL_TABS:
        num_aux = aux.get(lb, {}).get("num", "缺失")
        c.check(num_aux == num_exp, f"`{lb}` 编号 = {num_exp}",
                f"aux `{num_aux}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
