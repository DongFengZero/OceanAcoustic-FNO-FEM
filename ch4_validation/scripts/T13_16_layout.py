#!/usr/bin/env python3
"""Tables 13–16 等宽版式一致性核验。

四张表 bound in one float，必须等宽：
- 列数都是 12（No. + Method/Variant + 10 个数值）
- tabular preamble 一致
- 样式宏配对（13/14 用 \TABstylePerf，15/16 用 \TABstylePerfTight）
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, registry, report, texparse as T

SLUG = "T13_16_layout"
TABLES = {
    "tab:perf-rect": {"num": 13, "style": "TABstylePerf", "col2": "Method"},
    "tab:perf-wedge": {"num": 14, "style": "TABstylePerf", "col2": "Method"},
    "tab:abl-rect": {"num": 15, "style": "TABstylePerfTight", "col2": "Variant"},
    "tab:abl-wedge": {"num": 16, "style": "TABstylePerfTight", "col2": "Variant"},
}


def run():
    c = report.Checker(SLUG, "Tables 13–16 等宽版式一致性", "cross-table", "", "")
    c.source("印刷面 tex", paths.TEX, "四张表所在 table* 环境")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 四张表可定位")
    envs = {}
    for lb, meta in TABLES.items():
        env = T.table_env(lb)
        envs[lb] = env
        c.check(env is not None and f"\\label{{{lb}}}" in env,
                f"Table {meta['num']} ({lb}) 环境存在",
                f"长度 {len(env or '')}")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 样式宏正确性")
    c.note("Tables 13/14 用 \\TABstylePerf，Tables 15/16 用 \\TABstylePerfTight")
    for lb, meta in TABLES.items():
        style = meta["style"]
        c.check(f"\\{style}" in envs[lb],
                f"Table {meta['num']} 使用 `\\{style}`",
                "存在" if f"\\{style}" in envs[lb] else "缺失")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. tabular preamble 一致性")
    c.note("四张表都是 12 列（No. + Method/Variant + 10 个数值），"
           "preamble 应为 `cl*{10}{c}` 或等价形式")
    preambles = {}
    for lb, meta in TABLES.items():
        # 从 env 中提取 \begin{tabular*}{...}{preamble}
        m = re.search(r"\\begin\{tabular\*?\}(?:\[.*?\])?\{[^}]*?\}\{([^}]+)\}", envs[lb])
        pre = m.group(1) if m else None
        preambles[lb] = pre
        c.check(pre is not None, f"Table {meta['num']} preamble 可提取",
                f"`{pre}`" if pre else "未找到")

    # 规范化比较（忽略 @{} 填充符）
    def normalize(p):
        if p is None:
            return None
        # 移除 @{\extracolsep{\fill}} 等填充
        p = re.sub(r'@\{[^}]*\}', '', p)
        p = p.strip()
        return p

    norm_pres = {lb: normalize(p) for lb, p in preambles.items()}
    baseline = norm_pres["tab:perf-rect"]
    for lb, meta in TABLES.items():
        if lb == "tab:perf-rect":
            continue
        c.check(norm_pres[lb] == baseline,
                f"Table {meta['num']} preamble 与 Table 13 一致",
                f"Table {meta['num']}: `{norm_pres[lb]}` / Table 13: `{baseline}`")

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 列数验证")
    c.note("ncol=12 提取数据行，确认四张表都能提取到正确行数")
    for lb, meta in TABLES.items():
        rows = T.data_rows(envs[lb], ncol=12)
        expected = 5 if meta["num"] in (13, 14) else 4
        c.check(len(rows) == expected,
                f"Table {meta['num']} 数据行数 = {expected}",
                f"实得 {len(rows)}")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 表头第二列标题一致性")
    c.note("Tables 13/14 第二列应为 'Method'，Tables 15/16 应为 'Variant'")
    for lb, meta in TABLES.items():
        # 提取 multirow 行的第二列（从 env 而非 body）
        pattern = r"\\multirow\{2\}\{\*\}\{No\.\}\s*&\s*\\multirow\{2\}\{\*\}\{([^}]+)\}"
        m = re.search(pattern, envs[lb])
        col2 = m.group(1).strip() if m else None
        c.check(col2 == meta["col2"],
                f"Table {meta['num']} 第二列标题 = `{meta['col2']}`",
                f"实得 `{col2}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
