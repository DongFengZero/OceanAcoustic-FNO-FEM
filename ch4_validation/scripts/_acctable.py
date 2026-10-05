# -*- coding: utf-8 -*-
"""_acctable.py — 精度表核验的公用部分。

R1 把矩形与楔形两张表并排合并为一张（如 Table 6 = R4-R6 | W4-W6），
合并后各行/各块的检查项与合并前逐条相同，只是列偏移不同。为避免十二份
脚本各抄一遍同样的判据（改一处漏一处），共用逻辑集中在这里：

  acc_blocks()    合并表按"块"切分：每个块给出几何名、案例列、数值列偏移
  check_sources() 源可追溯：xlsx / log / tex 环境
  check_epoch()   best epoch：xlsx 列的取值须与日志自证一致
  check_dual()    双渠道交叉：xlsx vs 同轮日志评估块
  check_printed() 印刷值：源值舍入到 3 位与 tex 单元格逐字符比对
  check_decimals()数值格位数一致
  check_caption() caption 的 epoch 声明与表号

各表脚本只提供自己的块定义与正文引用清单。
"""
import os
import re

from common import metrics as M
from common import paths, report, texparse as T

FREQS = (25, 50, 75, 100)


def acc_blocks(env, ncol, blocks):
    """把合并表的数据行切成块。

    blocks: [(名称, 案例, 首列索引), ...]，首列索引是该块 "No." 所在的列。
    返回 {案例: 该行 cell 列表} 与 {案例: 块名}，行号取自各自的 No. 列。

    合并表的每个块各有一列 No.，故同一行里可能同时出现两个案例号
    （矩形 No. 与楔形 No.）；按块给的首列索引分别读取，才不会张冠李戴。
    """
    rows = T.data_rows(env, ncol=ncol)
    out, owner = {}, {}
    for name, cases, c0 in blocks:
        for r in rows:
            v = r[c0].strip()
            if not v.isdigit():
                continue
            no = int(v)
            if no in cases:
                out[no] = r
                owner[no] = name
    return out, owner, rows


def check_sources(c, label, xl, cases, note=""):
    """源清单与存在性。"""
    c.source("印刷面 tex", paths.TEX, f"`\\label{{{label}}}` 所在环境")
    c.source("渠道1 xlsx", xl, note or "工作表1，best epoch 全测试集")
    logs = {}
    c.section("2. 源可追溯性")
    c.check(os.path.exists(xl), "xlsx 存在", paths.rel(xl))
    for no in cases:
        lp = paths.log_path(no)
        logs[no] = lp
        c.check(lp is not None and os.path.exists(lp), f"Case {no} 日志存在",
                paths.rel(lp) if lp else "未找到")
        if lp:
            c.source(f"渠道2 log (Case {no})", lp, "训练日志同轮『评估』块")
    env = T.table_env(label)
    c.check(env is not None and f"\\label{{{label}}}" in env,
            "tex 表格环境可定位且确实包住 label", f"长度 {len(env or '')}")
    return env, logs


def check_epoch(c, xl, logs, cases, title="3. best epoch 一致性"):
    """xlsx 记载的 best epoch 须与日志自证一致，且该轮块存在。"""
    c.section(title, ("案例", "xlsx / 日志自证", "结论"))
    xd, ld = {}, {}
    for no in cases:
        xd[no] = M.xlsx_case(xl, no)
        be_x = xd[no]["best_epoch"]
        be_l = M.log_best_epoch(logs[no])
        c.check(be_x == be_l, f"Case {no} best epoch",
                f"xlsx `{be_x}` / log `{be_l}`")
        ld[no] = M.log_epoch(logs[no], be_x)
        c.check(ld[no] is not None, f"Case {no} 日志含『评估 Epoch {be_x}』块",
                f"轮次 {be_x}")
    return xd, ld


def check_dual(c, xd, ld, cases, groups, title="4. 双渠道交叉验证（xlsx vs log）"):
    """xlsx 与同轮日志的两个渠道须互相印证。"""
    c.section(title, ("量", "xlsx / log", "结论"))
    for no in cases:
        for g in groups:
            for q in ("sol", "tl"):
                a, b = xd[no][g][q], ld[no][g][q]
                ok = (a is not None and b is not None
                      and abs(a - b) <= max(1e-9, abs(a) * 2e-6))
                gname = "Avg." if g == "Overall" else f"{g}Hz"
                c.check(ok, f"Case {no} {gname} {q.upper()}",
                        f"`{a!r}` / `{b!r}`")


def check_printed(c, xd, ld, printed, spec, title="5. 印刷值比对（舍入到 3 位 vs tex）"):
    """spec: {case: [(标签, 起始列, 组序), ...]}；组序给出该案例要核的组。

    源的舍入判定走 report.eq（源→3 位 vs 印刷），两个渠道各核一遍。
    """
    c.section(title)
    for no, items in spec.items():
        for cell_label, c0, groups in items:
            for k, g in enumerate(groups):
                for j, q in enumerate(("sol", "tl")):
                    gname = "Avg." if g == "Overall" else f"{g}Hz"
                    cell = printed[no][c0 + k * 2 + j]
                    c.eq(f"{cell_label} {gname} {q.upper()} (xlsx)",
                         xd[no][g][q], cell)
                    c.eq(f"{cell_label} {gname} {q.upper()} (log)",
                         ld[no][g][q], cell)


def check_decimals(c, printed, cases, cols, title="6. 同表小数位一致性"):
    bad = []
    for no in cases:
        for j in cols:
            v = printed[no][j]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} 第{j + 1}列 `{v}`")
    n = len(cases) * len(cols)
    c.section(title)
    c.check(not bad, f"全部 {n} 个数值单元格均为 3 位小数",
            "全部合规" if not bad else "；".join(bad))


def check_caption(c, label, number, want_epoch=None,
                  title="7. caption 声明核验"):
    """caption 的 epoch 口径与表号。"""
    cap = T.caption_of(label) or ""
    c.section(title)
    if want_epoch:
        c.check(want_epoch in cap, f"caption 声明 {want_epoch}",
                "数据源确为该口径")
        for other in ("best epoch", "last epoch"):
            if other != want_epoch:
                c.check(other not in cap, f"caption 未误写 {other}",
                        "口径唯一")
    got = T.number_of(label)
    c.check(got == str(number), f"表号为 {number}", f"aux `{got}`")


def bold_col_min(env, rows, c0, ncol=None):
    """返回 {列索引: 该列加粗所在的行号}，用于"最小值加粗"类判据。"""
    mask = T.bold_mask(env, ncol=ncol)
    out = {}
    for i, r in enumerate(rows):
        v = r[c0].strip()
        if not v.isdigit() or i >= len(mask):
            continue
        out[int(v)] = mask[i]
    return out
