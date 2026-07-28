#!/usr/bin/env python3
"""
Fig 8/9（fig:res-rect-100 / fig:res-wedge-100）核验

对象：100 Hz 单频、方形域 TL 场图，各 3 个子图。
  Fig 8 = Case 6 (R4,128) / Case 7 (R5,256) / Case 8 (R6,512)   矩形
  Fig 9 = Case 12 (W4,128) / 13 (W5,256) / 14 (W6,512)          楔形

与 Fig 5/6/7 的差别：单频 npz 只含 2 个样本（多频 8 个）；三子图各带
subfloat label；对应 Table 7/8 取 best epoch 而图取 ep200(last)，
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

SLUG = "FIG08_09_res_100"

SCRIPT_AUTH = Path(r"D:\Data\regen_results_bigfont.py")
SCRIPT_REPO = Path(r"D:\Data\OceanAcoustic-FNO-FEM_github\Validation_Scripts"
                   r"\regen_results_bigfont.py")

# (图 label, [(case, 数据集, 子图 label, PDF 文件名), ...])
FIGS = [
    ("fig:res-rect-100", [
        (6, "R4", "fig:res-rect-100-4", "Case06_R4_TL.pdf"),
        (7, "R5", "fig:res-rect-100-5", "Case07_R5_TL.pdf"),
        (8, "R6", "fig:res-rect-100-6", "Case08_R6_TL.pdf"),
    ]),
    ("fig:res-wedge-100", [
        (12, "W4", "fig:res-wedge-100-10", "Case12_W4_TL.pdf"),
        (13, "W5", "fig:res-wedge-100-11", "Case13_W5_TL.pdf"),
        (14, "W6", "fig:res-wedge-100-12", "Case14_W6_TL.pdf"),
    ]),
]
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

    c = report.Checker(SLUG, "100Hz 单频 TL 场图 Fig 8/9", "figure",
                       "fig:res-rect-100 / fig:res-wedge-100", "8/9")

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
    c.note("图取 ep200(last)，兄弟表 Table 7/8 取 best epoch。二者本是不同轮。")
    from common import metrics as M
    for c_no in CASES:
        be = M.xlsx_case(paths.xlsx_path("4.3"), c_no)["best_epoch"]
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
    c.section("7. 图表趋势同向（图逐样本 vs 表全测试集）")
    c.note("图上 Avg 是单样本场误差，Table 7/8 的 TL 是全测试集平均，"
           "二者不可互相反算，只核趋势：域尺度越大误差越大。")
    for label, subs in FIGS:
        nos = [c_no for c_no, _, _, _ in subs]
        avgs = [max(s["avg_err"] for s in rec[n]["samples"]) for n in nos]
        c.check(avgs == sorted(avgs),
                f"{label} 误差随域尺度单调上升",
                " < ".join(f"Case{n}:{a:.2f}" for n, a in zip(nos, avgs)))

    # ── H ────────────────────────────────────────────────────────
    c.section("8. 正文引用：被引 + 说明与图内容相符")
    c.note("Fig 8 的单张 \\ref 计数为 0 并非漏引：Fig 5-9 编号连续，正文用"
           "区间引用 `Figs.~\\ref{fig:res-128}--\\ref{fig:res-wedge-100}` "
           "一次覆盖五张，Fig 8 落在区间内部。Fig 9 是区间右端点，"
           "故同时以端点身份出现在正文。")
    txt = T.tex_text()
    span_ref = "\\ref{fig:res-128}--\\ref{fig:res-wedge-100}"
    c.check(span_ref in txt, "正文存在覆盖 Fig 8/9 的区间引用",
            f"`Figs.~{span_ref}`")
    c.check(txt.count(span_ref) >= 2,
            "该区间引用在 4.3 节出现 >=2 处（引入段 + 结论段）",
            f"实得 {txt.count(span_ref)} 处")
    # 右端点必须正好是 Fig 9 的 label，否则区间覆盖不到 Fig 8/9
    aux = T.labels()
    c.check(aux.get("fig:res-wedge-100", {}).get("num") == "9",
            "区间右端点 fig:res-wedge-100 编号为 9",
            f"aux `{aux.get('fig:res-wedge-100', {}).get('num', '缺失')}`")
    c.check(aux.get("fig:res-rect-100", {}).get("num") == "8",
            "Fig 8 编号为 8，确在区间 5-9 内部",
            f"aux `{aux.get('fig:res-rect-100', {}).get('num', '缺失')}`")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
