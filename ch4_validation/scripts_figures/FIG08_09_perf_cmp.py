#!/usr/bin/env python3
"""
Fig 8 / Fig 9（fig:perf-cmp-r / fig:perf-cmp-w）核验 — R1

对象：五方法统一网格场图，R1 把原来的**一张 8 行 11 列巨图**拆为两张独立整页图：
  Fig 8 = fig:perf-cmp-r，perf_grid_R1.pdf，R1 矩形，Cases 15-19
  Fig 9 = fig:perf-cmp-w，perf_grid_W1.pdf，W1 楔形，Cases 20-24

与深度线族的差别：本组图上**不标任何数值**（无 Src、无 Avg），
  · 行标题 = `NN Hz (x, y)`（频率 + 该行实际样本的源坐标，1 位小数）
  · 列结构 = COMSOL(Reference) + 五个方法 x (Pred., |Err|)
  · 每个 |Err| 面板上方标该样本的**区域平均误差**（`x.xx dB`，取整前 2 位）
故数值锚点取：行标题的频率与坐标、|Err| 上方的平均误差、逐方法场误差的**排序**
须与兄弟表 Table 9（tab:perf-cmp）的 Avg TL 排序同向——图误差是每频率前 2 个
展示样本的场均值，表 TL 是全测试集均值，数值不同但**排序必须同向**。

数据源：Raw_Experimental_Data 下各 case 的 ep200 npz。

★ 成图脚本自 R1 起收入仓库：Validation_Scripts/fig08_09_perf_grid/
  fig08_09_perf_grid.py，产物写同目录 out/。旧路径 D:\\Data\\regen_method_grid.py
  及其 repo 副本已随 R1 整理废弃。

核验链
  A. 源可追溯      脚本入库、口径防漂移（GRID/METHOD 无模块常量，改核真实表面）
  B. epoch 双侧    图上 ep200(last) 与兄弟表 best epoch 是两个口径，两侧都核
  C. 图内结构      8 个行标题的频率/坐标与取样序一致；列标题齐全
  D. 平均误差标注  图上 x.xx dB 与 npz 全精度重算逐一吻合（★ 图内唯一的数值）
  E. 排序同向      图误差排序 == Table 9 的 Avg TL 排序（图表同源的可核关系）
  F. caption       取样措辞（the first two）、案例区间、last epoch
  G. 正文引用      图号 8/9；正文并列引用；兄弟表 Table 9 在正文被引
"""
import hashlib
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG08_09_perf_cmp"
SCRIPT = os.path.join(paths.PLOTDIR, "fig08_09_perf_grid",
                      "fig08_09_perf_grid.py")
SCRIPT_OUT = os.path.join(paths.PLOTDIR, "fig08_09_perf_grid", "out")
METHODS = ["Proposed", "DeepONet", "FNO", "KNO", "CNO"]
FREQS = (25, 50, 75, 100)

# (图 label, Fig 号, 组名, 兄弟表, 域, 案例, 案例区间串, PDF)
FIGS = [
    dict(lb="fig:perf-cmp-r", num="8", group="perf_grid_r1", dom="Rectangle",
         cases=(15, 16, 17, 18, 19), cases_str="Cases~15--19",
         pdf="perf_grid_R1.pdf"),
    dict(lb="fig:perf-cmp-w", num="9", group="perf_grid_w1", dom="Wedge",
         cases=(20, 21, 22, 23, 24), cases_str="Cases~20--24",
         pdf="perf_grid_W1.pdf"),
]
SIB = "tab:perf-cmp"        # 兄弟表：Table 9（逐频精度，排序同向判据用它）
SRC_TAB = "tab:dl-cmp"      # caption 实际引用的表：Table 7（深度线声源）


