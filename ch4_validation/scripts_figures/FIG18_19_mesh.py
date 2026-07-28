#!/usr/bin/env python3
"""
Fig 8/9（fig:res-rect-100 / fig:res-wedge-100）核验

对象：100 Hz 单频、方形域 TL 场图，各 3 个子图。
  Fig 8 = Case 6 (R4,128) / Case 7 (R5,256) / Case 8 (R6,512)   矩形
  Fig 9 = Case 12 (W4,128) / 13 (W5,256) / 14 (W6,512)          楔形

与 Fig 5/6/7 的差别：单频 npz 只含 2 个样本（多频 8 个）；三子图各带
subfloat label；对应 Tables 17/18 取 best epoch 而图取 ep200(last)，
Case 14 的 best=129 与 last=200 差 71 轮，是全章最大错位。

数据源一律取 Raw_Experimental_Data 下的 *__TL原始数据_ep200.npz。
"""
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report, texparse as T  # noqa: E402

SLUG = "FIG18_19_mesh"

SCRIPT_AUTH = Path(r"D:\Data\regen_results_bigfont.py")
SCRIPT_REPO = Path(r"D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts"
                   r"\regen_results_bigfont.py")

# (图 label, [(case, 数据集, 子图 label, PDF 文件名), ...])
FIGS = [
    ("fig:mesh-rect", [
        (33, "R4", "fig:mesh-rect-a", "Case33_R4_TL.pdf"),
        (34, "R7", "fig:mesh-rect-b", "Case34_R7_TL.pdf"),
        (35, "R8", "fig:mesh-rect-c", "Case35_R8_TL.pdf"),
    ]),
    ("fig:mesh-wedge", [
        (36, "W4", "fig:mesh-wedge-a", "Case36_W4_TL.pdf"),
        (37, "W7", "fig:mesh-wedge-b", "Case37_W7_TL.pdf"),
        (38, "W8", "fig:mesh-wedge-c", "Case38_W8_TL.pdf"),
    ]),
]
# 网格间距（m），用于核验 subfloat 题注与 Tables 17/18 的 Δ 列
DELTA = {33: "1.00", 34: "0.50", 35: "0.25",
         36: "1.00", 37: "0.50", 38: "0.25"}
# 数据集复用：Case 33 复用 Case 6 的 R4，Case 36 复用 Case 12 的 W4
REUSE = {33: 6, 36: 12}
CASES = [c for _, subs in FIGS for c, _, _, _ in subs]
PDF = {c: pdf for _, subs in FIGS for c, _, _, pdf in subs}


def md5(p):
    import hashlib
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def _pdftext(pdf_path):
    """PDF 文本层。必须用 -raw：-layout 会把 Ours 面板的两行标题
    按列交错咬合成 'OSurrcs:(T4L4(.5f=,2215.H9)z)'，正则一个都匹配不到。"""
    try:
        out = subprocess.run(["pdftotext", "-raw", str(pdf_path), "-"],
                             capture_output=True, text=True, timeout=120)
        return out.stdout
    except Exception:
        return ""


def pdf_avgs(pdf_path):
    return re.findall(r"Avg:([0-9.]+) dB", _pdftext(pdf_path))


def pdf_srcs(pdf_path):
    return re.findall(r"Src:\(([0-9.]+),([0-9.]+)\)", _pdftext(pdf_path))


