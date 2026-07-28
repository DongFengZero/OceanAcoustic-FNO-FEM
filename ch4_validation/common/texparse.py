"""
texparse.py — 从 tex/aux 里取"印刷事实"
========================================
核验的一侧是原始数据，另一侧必须是 tex 里真正排出来的东西，
不是脚本里另抄一遍的期望值。本模块只负责如实读出印刷面。

提供：
  labels()             aux 里 label -> (编号, 页码)，给出真实表号/图号
  table_env(label)     含该 label 的表格环境源码（caption + tabular）
  caption_of(label)    该 label 的 caption 文本（花括号配平截取）
  data_rows(env)       tabular 数据行 -> 每行 cell 列表（去掉 \\textbf 等包装）
  cite_contexts(pat)   正文中匹配某模式的句子，用于文段引用核查
"""
import os
import re

from . import paths


def _read(p):
    return open(p, encoding="utf-8", errors="ignore").read()


# ══════════════════════════════════════════════════════════════════════
#  aux：真实编号
# ══════════════════════════════════════════════════════════════════════
def labels():
    """label -> {'num':'13', 'page':'18'}。aux 缺失时返回空表。"""
    if not os.path.exists(paths.AUX):
        return {}
    txt = _read(paths.AUX)
    out = {}
    for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}\{([^}]*)\}", txt):
        out[m.group(1)] = {"num": m.group(2), "page": m.group(3)}
    return out


def number_of(label):
    return labels().get(label, {}).get("num")


# ══════════════════════════════════════════════════════════════════════
#  tex：环境与 caption
# ══════════════════════════════════════════════════════════════════════
def tex_text():
    return _read(paths.TEX)


def _brace_span(txt, open_pos):
    """txt[open_pos] == '{' 时，返回配平的闭合位置索引。"""
    d = 0
    for i in range(open_pos, len(txt)):
        if txt[i] == "{":
            d += 1
        elif txt[i] == "}":
            d -= 1
            if d == 0:
                return i
    return -1


def table_env(label, txt=None):
    """含 \\label{label} 的最小 minipage/table/figure 环境源码。

    表格被 minipage 绑在 figure* 浮动体里（本文多表共页的排法），
    故优先取 minipage 边界，落空再退到 table/figure*。

    ★ 必须校验"环境真的包住了 label"，不能只取最近的 begin + 最近的 end：
      Table 6 是裸 \\begin{table*}，其前方是 Table 4/5 所在浮动体的 minipage。
      不加校验时 rfind 会命中那个 minipage 的 begin，再配上 Table 7 的
      \\end{minipage}，跨出一个横穿三张表的错误区间。
      判据：begin 与 label 之间不得再出现同类型的 end。
    """
    txt = txt if txt is not None else tex_text()
    li = txt.find(f"\\label{{{label}}}")
    if li < 0:
        return None
    for beg, end in (("\\begin{minipage}", "\\end{minipage}"),
                     ("\\begin{table}", "\\end{table}"),
                     ("\\begin{table*}", "\\end{table*}"),
                     ("\\begin{figure*}", "\\end{figure*}"),
                     ("\\begin{figure}", "\\end{figure}")):
        b = txt.rfind(beg, 0, li)
        e = txt.find(end, li)
        if b < 0 or e <= li:
            continue
        if txt.find(end, b, li) != -1:      # begin…label 间已闭合 -> 不是包住 label 的环境
            continue
        return txt[b: e + len(end)]
    return None


def caption_of(label, txt=None):
    """label 对应的 caption 纯文本（\\caption 或 \\captionof{table|figure}）。"""
    txt = txt if txt is not None else tex_text()
    li = txt.find(f"\\label{{{label}}}")
    if li < 0:
        return None
    best = None
    for m in re.finditer(r"\\(?:captionof\{(?:table|figure)\}|caption)\s*\{", txt):
        if m.end() - 1 < li:
            best = m
        else:
            break
    if best is None:
        return None
    close = _brace_span(txt, best.end() - 1)
    return txt[best.end(): close]


def tabular_body(env):
    """环境源码 -> tabular/tabular* 的行体（\\midrule 之后、\\bottomrule 之前）。"""
    if env is None:
        return None
    i = env.find("\\midrule")
    j = env.find("\\bottomrule")
    if i < 0 or j < 0:
        return None
    return env[i + len("\\midrule"): j]


def tabular_preamble(env):
    """环境源码 -> tabular/tabular* 的列定义串，如 `@{}ll c ccc@{}`。

    用于跨表版式比对：并列于同一浮动体的两张表若列定义不同，
    渲染宽度就不同，读者无法左右对读。`tabular*` 的宽度参数
    （`{\\linewidth}`）不算列定义，需跳过。
    """
    if env is None:
        return None
    m = re.search(r"\\begin\{tabular\*?\}", env)
    if not m:
        return None
    pos = m.end()
    # tabular* 先带一个宽度参数，跳过它
    if env[m.start():m.end()].endswith("*}"):
        while pos < len(env) and env[pos] in " \t\n":
            pos += 1
        if pos < len(env) and env[pos] == "{":
            end = _brace_span(env, pos)
            if end < 0:
                return None
            pos = end + 1
        # 可能还有 \extracolsep 之类插在中间
        while pos < len(env) and env[pos] in " \t\n":
            pos += 1
        if pos < len(env) and env[pos] == "@":
            pass
    while pos < len(env) and env[pos] in " \t\n":
        pos += 1
    if pos >= len(env) or env[pos] != "{":
        return None
    end = _brace_span(env, pos)
    if end < 0:
        return None
    return env[pos + 1:end].strip()


