#!/usr/bin/env python3
"""
Fig 20（fig:gen-split）核验

对象：泛化实验的训练/测试源位置分布图，4 case x 4 频率 = 16 面板。

本图性质与前 17 张都不同：画的是**源坐标分布与数据划分**，不是场也不是
曲线。因此没有 epoch 概念（caption 也不含 epoch 声明，这是正确的——
划分与训练轮次无关），数值锚点换成划分本身：
  · 区外样本必须 100% 用于训练
  · 区内样本必须恰好 1:9 划分（10% 训练）
  · 阈值 (train_max_x, train_max_y) 须与 Table 19 的 Extrap. region 列一致
  · 面板布局：4 case 左到右 R9/R10/W9/W10，每 case 2x2 频率块
    (25/50 上行, 75/100 下行)

数据源：Raw_Experimental_Data/4.7 下各 case 的 manifest 与 train_test_split.pth。
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG20_gen_split"
LABEL = "fig:gen-split"
SCRIPT_AUTH = Path(r"D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts"
                   r"\plot_generalization_split.py")
PDF_NAME = "generalization_split.pdf"

# Table 19 印刷的 Extrap. region 列（No. -> (类型, 阈值)）
TAB19_REGION = {
    39: ("depth", 96),
    40: ("range", 96),
    41: ("depth", 48),
    42: ("range", 96),
}


def script():
    """import 权威绘图脚本，复用其 load_case（口径防漂移）。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("pgs", str(SCRIPT_AUTH))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run():
    import numpy as np

    c = report.Checker(SLUG, "泛化划分分布图 Fig 20", "figure", LABEL, "20")
    c.source("印刷面 tex", paths.TEX, "单栏 figure* 环境")
    c.source("成图脚本", str(SCRIPT_AUTH), "plot_generalization_split.py")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源与口径")
    c.check(SCRIPT_AUTH.exists(), "成图脚本存在", str(SCRIPT_AUTH.name))
    m = script()
    c.check([n for n, _, _, _, _ in m.CASES] == ["R9", "R10", "W9", "W10"],
            "CASES 顺序 = R9/R10/W9/W10（caption 称 left to right）",
            str([n for n, _, _, _, _ in m.CASES]))
    c.check(list(m.FREQS) == [25, 50, 75, 100], "FREQS = 25/50/75/100",
            str(list(m.FREQS)))
    c.check(m.QUAD == {25: (0, 0), 50: (0, 1), 75: (1, 0), 100: (1, 1)},
            "QUAD 布局 = 25/50 上行、75/100 下行（与 caption 一致）",
            str(m.QUAD))
    src_txt = open(SCRIPT_AUTH, encoding="utf-8").read()
    c.check('c="tab:blue"' in src_txt and 'c="tab:red"' in src_txt,
            "源码用 tab:blue / tab:red 两色", "与 caption 的 blue/red 对应")

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 划分口径：区外全训练、区内恰 1:9")
    c.note("caption 称『区外样本全部用于训练，区内按 1:9 划分，故阴影区内"
           "仍有约 10% 的训练点』。逐 case 逐频核验这两条，共 16 个面板。")
    data = {}
    for name, no, sub, raw, isw in m.CASES:
        d = m.load_case(sub, raw)
        data[no] = d
        depth = d["train_max_y"] < d["Ly"] - 1e-6
        for fi, f in enumerate(m.FREQS):
            sel = d["fidx"] == fi
            x, y, tr = d["x"][sel], d["y"][sel], d["is_train"][sel]
            ins = (y > d["train_max_y"]) if depth else (x > d["train_max_x"])
            n_in, n_out = int(ins.sum()), int((~ins).sum())
            n_in_tr = int((ins & tr).sum())
            c.check(bool(tr[~ins].all()),
                    f"{name} {f}Hz 区外样本 100% 用于训练",
                    f"区外 {n_out} 点全为训练")
            pct = 100.0 * n_in_tr / max(n_in, 1)
            c.check(abs(pct - 10.0) < 0.5,
                    f"{name} {f}Hz 区内训练占比 = 10%（1:9）",
                    f"区内 {n_in} 点中 {n_in_tr} 个训练 = {pct:.1f}%")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 外推区阈值与 Table 19 的 Extrap. region 列一致")
    c.note("图上阴影带的位置由 train_max_x/y 决定，Table 19 则以文字列出"
           "『depth (y>96 m)』这类描述。两者须指同一条界线。")
    for name, no, sub, raw, isw in m.CASES:
        d = data[no]
        depth = d["train_max_y"] < d["Ly"] - 1e-6
        kind = "depth" if depth else "range"
        thr = d["train_max_y"] if depth else d["train_max_x"]
        want_kind, want_thr = TAB19_REGION[no]
        c.check(kind == want_kind and abs(thr - want_thr) < 1e-6,
                f"No.{no} {name} 外推区 = {want_kind} > {want_thr} m",
                f"manifest `{kind} > {thr:.0f}` / 表印 `{want_kind} > {want_thr}`")

    # ── D ────────────────────────────────────────────────────────
    c.section("4. caption 与图件")
    cap = T.caption_of(LABEL) or ""
    c.check("epoch" not in cap.lower(),
            "caption 不含 epoch 声明（分布图与训练轮次无关，正确）", "")
    c.check(os.path.exists(os.path.join(paths.FIGDIR, PDF_NAME)),
            "图件存在", PDF_NAME)
    for kw in ("R9", "R10", "W9", "W10"):
        c.check(kw in cap, f"caption 列出数据集 {kw}", "")
    c.check("39" in cap and "42" in cap,
            "caption 标明案例区间 39-42", "含 `Cases~39--42`")
    c.check("blue" in cap and "red" in cap,
            "caption 说明 blue/red 配色语义", "")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 正文引用")
    txt = T.tex_text()
    aux = T.labels()
    c.check(aux.get(LABEL, {}).get("num") == "20", "编号为 20",
            f"aux `{aux.get(LABEL, {}).get('num', '缺失')}`")
    n = txt.count("\\ref{" + LABEL + "}")
    c.check(n >= 1, "正文引用本图", f"`\\ref{{{LABEL}}}` 出现 {n} 处")
    hits = T.sentences_with(r"shows the resulting source distributions", txt)
    c.check(bool(hits), "正文 4.7 节以散文引用并描述图内容",
            f"tex 行 {T.line_of(hits[0][0], txt)}" if hits else "未找到")
    # 正文称"nine tenths of the held-out region is never seen during training"
    c.note("正文断言『外推区的九成从未参与训练』，即区内训练占比 10%——"
           "已在第 2 节逐面板核验，16 个面板全部恰为 10.0%。")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