def run():
    sys.path.insert(0, str(Path(__file__).parent))
    from _recompute_field import recompute, METHOD, GRID_RES

    c = report.Checker(SLUG, "网格独立性场图 Fig 18/19", "figure",
                       "fig:mesh-rect / fig:mesh-wedge", "18/19")

    c.source("印刷面 tex", paths.TEX, "两个并列 minipage，各 3 个 subfloat")
    c.source("成图脚本（权威）", str(SCRIPT_AUTH), "regen_results_bigfont.py")
    c.source("成图脚本 repo 副本", str(SCRIPT_REPO), "md5 应与权威副本相同")
    for c_no in CASES:
        c.source(f"数据源 npz (Case {c_no})", paths.npz_path(c_no),
                 "Raw_Experimental_Data，ep200")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 源可追溯性")
    for c_no in CASES:
        p = paths.npz_path(c_no)
        c.check(p and os.path.exists(p), f"Case {c_no} npz 存在",
                paths.rel(p) if p else "未找到")
    c.check(SCRIPT_AUTH.exists() and SCRIPT_REPO.exists(),
            "成图脚本两份副本均存在", "")
    same = SCRIPT_AUTH.exists() and SCRIPT_REPO.exists() and \
        md5(SCRIPT_AUTH) == md5(SCRIPT_REPO)
    c.check(same, "两份成图脚本 md5 同源",
            md5(SCRIPT_AUTH)[:16] + "…" if same else "不一致")
    for _, subs in FIGS:
        for c_no, _, _, pdf in subs:
            fp = os.path.join(paths.FIGDIR, pdf)
            c.check(os.path.exists(fp), f"图件 {pdf} 存在", paths.rel(fp))

    # ── B ────────────────────────────────────────────────────────
    c.section("2. 口径防漂移（从成图脚本源码读取）")
    c.note("重算层 _recompute_field 复刻 render() 的算法，其 method/grid_res "
           "必须与成图脚本签名默认值一致；脚本改了而重算没跟上，此处报错。")
    src_txt = SCRIPT_AUTH.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"def render\([^)]*method\s*=\s*\"(\w+)\"[^)]*"
                  r"grid_res\s*=\s*(\d+)", src_txt, re.S)
    c.check(m is not None, "render() 签名可解析", "")
    if m:
        c.check(m.group(1) == METHOD, "插值方法一致",
                f"脚本 `{m.group(1)}` / 重算层 `{METHOD}`")
        c.check(int(m.group(2)) == GRID_RES, "网格分辨率一致",
                f"脚本 `{m.group(2)}` / 重算层 `{GRID_RES}`")
    c.check(":.1f}" in src_txt and "Src:(" in src_txt,
            "Src 标注为 1 位小数（全章统一口径）",
            "源码含 `Src:({src[0]:.1f},...`")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. epoch 自证与 caption 声明")
    c.note("单频 case 的 best epoch 多不等于 200（Case 14 的 best=129），"
           "而图取 ep200，故 caption 必须声明 last epoch。")
    rec = {}
    for c_no in CASES:
        rec[c_no] = recompute(paths.npz_path(c_no))
        c.check(rec[c_no]["epoch"] == 200, f"Case {c_no} npz epoch=200",
                f"实得 {rec[c_no]['epoch']}")
    for label, _ in FIGS:
        cap = T.caption_of(label) or ""
        c.check("last epoch" in cap, f"{label} caption 声明 last epoch",
                "含 `Fields are from the last epoch.`")
        c.check("best epoch" not in cap, f"{label} caption 未误写 best epoch",
                "图源自 ep200 npz，非 best-epoch 评估")
        c.check("100" in cap, f"{label} caption 标明 100 Hz", "含 `f=100`")

    # ★ 双侧判据：Case 14 的 best=129 与 last=200 相差 71 轮，是全章最大错位，
    #   最能说明"图注写 last、表注写 best"不是措辞随意，而是两套评估口径。
    c.note("图取 ep200(last)，兄弟表 Tables 17/18 取 best epoch。二者本是不同轮。")
    from common import metrics as M
    for c_no in CASES:
        be = M.xlsx_case(paths.xlsx_path("4.6"), c_no)["best_epoch"]
        c.check(be is not None, f"Case {c_no} best epoch 可读",
                f"best={be}, last=200, "
                + ("相等（巧合）" if be == 200 else f"相差 {abs(200 - be)} 轮"))

    # ── D ────────────────────────────────────────────────────────
    c.section("4. 逐样本 Avg 误差：npz 重算 vs 图上标注")
    c.note("图上每个 Error 面板标 `Avg:x.xx dB`。从 Raw_Experimental_Data 的 "
           "npz 复刻算法重算，与 PDF 文本层标注逐个按 2 位小数比对——"
           "这是图件产自这批 npz 的直接证据。")
    for c_no in CASES:
        got = pdf_avgs(os.path.join(paths.FIGDIR, PDF[c_no]))
        want = [f"{s['avg_err']:.2f}" for s in rec[c_no]["samples"]]
        c.check(got == want, f"Case {c_no} 2 个 Avg 逐一吻合",
                f"PDF {got} / npz 重算 {want}")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. Src 坐标：npz 重算 vs 图上标注")
    c.note("坐标 1 位小数，与深度线图及 Tables 5/9-12 同口径。")
    for c_no in CASES:
        got = pdf_srcs(os.path.join(paths.FIGDIR, PDF[c_no]))
        want = [(f"{s['src'][0]:.1f}", f"{s['src'][1]:.1f}")
                for s in rec[c_no]["samples"]]
        c.check(got == want, f"Case {c_no} 2 组 Src 坐标吻合",
                f"PDF {got} / npz {want}")
        bad = [g for g in got if not (re.fullmatch(r"\d+\.\d", g[0])
                                      and re.fullmatch(r"\d+\.\d", g[1]))]
        c.check(not bad, f"Case {c_no} Src 均为 1 位小数",
                "全部合规" if not bad else str(bad))

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 图结构与子图引用")
    c.note("单频 npz 只含 2 个样本，故每子图 2 行；三个 subfloat 的 label "
           "须在 aux 注册且编号为 8a/8b/8c、9a/9b/9c。")
    aux = T.labels()
    for c_no in CASES:
        r = rec[c_no]
        c.check(r["n"] == 2, f"Case {c_no} npz 样本数 = 2",
                f"单频 case，实得 {r['n']}")
        c.check(all(int(s["freq"]) == 100 for s in r["samples"]),
                f"Case {c_no} 全部样本为 100 Hz",
                str(sorted(set(int(s['freq']) for s in r['samples']))))
    for label, subs in FIGS:
        c.check(label in aux, f"主图 label `{label}` 已注册",
                f"编号 `{aux.get(label, {}).get('num', '缺失')}`")
        for c_no, ds, sub_lb, _ in subs:
            c.check(sub_lb in aux, f"子图 label `{sub_lb}` 已注册",
                    f"编号 `{aux.get(sub_lb, {}).get('num', '缺失')}`")
            cap_env = T.tex_text()
            pos = cap_env.find("\\label{" + sub_lb + "}")
            seg = cap_env[max(0, pos - 300):pos]
            c.check(f"Case~{c_no}" in seg and ds in seg,
                    f"子图 `{sub_lb}` 标注 Case {c_no} / {ds}",
                    f"subfloat 题注含 `Case~{c_no}` 与 `{ds}`")

    # ── G ────────────────────────────────────────────────────────
    c.section("7. 网格独立性：细化下误差保持同量级")
    c.note("★ 本组的论点是网格无关性，判据与场图族相反：不要求单调，而要求"
           "三种网格间距下误差**保持同一量级**（网格加密 4 倍、节点数增约 16 "
           "倍，若误差随之爆掉就说明模型依赖特定离散）。caption 已声明这是"
           "个别样本的 last-round 结果，故不与表的均值趋势强行对齐。")
    for label, subs in FIGS:
        nos = [c_no for c_no, _, _, _ in subs]
        avgs = [max(s["avg_err"] for s in rec[n]["samples"]) for n in nos]
        lo, hi = min(avgs), max(avgs)
        c.check(hi / lo < 3.0,
                f"{label} 三种 Δ 下图误差同量级（极差 < 3x）",
                " / ".join(f"Δ={DELTA[n]}m:{a:.2f}" for n, a in zip(nos, avgs))
                + f" → {hi / lo:.2f}x")
        c.check(hi < 1.0,
                f"{label} 三种 Δ 下图误差均 < 1 dB",
                f"最大 `{hi:.2f}` dB")

    # ── H ────────────────────────────────────────────────────────
    c.section("8. 引用方式：经 Tables 17/18 的 Fig. 列逐行引用")
    c.note("★ 本组的被引方式与前几组都不同：既非散文区间引用，也非单点引用，"
           "而是由兄弟表每一行的 Fig. 列指向自己的子图 "
           "（`\\ref{fig:mesh-rect}\\subref{fig:mesh-rect-a}` 等），"
           "故须逐行核对『第 N 行的子图引用确指第 N 个 Δ』，错配读者会看错图。")
    txt = T.tex_text()
    aux = T.labels()
    for label, subs in FIGS:
        num = aux.get(label, {}).get("num", "缺失")
        c.check(num in ("18", "19"), f"{label} 编号为 18/19 之一", f"aux `{num}`")
        for c_no, ds, sub_lb, _ in subs:
            pair = "\\ref{" + label + "}\\subref{" + sub_lb + "}"
            c.check(pair in txt,
                    f"Case {c_no} (Δ={DELTA[c_no]}m) 的 Fig. 列引用指向 {sub_lb}",
                    f"tex 含 `{pair}`")
            c.check(sub_lb in aux, f"子图 label `{sub_lb}` 已在 aux 注册",
                    f"编号 `{aux.get(sub_lb, {}).get('num', '缺失')}`")

    # ── I ────────────────────────────────────────────────────────
    c.section("9. caption 已声明『个别样本、非最优』的免责说明")
    c.note("图上名次可能与表的均值趋势不同（与 Fig 16/17 同类问题）。"
           "本组 caption 原本就写明了这点，此处固化为断言防止日后被删。")
    for label, _ in FIGS:
        cap = T.caption_of(label) or ""
        c.check("individual sampled examples" in cap,
                f"{label} caption 声明为个别样本", "含 `individual sampled examples`")
        c.check("rather than the best result" in cap,
                f"{label} caption 声明非最优轮次", "含 `rather than the best result`")
        c.check("need not follow the averaged trend" in cap,
                f"{label} caption 说明不必吻合表的均值趋势",
                "含 `need not follow the averaged trend`")

    # ── J ────────────────────────────────────────────────────────
    c.section("10. 数据集复用（Table 3 的 Reuse 列）")
    c.note("Case 33 复用 Case 6 的 R4 数据集、Case 36 复用 Case 12 的 W4。"
           "两侧 npz 须逐字节相同，否则『复用』的说法不成立。")
    import hashlib
    for a, b in REUSE.items():
        pa, pb = paths.npz_path(a), paths.npz_path(b)
        ha = hashlib.md5(Path(pa).read_bytes()).hexdigest()
        hb = hashlib.md5(Path(pb).read_bytes()).hexdigest()
        c.check(ha == hb, f"Case {a} 与 Case {b} 的 npz 逐字节相同",
                f"md5 `{ha[:12]}` vs `{hb[:12]}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
