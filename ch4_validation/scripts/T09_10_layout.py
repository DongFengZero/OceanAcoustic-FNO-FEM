#!/usr/bin/env python3
"""Tables 9-10 等宽版式一致性核验。

R1 修订把原来的四张表（perf-rect/perf-wedge/abl-rect/abl-wedge）合并为两张，
并 bound 在同一个 figure* 浮动体内，故"等宽"约束现在落在**两张**表之间：

- 列数都是 12（No. + Method/Variant + 10 个数值）
- 两张表的 tabular* 宽度参数一致（\linewidth），否则左右对不齐
- 样式宏各自配对：perf 用 \TABstylePerf，abl 用 \TABstylePerfTight
  （两者都是 \scriptsize + 紧凑列距，差别只在列距，属有意为之）
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, registry, report, texparse as T

SLUG = "T09_10_layout"
TABLES = {
    "tab:perf-cmp": {"num": 9, "style": "TABstylePerf", "col2": "Method"},
    "tab:abl": {"num": 10, "style": "TABstylePerfTight", "col2": "Variant"},
}


def run():
    c = report.Checker(SLUG, "Tables 9-10 等宽版式一致性", "cross-table", "", "")
    c.source("印刷面 tex", paths.TEX, "两张表所在 table* 环境")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 两张表可定位")
    envs = {}
    for lb, meta in TABLES.items():
        env, star = T.table_body_of(lb)
        envs[lb] = env
        c.check(env is not None, f"`{lb}` 表体可定位", f"长度 {len(env or '')}")
        if env:
            c.check(star, f"`{lb}` 用 tabular*（等宽所需）",
                    "tabular* 的宽度参数即总宽")
        n = T.number_of(lb)
        c.check(n == str(meta["num"]), f"`{lb}` 编号 = {meta['num']}",
                f"aux `{n}`")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 列数与列定义")
    pre = {}
    for lb, meta in TABLES.items():
        env = envs[lb]
        if not env:
            continue
        pre[lb] = T.tabular_preamble(env)
        c.check(pre[lb] is not None, f"`{lb}` 列定义可解析", f"`{pre[lb]}`")
    same_cols = len(set(v for v in pre.values() if v)) <= 1
    c.check(same_cols, "两表列定义相同（数值列数与列距一致）",
            " / ".join(f"{k.split(':')[1]}=`{v}`" for k, v in pre.items()))

    # ── C ────────────────────────────────────────────────────────
    c.section("3. tabular* 宽度参数一致（左右对齐的前提）")
    widths = {}
    for lb in TABLES:
        env = envs[lb] or ""
        m = re.search(r"\\begin\{tabular\*\}\{([^}]*)\}", env)
        widths[lb] = m.group(1) if m else None
    ok = None not in widths.values() and len(set(widths.values())) == 1
    c.check(ok, "两表总宽参数相同",
            " / ".join(f"{k.split(':')[1]}=`{v}`" for k, v in widths.items()))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 样式宏各自配对")
    c.note("样式宏写在 \\label 与 \\begin{tabular} 之间，落在表体区间之外，"
           "故从 label 前后的一段源码里读，而不是从表体里找。")
    txt = T.tex_text()
    for lb, meta in TABLES.items():
        li = txt.find("\\label{%s}" % lb)
        seg = txt[max(0, li - 1500): li + 200]
        got = re.findall(r"\\TABstyle\w*", seg)
        want = "\\" + meta["style"]
        c.check(want in got, f"`{lb}` 用 {meta['style']}",
                f"label 邻域内实得 {got}")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 两表数据行数与块结构")
    for lb, meta in TABLES.items():
        rows = T.data_rows(envs[lb], ncol=12)
        c.check(len(rows) > 0, f"`{lb}` 有数据行", f"实得 {len(rows)} 行")
        body = T.tabular_body(envs[lb]) or ""
        c.check(body.count("\\multicolumn{12}") == 2,
                f"`{lb}` 有两个几何分组小标题行",
                f"实得 {body.count(chr(92) + 'multicolumn{12}')} 个")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
