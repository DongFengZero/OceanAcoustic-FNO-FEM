"""
TS1_ideal_depthline.py — Supplementary Table S1（tab:S1）核验
=============================================================
对象：解析解深度线 TL-MAE @ y=44.7 m，R0 (Case 1) / W0 (Case 2)，逐频 TL + Src。
      本表原为正文 Table 5；因 Fig. 3 已显示同一批样本，R1 定稿把它移入补充材料
      OE_supplementary.tex，正文 4.2 节与 Fig. 3 图题以 `Table~S1` 指向它。

★ 与 Table 4 的关键差别：本表**不来自 xlsx**。
  xlsx 第 2 工作表『深度线误差』只记了 100Hz 一个代表样本（R0 源位 122.33/91.5），
  与本表 100Hz 的 (23,54) 不是同一样本——那是另一套取样，不能当第二渠道。
  本表的源是成图脚本 `fig03_ideal/_ideal_core.py` 从 ep200 npz 的提取：
  每频率取 y=Y_LINE 行 MAE 最小的样本，故 caption 标注 last epoch。

核验链
  A. 源可追溯    npz 存在；成图脚本读的数组与 Raw_ 下 npz 逐元素相同
  B. 口径防漂移   从成图脚本源码解析 GRID/METHOD/Y_LINE，须与本脚本复刻值一致
  C. 值复现      独立复刻 pick_sample，重算 MAE 与源位，与印刷值比对
  D. 位数一致     TL 全 3 位；Src 全 1 位小数（与图/场图统一口径）
  E. caption 自洽 caption 写的 y=44.7 与脚本常量一致；指向正文 Fig. 3 的编号正确
  F. 跨文件引用   正文 4.2 节与 Fig. 3 图题指向 `Table~S1`；正文不再有 tab:ideal-depthline
  G. 文段引用     4.2 正文关于深度线的趋势断言（楔形 75/100Hz 误差最大）
"""
import io
import os
import re

import numpy as np

import _boot  # noqa: F401
from common import paths, registry, report, texparse as T

SLUG = "TS1_ideal_depthline"
REC = registry.by_slug(SLUG)
LABEL = REC["label"]                                  # tab:S1
SUPP = os.path.join(os.path.dirname(paths.TEX), "OE_supplementary.tex")
CASES = {1: ("R0 (rect.)", "Case01_R0"), 2: ("W0 (wedge)", "Case02_W0")}
FREQS = [25, 50, 75, 100]

# ── 复刻成图脚本的提取口径（B 段会核对是否与脚本源码一致）──
GRID = 220
METHOD = "cubic"
Y_LINE = 44.7


def grids(data, i):
    """复刻成图脚本 grids()：cubic 插值到 GRID×GRID，楔形域外置 NaN，再按 vmin/vmax 截断。

    截断顺序很重要：先 NaN 掉域外，再 clip；反过来会把域外的极值拉进有效区。
    """
    from scipy.interpolate import griddata
    xc, yc = data["x_coords"], data["y_coords"]
    Lx, Ly = float(data["Lx_dom"]), float(data["Ly_dom"])
    vmin, vmax = float(data["vmin"]), float(data["vmax"])
    gx = np.linspace(0, Lx, GRID)
    gy = np.linspace(0, Ly, GRID)
    GX, GY = np.meshgrid(gx, gy)
    gp = griddata((xc, yc), data["pred_tl"][i], (GX, GY), METHOD)
    gf = griddata((xc, yc), data["fem_tl"][i], (GX, GY), METHOD)
    if bool(data["is_wedge"]):
        outside = GY > (Ly / Lx) * GX
        gp[outside] = np.nan
        gf[outside] = np.nan
    return gx, gy, np.clip(gp, vmin, vmax), np.clip(gf, vmin, vmax)


def pick_sample(data, freq):
    """复刻成图脚本 pick_sample()：该频率下 y=Y_LINE 行 MAE 最小的样本。

    返回 (idx, mae, (src_x, src_y), y_actual)。
    """
    freqs = [int(round(f)) for f in data["freq"]]
    cand = [i for i in range(len(freqs)) if freqs[i] == freq]
    best = None
    for i in cand:
        gx, gy, gp, gf = grids(data, i)
        r = int(np.argmin(np.abs(gy - Y_LINE)))
        fem = gf[r]
        ok = np.isfinite(fem) & np.isfinite(gp[r])
        if ok.sum() < 20:
            continue
        mae = float(np.mean(np.abs((gp[r] - fem)[ok])))
        if best is None or mae < best[1]:
            best = (i, mae, tuple(data["source_pos"][i]), float(gy[r]))
    return best