def header_row(env):
    """环境源码 -> 表头行（\\toprule 与 \\midrule 之间），已压缩空白。

    多行表头（\\cmidrule 分层）会整段返回，比对时按整体是否逐字符相同判定。
    """
    if env is None:
        return None
    i = env.find("\\toprule")
    j = env.find("\\midrule")
    if i < 0 or j < 0 or j < i:
        return None
    return re.sub(r"\s+", " ", env[i + len("\\toprule"):j]).strip()


_STRIP = [
    (re.compile(r"\\textbf\s*\{([^{}]*)\}"), r"\1"),
    (re.compile(r"\\scriptsize\s*"), ""),
    (re.compile(r"\\,"), ""),
    (re.compile(r"\\%"), "%"),
    (re.compile(r"\\times"), "x"),
]


def clean_cell(s):
    """去掉排版包装，留下可比对的字面值。保留 $...$ 内容（源位置等）。"""
    s = s.strip()
    for _ in range(3):                       # \textbf{\textbf{}} 之类嵌套
        for rx, rep in _STRIP:
            s = rx.sub(rep, s)
    s = s.replace("{", "").replace("}", "").strip()
    return s


def data_rows(env, ncol=None):
    """tabular 数据行列表，每项为该行的 cell 列表（已 clean）。

    过滤掉 \\cmidrule / 空行 / 纯 \\addlinespace 行。
    ncol 给定时只保留列数相符的行，用于排除跨列说明行。
    """
    body = tabular_body(env)
    if body is None:
        return []
    rows = []
    for raw in body.split("\\\\"):
        line = raw.strip()
        if not line or line.startswith("\\cmidrule") or line.startswith("\\addlinespace"):
            continue
        line = re.sub(r"\\cmidrule\(?[^)]*\)?\{[^}]*\}", "", line).strip()
        if not line:
            continue
        cells = [clean_cell(c) for c in line.split("&")]
        if ncol is not None and len(cells) != ncol:
            continue
        rows.append(cells)
    return rows


def data_rows_raw(env, ncol=None):
    """同 data_rows，但**不做 clean**，保留 \\ref/\\subref/\\textbf 原文。

    Fig. 列的内容形如 `\\ref{fig:res-128}\\subref{fig:res-128-r}`，
    clean_cell 会把花括号剥掉变成 `\\reffig:res-128…`，无法再解析出 label。
    需要核验图号引用时用本函数。
    """
    body = tabular_body(env)
    if body is None:
        return []
    rows = []
    for raw in body.split("\\\\"):
        line = raw.strip()
        if not line or line.startswith("\\cmidrule") or line.startswith("\\addlinespace"):
            continue
        line = re.sub(r"\\cmidrule\(?[^)]*\)?\{[^}]*\}", "", line).strip()
        if not line:
            continue
        cells = [x.strip() for x in line.split("&")]
        if ncol is not None and len(cells) != ncol:
            continue
        rows.append(cells)
    return rows


def refs_in(cell):
    """cell 原文里的 \\ref / \\subref 目标 label 列表，按出现顺序。"""
    return re.findall(r"\\(?:sub)?ref\s*\{([^}]*)\}", cell)


def bold_mask(env, ncol=None):
    """与 data_rows 同形的布尔表，标记该 cell 原文是否带 \\textbf。"""
    body = tabular_body(env)
    if body is None:
        return []
    out = []
    for raw in body.split("\\\\"):
        line = raw.strip()
        if not line or line.startswith("\\cmidrule") or line.startswith("\\addlinespace"):
            continue
        line = re.sub(r"\\cmidrule\(?[^)]*\)?\{[^}]*\}", "", line).strip()
        if not line:
            continue
        cells = line.split("&")
        if ncol is not None and len(cells) != ncol:
            continue
        out.append(["\\textbf" in c for c in cells])
    return out


# ══════════════════════════════════════════════════════════════════════
#  正文引用
# ══════════════════════════════════════════════════════════════════════
def body_text(start_marker=None, end_marker=None, txt=None):
    """正文切片。缺省取第 4 章（Results 起、Conclusion 前）。"""
    txt = txt if txt is not None else tex_text()
    b = txt.find(start_marker) if start_marker else 0
    e = txt.find(end_marker) if end_marker else len(txt)
    return txt[b if b >= 0 else 0: e if e > 0 else len(txt)]


def numbers_in(s):
    """字符串里的所有数字字面量（含小数），按出现顺序返回字符串形式。

    返回字面量而非 float：位数信息不能丢，"0.44" 与 "0.440" 必须可区分。
    """
    return re.findall(r"\d+\.\d+|\d+", s)


def sentences_with(pattern, txt=None, window=260):
    """返回正文中匹配 pattern 的片段（前后各留 window/2 字符），用于人工复核定位。"""
    txt = txt if txt is not None else tex_text()
    out = []
    for m in re.finditer(pattern, txt):
        a = max(0, m.start() - window // 2)
        b = min(len(txt), m.end() + window // 2)
        out.append((m.start(), txt[a:b].replace("\n", " ")))
    return out


def line_of(offset, txt=None):
    """字符偏移 -> tex 行号，报告里给出可点击定位。"""
    txt = txt if txt is not None else tex_text()
    return txt.count("\n", 0, offset) + 1
