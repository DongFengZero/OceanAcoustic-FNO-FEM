#!/usr/bin/env python3
"""
PROSE_derived.py — 正文中不属于任何表/图的数值（跨对象核验）

覆盖审计（_tmp/_coverage.py）显示，摘要与第 4–5 章正文里共 85 个具体数值，
81 个已由各表/图脚本断言；余下 4 个只出现在正文里，不挂靠任何表格：

  γ = 0.995           学习率衰减系数（4.1 节）
  1.96×10^8           三维节点数估计（第 5 章结论三维代价段）
  > 2.6 dB            "其余基线 TL 均超过 2.6 dB"（4.4 节）
  8000 / 2000         "每个多频算例 8000 个有限元解，每频 2000"（第 5 章）

其中 8000 那句曾写成"每个算例 8000 个解"，与 Table 3 中 20 个单频算例
（2000 个解）矛盾——正因为没有任何脚本断言它，才一直没被发现。

本脚本把这几处、连同三维段落里的其余推导量（5.9×10^5、9.4×10^6、96 倍），以及 4.1 节的 FNO 超参数，逐一回到**源头**核对：
  · 超参数 → 训练代码（Experiment_Code）里的默认值
  · 节点数 → 4.8 节运行时 xlsx（与 Table 13 同源）
  · 样本数 → Table 3 印刷值（Table 3 自身已由 T03 回到 Dataset 核过）
  · 基线 TL → 4.4 节精度 xlsx（与 Table 9 同源）
  · 推导量 → 用上述源值现场重算，按正文位数比对
"""
import os
import re
import sys

import _boot  # noqa: F401
from common import metrics as M
from common import paths, report, texparse as T

SLUG = "PROSE_derived"
CODE = os.path.join(paths.REPO, "Experiment_Code", "Main_Code")
TRAINER = os.path.join(CODE, "ocean_trainer_forward_b.py")
MODELS = os.path.join(CODE, "deq_modules", "models.py")
BS = chr(92)


def grab(path, pattern, cast=float):
    src = open(path, encoding="utf8", errors="replace").read()
    m = re.search(pattern, src)
    return cast(m.group(1)) if m else None


def sci(v, digits):
    """1.959e8 -> '1.96\\times10^{8}'（与正文写法一致）"""
    e = len(str(int(abs(v)))) - 1
    return f"{v / 10 ** e:.{digits}f}" + BS + f"times10^{{{e}}}"