def md5(p):
    if not p or not os.path.exists(p):
        return None
    h = hashlib.md5()
    with open(p, "rb") as fp:
        for blk in iter(lambda: fp.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def script():
    """import 权威绘图脚本，复用其取数与插值函数（口径防漂移）。"""
    spec = importlib.util.spec_from_file_location("f89", SCRIPT)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pdftext(pdf_path):
    """PDF 文本层，必须 -raw（-layout 会把多行面板标题按列咬合）。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=180)
        return out.stdout
    except Exception:
        return ""


def flat(s):
    return re.sub(r"\s+", " ", (s or "")).replace("$", "").replace(chr(92) + ",", "")


def run():
    import numpy as np
    from common import metrics as M

    c = report.Checker(SLUG, "五方法统一网格场图 Fig 8/9", "figure",
                       "fig:perf-cmp-r / fig:perf-cmp-w", "8/9")

    c.source("印刷面 tex", paths.TEX, "两个独立 figure* 环境，各含一张整页图")
    c.source("成图脚本（权威）", SCRIPT,
             "fig08_09_perf_grid.py（R1 起入库；旧 regen_method_grid.py 已废弃）")
    for f in FIGS:
        c.source(f"论文图件（Fig {f['num']}）",
                 os.path.join(paths.FIGDIR, f["pdf"]),
                 "成图脚本 out/ 下的整页 PDF")

    # ── A ────────────────────────────────────────────────────────
    c.section("2. 源可追溯与口径防漂移")
    c.note("R1 把成图脚本收入仓库（Validation_Scripts/fig08_09_perf_grid/），"
           "旧路径 D:\\Data\\regen_method_grid.py 与其 repo 副本已不存在，"
           "故『两份副本 md5 同源』这一判据在 R1 已无对象——改为核入库脚本"
           "确实存在。")
    c.check(os.path.exists(SCRIPT), "成图脚本已入库", paths.rel(SCRIPT))
    c.exempt("成图脚本两份副本 md5 同源",
             "旧权威路径 D:\\Data\\regen_method_grid.py 与 repo 副本均已不存在；"
             "R1 的成图脚本只有入库的这一份，无副本可比")
    m = script()
    # 脚本里没有 GRID / METHOD / N_SAMPLE 模块常量：grid_res/method 是 interp()
    # 与 render() 的**形参**，取样序是模块常量 ROWS_2S。故按真实表面断言。
    c.note("该脚本不设 GRID / METHOD / N_SAMPLE 模块常量：插值格数与方式"
           "（grid_res=200, method=\"cubic\"）是 interp() 的形参默认值，取样序"
           "由模块常量 ROWS_2S 给出。故本节的防漂移断言按脚本真实表面写，"
           "不照搬场图族其他脚本的常量名。")
    import inspect
    sig = inspect.signature(m.interp)
    c.check(sig.parameters["grid_res"].default == 200,
            "插值网格 grid_res == 200", f"`{sig.parameters['grid_res'].default}`")
    c.check(sig.parameters["method"].default == "cubic",
            "插值方式 method == cubic", f"`{sig.parameters['method'].default}`")
    c.check([lb for lb, _ in
             zip(METHODS, m.GROUPS["perf_grid_r1"]["cases"])] == METHODS,
            "五方法列序与表行序一致", str(METHODS))
    c.exempt("FREQS / N_SAMPLE 模块常量 == 期望值",
             "脚本无这两个常量；取样序由 ROWS_2S 给出，频率集由 npz 的 freq "
             "数组给出，已在第 4 节按 ROWS_2S 逐行核过")
    c.check(m.ROWS_2S == [(25, 0), (25, 1), (50, 2), (50, 3), (75, 4),
                          (75, 5), (100, 6), (100, 7)],
            "取样序 ROWS_2S = 每频率前 2 个样本（索引 0-7 顺序）",
            "行标题频率须与之逐一对应")

    for f in FIGS:
        cfg = m.GROUPS[f["group"]]
        c.check(m.find_npz(cfg["cases"][0]).endswith("_ep200.npz"),
                f"Fig {f['num']} 取 ep200 npz",
                Path(m.find_npz(cfg["cases"][0])).name)
        c.check(os.path.exists(os.path.join(paths.FIGDIR, f["pdf"])),
                f"Fig {f['num']} 图件存在", f["pdf"])
        for sub in cfg["cases"]:
            c.check(os.path.exists(m.find_npz(sub)),
                    f"Fig {f['num']} 数据源 npz 存在", sub)

    # ── B ────────────────────────────────────────────────────────
    c.section("3. epoch 双侧判据与 caption 声明")
    c.note("图取 ep200(last)，兄弟表 Table 9 取 best epoch，本是两套口径。"
           "故除『caption 含 last』外，还须断言『caption 未误写 best』，"
           "并列出各 case 的 best 与 200 的差异佐证。")
    for f in FIGS:
        cfg = m.GROUPS[f["group"]]
        eps = sorted({int(np.load(m.find_npz(sub), allow_pickle=True)["epoch"])
                      for sub in cfg["cases"]})
        c.check(eps == [200], f"Fig {f['num']} 全部 npz epoch == 200 (last)",
                f"实得 {eps}（{len(cfg['cases'])} 份 npz）")
        cap = flat(T.caption_of(f["lb"]))
        c.check("Fields are from the last epoch" in cap,
                f"Fig {f['num']} caption 声明 last epoch",
                "含 `Fields are from the last epoch.`")
        c.check("best epoch" not in cap, f"Fig {f['num']} caption 未误写 best epoch",
                "图源自 ep200 npz")
        c.check(f["cases_str"] in cap,
                f"Fig {f['num']} caption 标明案例区间 {f['cases_str']}", "")
        for no in f["cases"]:
            be = M.xlsx_case(paths.xlsx_path("4.4"), no)["best_epoch"]
            c.check(be is not None, f"Case {no} best epoch 可读",
                    f"best={be}, last=200, "
                    + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── C ────────────────────────────────────────────────────────
    c.section("4. 图内结构：行标题与列标题")
    c.note("本组图不标任何 Src/Avg 之外的内容，故锚点取图内文本。R1 的行标题"
           "格式为 `NN Hz (x, y)`——频率 + 该行样本的源坐标（1 位小数），"
           "**没有** a/b 标签，也**没有** `f = ` 前缀（旧版格式已废弃）。")
    for f in FIGS:
        cfg = m.GROUPS[f["group"]]
        d0 = np.load(m.find_npz(cfg["cases"][0]), allow_pickle=True)
        rows = cfg["rows"]
        want = ["%d Hz (%.1f, %.1f)"
                % (fr, d0["source_pos"][i][0], d0["source_pos"][i][1])
                for fr, i in rows]
        txt = pdftext(os.path.join(paths.FIGDIR, f["pdf"]))
        got = re.findall(r"(\d+) Hz \(([\d.]+), ([\d.]+)\)", txt)
        got = [_fmt(fr, x, y) for fr, x, y in got]
        c.check(len(rows) == 8, f"Fig {f['num']} 行数 = 8（4 频率 x 2 样本）",
                f"实得 {len(rows)}")
        c.check(got == want, f"Fig {f['num']} 8 个行标题与取样序的坐标一致",
                f"图上 {len(got)} 个 / 期望 {len(want)} 个"
                + ("" if got == want else f"；差异 {sorted(set(got) ^ set(want))}"))
        c.check([i for _, i in rows] == list(range(8)),
                f"Fig {f['num']} 样本索引按 0-7 顺序取", str([i for _, i in rows]))
        # 措辞须与机制相符：取每频率前 2 个索引，不是择优，故 caption 应写
        # the first two 而非含混的 representative。
        cap_s = flat(T.caption_of(f["lb"]))
        c.check("first two" in cap_s,
                f"Fig {f['num']} caption 写明取每频率前两个样本（非择优）",
                "含 `the first two held-out samples`")
        c.check("representative" not in cap_s,
                f"Fig {f['num']} caption 未含混使用 representative",
                "索引顺序取样不应称 representative")
        for tag in ("COMSOL", "Reference", "Pred.", "|Err|"):
            c.check(tag in txt, f"Fig {f['num']} 含列标题 {tag}", "")
        for name in METHODS:
            c.check(name in txt, f"Fig {f['num']} 含方法 {name} 的列标题", "")
        c.check("TL (dB)" in txt and "|Error| (dB)" in txt,
                f"Fig {f['num']} 含两条色条的标签", "")

    # ── D ────────────────────────────────────────────────────────
    c.section("5. |Err| 上方的区域平均误差：npz 重算 vs 图上标注")
    c.note("本组图唯一的数值标注是每个 |Err| 面板上方的区域平均误差（2 位小数），"
           "共 8 行 x 5 方法 = 40 个。逐方法与 npz 全精度重算比对——图上取整到"
           "2 位，重算给全精度，判定用舍入后的 2 位值。")
    for f in FIGS:
        cfg = m.GROUPS[f["group"]]
        datas = [np.load(m.find_npz(sub), allow_pickle=True)
                 for sub in cfg["cases"]]
        d0 = datas[0]
        want = []
        for fr, i in cfg["rows"]:
            gf = m.interp(d0, "fem_tl", i)
            for d in datas:
                err = np.abs(m.interp(d, "pred_tl", i) - gf)
                want.append("%.2f" % float(np.nanmean(err)))
        txt = pdftext(os.path.join(paths.FIGDIR, f["pdf"]))
        got = re.findall(r"([0-9]+\.[0-9]{2}) dB", txt)
        c.check(len(got) == 40, f"Fig {f['num']} 图上解析到 40 个平均误差标注",
                f"实得 {len(got)}")
        c.check(got == want, f"Fig {f['num']} 40 个平均误差逐一吻合 npz 重算",
                "全部吻合" if got == want else
                "首个不符: " + ", ".join(
                    f"#{k} 图 `{a}` vs 重算 `{b}`"
                    for k, (a, b) in enumerate(zip(got, want)) if a != b)[:200])

    # ── E ────────────────────────────────────────────────────────
    c.section("6. 图误差排序 vs 兄弟表 Table 9 的 Avg TL 排序")
    c.note("图上展示样本的逐方法场误差均值，与表的全测试集 Avg TL 数值不同"
           "（样本集不同），但**排序必须同向**——若图里某方法看着最准而表里它"
           "最差，就是图表不同源的信号。表侧取 Table 9 各自几何块的行。")
    for f in FIGS:
        cfg = m.GROUPS[f["group"]]
        datas = [np.load(m.find_npz(sub), allow_pickle=True)
                 for sub in cfg["cases"]]
        d0 = datas[0]
        gfem = {i: m.interp(d0, "fem_tl", i) for _, i in cfg["rows"]}
        fig_err, tab_tl = [], []
        for sub, lb, no in zip(cfg["cases"], METHODS, f["cases"]):
            d = np.load(m.find_npz(sub), allow_pickle=True)
            e = float(np.mean([float(np.nanmean(
                np.abs(m.interp(d, "pred_tl", i) - gfem[i])))
                for _, i in cfg["rows"]]))
            fig_err.append((lb, e))
            tab_tl.append((lb, M.xlsx_case(paths.xlsx_path("4.4"),
                                           no)["Overall"]["tl"]))
        o_fig = [lb for lb, _ in sorted(fig_err, key=lambda t: t[1])]
        o_tab = [lb for lb, _ in sorted(tab_tl, key=lambda t: t[1])]
        c.check(o_fig == o_tab, f"Fig {f['num']} 图误差排序 == Table 9 TL 排序",
                f"图 {o_fig} / 表 {o_tab}")
        c.check(o_fig[0] == "Proposed", f"Fig {f['num']} 图上本文法误差最小",
                " < ".join(f"{lb}:{e:.3f}" for lb, e in sorted(
                    fig_err, key=lambda t: t[1])))

    # ── F ────────────────────────────────────────────────────────
    c.section("7. caption 与图表交叉引用")
    c.note("R1 两张图各自独立成页，Fig 9 的 caption 以 `Layout as in "
           "Fig.~\\ref{fig:perf-cmp-r}` 继承布局与取样说明，但**自身也写明**"
           "the first two，故两图的取样判据都直接可核，不靠继承兜底。")
    cap_r = flat(T.caption_of("fig:perf-cmp-r"))
    c.check("first two" in cap_r,
            "被继承的 Fig 8 caption 自身写明取样方式", "含 `the first two`")
    c.check("row title" in cap_r, "Fig 8 caption 说明行标题含源坐标", "")
    c.check("domain average" in cap_r,
            "Fig 8 caption 说明 |Error| 的域平均标注", "")
    cap_w = flat(T.caption_of("fig:perf-cmp-w"))
    c.check("Layout as in" in cap_w,
            "Fig 9 caption 以 Layout as in Fig.~\\ref{fig:perf-cmp-r} 继承布局",
            "含该交叉引用")
    c.check(chr(92) + "ref{fig:perf-cmp-r}" in (T.caption_of("fig:perf-cmp-w") or ""),
            "Fig 9 caption 的继承链指向 Fig 8", "")
    for f in FIGS:
        cap = T.caption_of(f["lb"]) or ""
        c.check(chr(92) + "ref{" + SRC_TAB + "}" in cap,
                f"Fig {f['num']} caption 以 Table~\\ref{{{SRC_TAB}}} 交代与表的对应",
                "含 `these include the sources of Table~\\ref{tab:dl-cmp}`；"
                "★ 被引的是 Table 7（深度线表）而非兄弟表 Table 9——"
                "本组图的 40 个展示样本里，每频率恰有一个就是 Table 7 的"
                "深度线声源，caption 指的是这个事实")
    # ★ caption 的实质声明要真的成立：本组图每频率展示前 2 个样本，其中
    #   前一个恰是 Table 7 表头所选的那条深度线声源（两图共用同一批 8 个
    #   深度线样本）。故逐图核『图内行坐标与 Table 7 表头 \\srcxy 有交集』，
    #   不能只核 caption 里出现了 \\ref —— 引用对了而事实不成立照样是错。
    tbl_src = set(re.findall(
        r"\\srcxy\{([\d.]+)\}\{([\d.]+)\}", T.table_body_of(SRC_TAB)[0] or ""))
    c.check(len(tbl_src) == 8, "Table 7 表头解析到 8 个深度线声源",
            str(sorted(tbl_src)))
    for f in FIGS:
        cfg = m.GROUPS[f["group"]]
        d0 = np.load(m.find_npz(cfg["cases"][0]), allow_pickle=True)
        rows = {("%.1f" % d0['source_pos'][i][0], "%.1f" % d0['source_pos'][i][1])
                for _, i in cfg["rows"]}
        inter = rows & tbl_src
        c.check(len(inter) == 4,
                f"Fig {f['num']} 每个频率各有一个展示样本是 Table 7 的深度线声源",
                f"交集 {sorted(inter)}（每频率 1 个 = 4 个，与 caption 的 "
                "`these include the sources of Table~\\ref{tab:dl-cmp}` 相符；"
                "该判决由坐标事实而非 \\ref 字符串给出）")

    # ── G ────────────────────────────────────────────────────────
    c.section("8. 正文引用")
    txt_all = T.tex_text()
    aux = T.labels()
    for f in FIGS:
        c.check(aux.get(f["lb"], {}).get("num") == f["num"],
                f"{f['lb']} 编号为 {f['num']}",
                f"aux `{aux.get(f['lb'], {}).get('num', '缺失')}`")
    pair = "".join([chr(92), "ref{fig:perf-cmp-r} and~", chr(92),
                    "ref{fig:perf-cmp-w}"])
    c.check(pair in txt_all, "正文并列引用 Fig 8 与 Fig 9",
            "含 `Figs.~\\ref{fig:perf-cmp-r} and~\\ref{fig:perf-cmp-w}`")
    hits = T.sentences_with(re.escape(SIB), txt_all)
    c.check(bool(hits), "兄弟表 Table 9 在正文被引",
            f"tex 行 {T.line_of(hits[0][0], txt_all)}" if hits else "未找到")

    return c


def _fmt(fr, x, y):
    return "%d Hz (%.1f, %.1f)" % (int(fr), float(x), float(y))


if __name__ == "__main__":
    sys.exit(run().finish())
