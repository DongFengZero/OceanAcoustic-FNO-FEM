#!/usr/bin/env python3
"""
PROSE_numbers.py — 正文每一个小数都必须有出处（跨对象核验）

方向是从正文出发，而不是从脚本出发。此前各表脚本的 PROSE 列表把正文数值写死在
脚本里，再拿这个常量去比对表格——并不读正文，正文写错了照样通过。变异测试证实：
把 4.3 节的 "1.688" 改成 "1.698"，T06 仍全部 PASS。

本脚本把摘要与第 4-5 章正文（去掉所有浮动体）里的每个小数逐一归类，三类之外即 FAIL：

  1. 表格印刷值：必须等于**本小节正文 \\ref 到的某张表**的印刷单元格（逐字符）。
     把一个数改成不存在的数、或改成本节所引表之外的数，都会落空。
  2. 推导量 / 门槛：用表格印刷值当场重算，或验证门槛论断本身成立。
  3. 配置参数：对照训练代码默认值；无法由数据核实的（软件版本号）单列豁免。

已知局限（如实登记）：若把一个数改成**同一张所引表里的另一个印刷值**，本检查
无法察觉——那需要逐句标注"此数指哪个单元格"，属于各表脚本 PROSE 列表的职责。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "PROSE_numbers"
B = chr(92)
NUM = re.compile(r"(?<![\w.{])(\d+(?:\{,\}\d{3})*\.\d+|\d+\{,\}\d{3})(?![\w}])")
CELL = re.compile(r"(?<![\w.])(\d+(?:\{,\}\d{3})*\.\d+|\d+\{,\}\d{3})(?![\w])")
BOLD = re.compile(r"\\textbf\{([^}]*)\}")
TRAINER = os.path.join(paths.REPO, "Experiment_Code", "Main_Code", "ocean_trainer_forward_b.py")


def run():
    c = report.Checker(SLUG, "正文每个小数的出处（表格印刷值 / 推导量 / 配置）", "table",
                       "prose (abstract + Sec. 4-5)", "—")
    c.source("印刷面 tex", paths.TEX, "摘要与第 4-5 章正文、全部表格")
    c.source("训练代码", TRAINER, "配置参数默认值")
    s = "\n".join(l for l in T.tex_text().split("\n") if not l.lstrip().startswith("%"))

    # ── 每张表的印刷单元格：共享浮动体按 label 取自己的 tabular，去掉加粗再取数 ──
    tab_cells, tab_rows = {}, {}
    for lab in sorted(set(re.findall(r"\\label\{(tab:[^}]*)\}", s))):
        env, _ = T.table_body_of(lab)
        if not env:
            continue
        # 浮动体里只有这一个表 label、却含多张 tabular（如 Table 14 的 (a)(b)）：取整个浮动体
        whole = T.table_env(lab) or ""
        if len(re.findall(r"\\label\{tab:", whole)) == 1 and len(re.findall(r"\\begin\{tabular", whole)) > 1:
            env = whole
        plain = BOLD.sub(r"\1", env)
        tab_cells[lab] = set(CELL.findall(plain))
        tab_rows[lab] = T.data_rows(env)

    def cell(label, row_key, col):
        """表 label 中首列(或第二列)为 row_key 的行，第 col 个数值单元格（印刷字面量）。"""
        for r in tab_rows[label]:
            if r[0].strip() == row_key or (len(r) > 1 and r[1].strip() == row_key):
                vals = [x.strip() for x in r if re.fullmatch(r"\d+\.\d+", x.strip())]
                return vals[col]
        raise KeyError((label, row_key))

    f3 = lambda x: f"{x:.3f}"
    code = open(TRAINER, encoding="utf8", errors="replace").read()

    def code_default(arg):
        m = re.search(r"'--" + arg + r"',\s*type=\w+,\s*default=([0-9.eE+-]+)", code)
        return float(m.group(1)) if m else None

    # Table 12 的 TL 列：行格式  Δ | No. Dataset Sol TL | No. Dataset Sol TL
    mesh_tl = []
    for r in tab_rows["tab:mesh"]:
        vals = [x.strip().strip("$") for x in r if re.fullmatch(r"\d+\.\d+", x.strip().strip("$"))]
        if len(vals) == 5:
            mesh_tl += [float(vals[2]), float(vals[4])]

    tl6 = lambda no: float(cell("tab:res-rect-mf", no, 9))      # Avg. TL
    dl = lambda row, k: float(cell("tab:dl-abl", row, k))
    derived = {
        "2.268": ("R3/R1 多频 TL 倍数 = Table 6 印刷值相除",
                  f3(tl6("5") / tl6("3")) == "2.268", f"{tl6('5')}/{tl6('3')}"),
        "8.676": ("R6/R4 单频 TL 倍数 = Table 7 印刷值相除",
                  f3(3.852 / 0.444) == "8.676" and {"3.852", "0.444"} <= tab_cells["tab:sq100"],
                  "3.852/0.444"),
        "1.356": ("Table 9：w/o graph − Full @75 Hz（印刷值相减）",
                  f3(dl("w/o graph correction", 2) - dl("Full model", 2)) == "1.356", ""),
        "1.834": ("Table 9：w/o graph − Full @100 Hz（印刷值相减）",
                  f3(dl("w/o graph correction", 3) - dl("Full model", 3)) == "1.834", ""),
        "0.65": ("门槛：Table 12 全部 TL < 0.65 dB",
                 len(mesh_tl) == 6 and max(mesh_tl) < 0.65,
                 f"max TL = {max(mesh_tl) if mesh_tl else None}"),
        "2.6": ("门槛：Table 10 中 DeepONet/KNO/CNO 矩形 Avg. TL 均 > 2.6 dB",
                all(float(cell("tab:perf-cmp", n, 9)) > 2.6 for n in ("16", "18", "19")), ""),
        "1.96": ("三维节点数 337351^1.5（PROSE_derived 回源核）", f"{337351 ** 1.5:.2e}" == "1.96e+08", ""),
        "1.35": ("513^3（PROSE_derived 回源核）", f"{513 ** 3:.2e}" == "1.35e+08", ""),
        "5.9": ("48²×16²（PROSE_derived 回源核）", f"{48 ** 2 * 16 ** 2:.1e}" == "5.9e+05", ""),
        "9.4": ("48²×16³（PROSE_derived 回源核）", f"{48 ** 2 * 16 ** 3:.1e}" == "9.4e+06", ""),
        "0.995": ("γ（ExponentialLR）↔ 训练代码", "gamma=0.995" in code, ""),
        "1.0": ("λ_p ↔ 训练代码 --loss_w_prior 默认值", code_default("loss_w_prior") == 1.0,
                f"default={code_default('loss_w_prior')}"),
        # 网格分辨率 Δ：对照 Table 12 的 Δ 列（同为印刷值）
        "1.00": ("网格分辨率 Δ ∈ Table 12 Δ 列", "1.00" in tab_cells["tab:mesh"], ""),
        "0.50": ("网格分辨率 Δ ∈ Table 12 Δ 列", "0.50" in tab_cells["tab:mesh"], ""),
        "0.25": ("网格分辨率 Δ ∈ Table 12 Δ 列", "0.25" in tab_cells["tab:mesh"], ""),
    }
    EXEMPT = {"6.4": "COMSOL 软件版本号（作者确认），非数据，无法由归档数据核实"}

    # ── 正文：去掉浮动体（等长空白保持位置），取摘要与第 4-5 章 ──
    body = re.sub(r"\\begin\{(table|figure)\*?\}.*?\\end\{\1\*?\}",
                  lambda m: " " * len(m.group(0)), s, flags=re.S)
    marks = [(m.start(), m.group(1)) for m in re.finditer(r"\\label\{(sec:[^}]*)\}", body)]
    bounds = [p0 for p0, _ in marks] + [len(body)]
    refd = {"front": set()}
    for k, (p0, lab) in enumerate(marks):
        refd[lab] = set(re.findall(r"\\ref\{(tab:[^}]*)\}", body[p0:bounds[k + 1]]))

    def sec_at(pos):
        cur = "front"
        for p0, lab in marks:
            if p0 <= pos:
                cur = lab
        return cur

    spans = [(body.find(B + "begin{abstract}"), body.find(B + "end{abstract}")),
             (body.find(B + "section{Experiments}"), body.find(B + "section*{Supplementary"))]

    c.section("1. 正文每个小数的出处", ("数值 @ 节", "依据", "结论"))
    c.note("表格印刷值须出自本小节正文 \\ref 到的表（逐字符）；推导量用印刷值当场重算；"
           "门槛验证论断本身；配置对照代码。任一数不属上述三类即 FAIL。")
    n = 0
    for a, b in spans:
        for m in NUM.finditer(body, a, b):
            v, pos = m.group(1), m.start()
            sec = sec_at(pos)
            n += 1
            ctx = re.sub(r"\s+", " ", body[max(0, pos - 40):pos + 15])
            if v in derived:
                desc, ok, ev = derived[v]
                c.check(bool(ok), f"`{v}` @ {sec}", f"{desc} {ev}")
            elif v in EXEMPT:
                c.exempt(f"`{v}` @ {sec}", EXEMPT[v])
            else:
                src = sorted(t for t in refd.get(sec, ()) if v in tab_cells.get(t, ()))
                # 数后面紧跟括注 "(Case~N)"（到下一个小数之前）：必须出自 Case N 那一行
                nxt = NUM.search(body, m.end(), b)
                tail = body[m.end():min(nxt.start() if nxt else b, m.end() + 60)]
                bind = re.search(r"\(Case~(\d+)\)", tail)      # 只认括注 "(Case~N)"
                if src and bind:
                    no = bind.group(1)
                    hit = []
                    for t in src:
                        for r in tab_rows.get(t, []):
                            cl = [BOLD.sub(r"\1", x).strip() for x in r]
                            # 并排表（矩形 | 楔形）里，算例号是每个列组的首格：只取该组
                            for i, x in enumerate(cl):
                                if x == no:
                                    j = next((k for k in range(i + 1, len(cl)) if cl[k].isdigit()), len(cl))
                                    if v in cl[i + 1:j]:
                                        hit.append(t)
                    c.check(bool(hit), f"`{v}` @ {sec} → Case {no}",
                            f"出自 {sorted(set(hit))} 的 Case {no} 行" if hit else
                            f"不在所引表 {src} 的 Case {no} 行；…{ctx}…")
                elif src:
                    c.check(True, f"`{v}` @ {sec}", f"印刷于本节所引 {src}")
                else:
                    where = sorted(t for t, cs in tab_cells.items() if v in cs)
                    c.check(False, f"`{v}` @ {sec}",
                            f"无出处：不在本节所引表 {sorted(refd.get(sec, ()))} 中"
                            + (f"（仅见于 {where}）" if where else "") + f"；…{ctx}…")
    c.note(f"共核 {n} 个正文小数。")
    return c


if __name__ == "__main__":
    sys.exit(run().finish())