def run():
    c = report.Checker(SLUG, "正文推导与独立数值（不挂靠表/图）", "table",
                       "prose", "—")
    txt = T.tex_text()
    c.source("印刷面 tex", paths.TEX, "4.1 / 4.4 节与第 5 章正文")
    c.source("训练代码", TRAINER, "学习率调度、通道宽度")
    c.source("模型代码", MODELS, "FNO 网格/模态/层数")
    c.source("运行时 xlsx", paths.xlsx_path("4.8"), "网格节点数（Table 13 同源）")
    c.source("精度 xlsx", paths.xlsx_path("4.4"), "基线 TL（Table 9 同源）")

    # ── 1. 4.1 节 FNO 超参数 vs 代码 ───────────────────────────────
    c.section("1. 4.1 节超参数 ↔ 训练代码默认值")
    gamma = grab(TRAINER, r"ExponentialLR\([^)]*?gamma\s*=\s*([0-9.]+)")
    width = grab(TRAINER, r"'--hidden_channels',\s*type=int,\s*default=(\d+)", int)
    grid = grab(MODELS, r"self\.fno_corr = _FNOScatterField\([\s\S]{0,300}?grid=(\d+)", int)
    modes = grab(MODELS, r"self\.fno_corr = _FNOScatterField\([\s\S]{0,300}?modes=(\d+)", int)
    layers = grab(MODELS, r"n_layers: int = (\d+)", int)
    for name, val, lit in (("γ (ExponentialLR)", gamma, BS + "gamma=0.995"),
                           ("G (FNO 网格)", grid, "$G=64$"),
                           ("W (通道宽度)", width, "$W=48$"),
                           ("L (Fourier 层数)", layers, "$L=4$"),
                           ("m1=m2 (保留模态)", modes, "$m_1=m_2=16$")):
        printed = re.search(r"[0-9.]+(?=\$?\)?$)", lit.rstrip("$")).group(0)
        c.check(val is not None and lit in txt and f"{val:g}" == f"{float(printed):g}",
                f"{name}：代码 `{val}` / 正文 `{lit}`", "代码默认值与正文一致")

    # ── 2. 第 5 章三维代价段的推导量 ────────────────────────────────
    c.section("2. 第 5 章三维代价段：推导量现场重算（节点数取自 4.8 节 xlsx）")
    import T13_runtime as R
    scale = R.load_scale()
    n_max = max(d["n"] for d in scale.values())
    lx_max = max(d["lx"] for d in scale.values())
    c.check(f"$N={n_max:,}$".replace(",", "{,}") in txt,
            f"最大网格节点数 N = {n_max:,}（xlsx）出现在正文", f"Lx = {lx_max} m")
    n3 = n_max ** 1.5
    c.check(sci(n3, 2) in txt, "三维节点数 N^{3/2}",
            f"`{n_max}^1.5 = {n3:.4e}` → `{sci(n3, 2)}`")
    wts = width ** 2 * modes ** 2
    c.check(sci(wts, 1) in txt, "每层截断模态张量 W²m1m2",
            f"`{width}²×{modes}² = {wts:,}` → `{sci(wts, 1)}`")
    c.check(sci(wts * modes, 1) in txt, "三维每层权重（×m3=16）",
            f"`{wts * modes:,}` → `{sci(wts * modes, 1)}`")
    ratio = (grid ** 3 * 3) / (grid ** 2 * 2)          # G^3 log G^3 / G^2 log G^2
    c.check(f"about {ratio:.0f} times more work at $G={grid}$" in txt,
            "FFT 代价增长倍数 (G³logG³)/(G²logG²) = 1.5G", f"`1.5×{grid} = {ratio:g}`")

    # ── 3. 第 5 章"每个多频算例 8000 个解，每频 2000" ↔ Table 3 ────
    c.section("3. 参考解数量 ↔ Table 3")
    env = T.table_env("tab:datasets")
    rows = T.data_rows(env, ncol=13)
    multi = [r for r in rows if "," in r[7]]            # 多频算例：频率列含逗号
    single = [r for r in rows if "," not in r[7]]
    c.check(all(r[8].replace(" ", "").startswith("8000") for r in multi),
            f"全部 {len(multi)} 个多频算例 N = 8000", "")
    c.check(all("(2000)" in r[8].replace(" ", "") for r in rows),
            f"全部 {len(rows)} 个算例每频 2000", "")
    c.check(all(r[8].replace(" ", "").startswith("2000") for r in single),
            f"{len(single)} 个单频算例 N = 2000（故不能写成『每个算例 8000』）", "")
    c.check("each multi-frequency case here rests on $8000$" in txt
            and "$2000$ per frequency" in txt,
            "正文限定为『每个多频算例 8000、每频 2000』", "")
    c.check("Each case reported here rests on $8000$" not in txt,
            "正文不再有『每个算例 8000』的旧说法", "")

    # ── 4. 4.4 节"其余基线 TL 均超过 2.6 dB" ↔ xlsx ──────────────
    c.section("4. 4.4 节基线 TL 门槛 ↔ 精度 xlsx")
    xl = paths.xlsx_path("4.4")
    tls = {name: M.xlsx_case(xl, no)["Overall"]["tl"]
           for name, no in (("DeepONet", 16), ("KNO", 18), ("CNO", 19))}
    fno = M.xlsx_case(xl, 17)["Overall"]["tl"]
    for name, v in tls.items():
        c.check(v > 2.6, f"矩形 R1 {name} 平均 TL > 2.6 dB", f"`{v:.3f}`")
    c.check(fno < 2.6, "FNO 不在此列（正文单独给出 1.305 dB）", f"`{fno:.3f}`")
    c.check("exceed $2.6$" in txt, "正文门槛字面量 2.6", "")
    return c


if __name__ == "__main__":
    sys.exit(run().finish())