def run():
    c = report.Checker(SLUG, REC["desc"], "table", LABEL, "S1")

    ps = paths.plot_script(REC["plot"])
    core = os.path.join(os.path.dirname(ps), "_ideal_core.py")
    ps_const = core if os.path.exists(core) else ps
    c.source("补充材料 tex", SUPP, f"`\\label{{{LABEL}}}` 所在 table 环境（Supplementary Material）")
    c.source("正文 tex", paths.TEX, "4.2 节与 Fig. 3 图题对 Table~S1 的指向；趋势断言")
    c.source("提取口径 脚本", ps, "每频率取 y=44.7m 行 MAE 最小样本；成图与表值同一算法")
    for no, (_, cd) in CASES.items():
        c.source(f"数据源 npz (Case {no})", paths.npz_path(no), "ep200 TL 原始数据（last epoch）")

    supp = io.open(SUPP, encoding="utf8").read()
    main = T.tex_text()
    aux = T.labels()

    # ── A. 源可追溯 ──────────────────────────────────────────────
    c.section("2. 源可追溯性")
    c.check(os.path.exists(SUPP), "补充材料 tex 存在", paths.rel(SUPP))
    c.check(os.path.exists(ps), "成图脚本存在", paths.rel(ps))
    npz = {}
    for no, (_, cd) in CASES.items():
        p = paths.npz_path(no)
        npz[no] = p
        c.check(p is not None and os.path.exists(p), f"Case {no} npz 存在", paths.rel(p))

    c.note("成图脚本默认读公开数据 `Raw_Experimental_Data/4.2_Validation/`，与注册表同一份；"
           "此处断言它实际加载的数组与注册 npz 逐元素相同，确保图与表的数据基础一致。")
    import importlib.util
    os.environ.setdefault("CH4_RAWROOT", paths._RAWROOT)
    _sp = importlib.util.spec_from_file_location("ideal_core_ts1", os.path.join(os.path.dirname(ps), "_ideal_core.py"))
    _core = importlib.util.module_from_spec(_sp)
    _sp.loader.exec_module(_core)
    for no, (_, cd) in CASES.items():
        gen = _core.load(cd)
        reg = np.load(npz[no], allow_pickle=True)
        same = all(np.array_equal(gen[k], reg[k]) for k in ("pred_tl", "fem_tl", "source_pos", "freq"))
        c.check(same and _core.CASE_ROOT is None, f"Case {no} 成图脚本读取的即公开 npz",
                "逐元素相同" + ("" if _core.CASE_ROOT is None else f"；CH4_IDEAL_ROOT={_core.CASE_ROOT}"))

    env = T.table_env(LABEL, supp)
    c.check(env is not None, "补充材料含 `\\label{tab:S1}` 的 table 环境", "")
    rows = T.data_rows(env or "", ncol=10)
    c.check(len(rows) == 2, "tex 数据行数 = 2", f"实得 {len(rows)}")
    printed = {int(r[0]): r for r in rows}
    c.check(set(printed) == set(CASES), "tex 行 No. 覆盖 Case 1-2", str(sorted(printed)))
    c.check(supp.count("\\label{tab:S1}") == 1 and "\\label{tab:ideal-depthline}" not in main,
            "Table S1 只在补充材料出现一次，正文不再含 tab:ideal-depthline", "")

    # ── B. 口径防漂移 ────────────────────────────────────────────
    c.section("3. 提取口径与成图脚本一致（防漂移）")
    c.note("本脚本复刻了成图脚本的提取算法。若成图脚本的常量被改动而这里没跟上，"
           "表值就会与图脱钩，故直接从脚本源码解析常量做断言。")
    src = open(ps_const, encoding="utf-8", errors="ignore").read()
    for name, mine, pat in (("GRID", GRID, r"^GRID\s*=\s*(\d+)"),
                            ("METHOD", METHOD, r'^METHOD\s*=\s*"([^"]+)"'),
                            ("Y_LINE", Y_LINE, r"^Y_LINE\s*=\s*([0-9.]+)")):
        m = re.search(pat, src, re.M)
        got = m.group(1) if m else None
        ok = got is not None and str(mine) == got
        c.check(ok, f"常量 {name}",
                f"`{os.path.basename(ps_const)}` `{got}` / 复刻 `{mine}`")

    # ── C. 值复现 ────────────────────────────────────────────────
    c.section("4. 从 npz 独立复现（MAE 与源位 vs 印刷值）")
    c.note("列序：No., Dataset, 25Hz(TL,Src), 50Hz, 75Hz, 100Hz。"
           "Src 印刷为 1 位小数对，与图面板标题及场图同口径，故按 1 位比对。")
    mae_tab = {}
    for no, (dsname, _) in CASES.items():
        if no not in printed:
            continue
        data = np.load(npz[no], allow_pickle=True)
        c.check(printed[no][1].strip() == dsname, f"Case {no} Dataset 名",
                f"tex `{printed[no][1].strip()}`")
        mae_tab[no] = {}
        for k, f in enumerate(FREQS):
            got = pick_sample(data, f)
            if got is None:
                c.check(False, f"Case {no} {f}Hz 可取样", "候选样本不足 20 有效点")
                continue
            idx, mae, (sx, sy), yv = got
            mae_tab[no][f] = mae
            cell_tl = printed[no][2 + k * 2]
            cell_src = printed[no][3 + k * 2]
            c.eq(f"Case {no} {f}Hz TL-MAE", mae, cell_tl)
            m = re.search(r"\(\s*(-?[\d.]+)\s*,\s*(-?[\d.]+)\s*\)", cell_src)
            if m:
                px, py = float(m.group(1)), float(m.group(2))
                ok = (round(sx, 1) == px) and (round(sy, 1) == py)
                c.check(ok, f"Case {no} {f}Hz Src",
                        f"npz 样本#{idx} `({sx:.6f},{sy:.6f})` → "
                        f"`({round(sx,1):.1f},{round(sy,1):.1f})` / 印刷 `({px},{py})`")
            else:
                c.check(False, f"Case {no} {f}Hz Src 可解析", f"印刷 `{cell_src}`")
            c.check(abs(yv - Y_LINE) <= 0.5, f"Case {no} {f}Hz 取样行贴近 y={Y_LINE}",
                    f"实际 y=`{yv:.2f}` m")

    # ── D. 位数一致 ──────────────────────────────────────────────
    c.section("5. 同表小数位一致性")
    bad = []
    for no in printed:
        for k in range(4):
            v = printed[no][2 + k * 2]
            if not re.fullmatch(r"\d+\.\d{3}", v):
                bad.append(f"Case {no} {FREQS[k]}Hz TL `{v}`")
            s = printed[no][3 + k * 2]
            if not re.search(r"\(\s*-?\d+\.\d\s*,\s*-?\d+\.\d\s*\)", s):
                bad.append(f"Case {no} {FREQS[k]}Hz Src `{s}`")
    c.check(not bad, "8 个 TL 单元格均 3 位小数、8 个 Src 均 1 位小数对",
            "全部合规" if not bad else "；".join(bad))

    # ── E. caption 自洽 ──────────────────────────────────────────
    c.section("6. caption 与口径自洽")
    cap = re.sub(r"\s+", " ", T.caption_of(LABEL, supp) or "")
    c.check(f"y={Y_LINE}" in cap.replace("$", "").replace("\\,m", ""),
            "caption 标注的深度线位置 = 脚本 Y_LINE", f"caption 含 `y={Y_LINE}`")
    c.check("last epoch" in cap, "caption 声明 last epoch", "本表源自 ep200 npz，非 best epoch")
    c.check("best-matching" in cap, "caption 说明取样规则", "每频率取最匹配样本")
    n_fig = aux.get("fig:ideal", {}).get("num")
    n_sec = aux.get("sec:ideal", {}).get("num")
    c.check(n_fig is not None and f"Fig.~{n_fig} of the main text" in cap,
            f"caption 指向正文 Fig.~{n_fig}（fig:ideal 的实际编号）", f"aux `{n_fig}`")
    c.check(n_sec is not None and f"Sec.~{n_sec} of the main text" in cap,
            f"caption 指向正文 Sec.~{n_sec}（sec:ideal 的实际编号）", f"aux `{n_sec}`")

    # ── F. 跨文件引用 ────────────────────────────────────────────
    c.section("7. 正文对 Table S1 的指向")
    c.note("正文不再排这张表，但 4.2 节与 Fig. 3 图题都要把读者指到补充材料；"
           "两处都写 `Table~S1 of the Supplementary Material`。")
    n_ref = main.count("Table~S1 of the Supplementary Material")
    c.check(n_ref >= 2, "正文至少两处写 `Table~S1 of the Supplementary Material`", f"实得 {n_ref}")
    fcap = T.caption_of("fig:ideal") or ""
    c.check("Table~S1" in fcap, "Fig. 3 图题指向 Table~S1", "")
    sec_txt = main[main.find("\\label{sec:ideal}"):main.find("\\label{sec:forward}")]
    c.check("Table~S1" in sec_txt, "4.2 节正文指向 Table~S1", "")
    c.check("Table~S1" in main[main.find("\\section*{Supplementary Material}"):],
            "正文『Supplementary Material』一节列出 Table~S1", "")

    # ── G. 文段引用 ──────────────────────────────────────────────
    c.section("8. 正文断言与表值一致（4.2 节）")
    c.note("4.2 正文未直接引用本表数字，只作趋势断言："
           "“The error is largest at 75 and 100 Hz on the wedge”。"
           "趋势断言同样须由表值支持，否则是无据之言。")
    if 2 in mae_tab and len(mae_tab[2]) == 4:
        order = sorted(FREQS, key=lambda f: mae_tab[2][f], reverse=True)
        c.check(set(order[:2]) == {75, 100},
                "楔形 W0 误差最大的两个频率 = 75/100Hz",
                "降序 " + " > ".join(f"{f}Hz({mae_tab[2][f]:.3f})" for f in order))
    hits = T.sentences_with(r"largest at \$75\$ and \$100\$", main)
    c.check(bool(hits), "正文该断言可定位",
            f"tex 行 {T.line_of(hits[0][0])}" if hits else "未找到")

    return c


if __name__ == "__main__":
    import sys
    sys.exit(run().finish())
