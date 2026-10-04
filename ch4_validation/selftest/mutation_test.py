# -*- coding: utf-8 -*-
"""Mutation test of the verification suite: does it catch errors it should catch?

A copy of the manuscript directory is checked by the suite (CH4_TEXDIR points at
the copy). First the unmodified copy must pass (no false alarms). Then, one at a
time, a single realistic error is planted -- a mistyped digit, two rows swapped,
a wrong rounding, a dropped trailing zero, a wrong epoch claim in a caption, a
wrong number in the prose, a wrong derived ratio, wrong Table 3 metadata, or the
wrong figure file in place of the right one -- and the checker responsible for
that object is run. A mutation is "killed" if the checker reports at least one
FAIL; a surviving mutation means the suite has a blind spot.

The suite's own reports/ are overwritten during the run; verify.py is re-run at
the end to restore them.
"""
import os, re, shutil, subprocess, sys

SRC = os.environ.get("CH4_TEXDIR", r"D:\JASA\OE\OE_Revision_R1_Submission")
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_mutwork")
PAPER = os.path.join(WORK, "paper")
SUITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = chr(92)
TEX = "OE_submission.tex"

# (编号, 说明, 改动, 负责的核验脚本)
#   改动 = ("tex", 原文, 改后)  或  ("swap", 被替换图件, 用来顶替的图件)
M = [
    ("M01", "Table 6 末位抄错 2.476→2.477", ("tex", "3 & R1 & 2.476 &", "3 & R1 & 2.477 &"), "scripts/T06_res_rect_mf"),
    ("M02", "Table 6 舍入错 TL 0.951→0.950", ("tex", "& 1.688 & 0.951 " + B + B, "& 1.688 & 0.950 " + B + B), "scripts/T06_res_rect_mf"),
    ("M03", "Table 6 少写一位 0.266→0.27", ("tex", "3 & R1 & 2.476 & 0.705 & 0.266 &", "3 & R1 & 2.476 & 0.705 & 0.27 &"), "scripts/T06_res_rect_mf"),
    ("M04", "Table 6 caption epoch best→last", ("tex", "four frequencies. Values are from the best epoch.}\n\t" + B + "label{tab:res-rect-mf}",
                                                 "four frequencies. Values are from the last epoch.}\n\t" + B + "label{tab:res-rect-mf}"), "scripts/T06_res_rect_mf"),
    ("M05", "正文引用值 1.688→1.698", ("tex", "rises from $1.688" + B + "times", "rises from $1.698" + B + "times"), "scripts/T06_res_rect_mf|scripts/PROSE_numbers"),
    ("M19", "正文值换成同表另一算例 1.688(Case 3)→2.121(Case 9)", ("tex", "rises from $1.688" + B + "times10^{-6}$ at $128$" + B + ",m (Case~3)", "rises from $2.121" + B + "times10^{-6}$ at $128$" + B + ",m (Case~3)"), "scripts/T06_res_rect_mf|scripts/PROSE_numbers"),
    ("M20", "正文值换成未引用表的数 1.515→3.852", ("tex", "staying at or below $1.515$", "staying at or below $3.852$"), "scripts/T08_dl_cmp|scripts/PROSE_numbers"),
    ("M21", "正文值换成同表另一合法值、无 Case 括注 1.515→1.210", ("tex", "staying at or below $1.515$", "staying at or below $1.210$"), "scripts/T08_dl_cmp|scripts/PROSE_numbers"),
    ("M06", "正文推导倍数 2.268→2.267", ("tex", "factor of only $2.268$", "factor of only $2.267$"), "scripts/T06_res_rect_mf"),
    ("M07", "Table 10 两行对调 (DeepONet↔FNO 数值)",
     ("tex", "16 & DeepONet & 32.022 & 1.508 & 18.370 & 1.869 & 53.548 & 3.491 & 81.196 & 7.067 & 46.284 & 3.484 " + B + B + "\n\t\t\t17 & FNO & 4.016 & 0.829 & 0.441 & 0.606 & 4.748 & 1.529 & 5.713 & 2.256 & 3.730 & 1.305 " + B + B,
             "16 & DeepONet & 4.016 & 0.829 & 0.441 & 0.606 & 4.748 & 1.529 & 5.713 & 2.256 & 3.730 & 1.305 " + B + B + "\n\t\t\t17 & FNO & 32.022 & 1.508 & 18.370 & 1.869 & 53.548 & 3.491 & 81.196 & 7.067 & 46.284 & 3.484 " + B + B),
     "scripts/T10_perf_cmp"),
    ("M08", "Table 10 数字换位 32.022→32.202", ("tex", "16 & DeepONet & 32.022", "16 & DeepONet & 32.202"), "scripts/T10_perf_cmp"),
    ("M09", "Table 8 深度线值换位 0.469→0.496", ("tex", "Proposed & " + B + "textbf{0.469}", "Proposed & " + B + "textbf{0.496}"), "scripts/T08_dl_cmp"),
    ("M10", "Table 8 加粗标错（最优值未加粗）", ("tex", "Proposed & " + B + "textbf{0.469}", "Proposed & 0.469"), "scripts/T08_dl_cmp"),
    ("M11", "Table 9 消融深度线 1.092→1.029", ("tex", "Full model            & 1.092", "Full model            & 1.029"), "scripts/T09_dl_abl"),
    ("M12", "Table 3 Reuse 3→1（本次查出的原错误）", ("tex", "& 3 & DCU & Proposed (reuse)", "& 1 & DCU & Proposed (reuse)"), "scripts/T03_datasets"),
    ("M13", "Table 3 样本数 8000→2000（本次查出的原错误）",
     ("tex", "25,50,75,100 & 8000" + B + ",(2000) & (64,64,16,8)  &        & A800 & Runtime",
             "25,50,75,100 & 2000" + B + ",(2000) & (64,64,16,8)  &        & A800 & Runtime"), "scripts/T03_datasets"),
    ("M14", "Table 14 运行时间 873.10→873.01", ("tex", "COMSOL  & 873.10", "COMSOL  & 873.01"), "scripts/T14_runtime"),
    ("M15", "Fig. 4 放错图件（矩形位置放楔形图）", ("swap", "Figures/results/case03_r1_tl.pdf", "Figures/results/case09_w1_tl.pdf"), "scripts_figures/FIG04_res_128"),
    ("M16", "Fig. 6 放错图件（对比图换成消融图）", ("swap", "Figures/results/comparison_r1_model_advantage.pdf", "Figures/results/ablation_r1_module_advantage.pdf"), "scripts_figures/FIG06_dl_cmp"),
    ("M17", "Fig. S1 放错图件（S1 位置放 S2）", ("swap", "Figures/supplementary/figS1_case04_r2.pdf", "Figures/supplementary/figS2_case10_w2.pdf"), "scripts_figures/FIGS1_S7_supplementary"),
    ("M18", "正文 S 编号越界 Fig.~S7→Fig.~S8", ("tex", "and Fig.~S7 of the Supplementary", "and Fig.~S8 of the Supplementary"), "scripts_figures/FIGS1_S7_supplementary"),
]


def run(script):
    env = dict(os.environ, CH4_TEXDIR=PAPER, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, os.path.join(SUITE, script + ".py")],
                       cwd=SUITE, env=env, capture_output=True, timeout=1800)
    out = r.stdout.decode("utf8", "replace") + r.stderr.decode("utf8", "replace")
    m = re.search(r"\[(PASS|FAIL)\] \S+: (\d+) pass / (\d+) fail", out)
    if not m:
        return "CRASH", 0, 0, out.strip().splitlines()[-1][:120] if out.strip() else ""
    fails = []
    rep = os.path.join(SUITE, "reports", os.path.basename(script) + ".md")
    if os.path.exists(rep):
        fails = [l.split("|")[1].strip() for l in open(rep, encoding="utf8") if "**FAIL**" in l and l.startswith("|")]
    return m.group(1), int(m.group(2)), int(m.group(3)), "; ".join(fails[:2])


if os.path.isdir(WORK):
    shutil.rmtree(WORK)
os.makedirs(PAPER)
for f in ("OE_submission.tex", "OE_submission.aux", "OE_submission.bbl",
          "OE_supplementary.tex", "Response_to_Reviewers.tex"):
    shutil.copy2(os.path.join(SRC, f), PAPER)
shutil.copytree(os.path.join(SRC, "Figures"), os.path.join(PAPER, "Figures"))
pristine = open(os.path.join(PAPER, TEX), encoding="utf8").read()

print("== 基线：未改动的副本必须全部通过（不误报）")
for script in sorted({x for m in M for x in m[3].split("|")}):
    st, p, f, why = run(script)
    print(f"   {script:38s} {st}  {p} pass / {f} fail  {why}")

print("\n== 逐个植入错误")
killed = 0
for code, desc, (kind, a, b), script in M:
    tex_path = os.path.join(PAPER, TEX)
    if kind == "tex":
        assert pristine.count(a) == 1, (code, pristine.count(a))
        open(tex_path, "w", encoding="utf8", newline="\n").write(pristine.replace(a, b))
    else:
        tgt = os.path.join(PAPER, a)
        bak = tgt + ".orig"
        shutil.copy2(tgt, bak)
        shutil.copy2(os.path.join(PAPER, b), tgt)
    res = [run(sc) for sc in script.split("|")]
    st = "FAIL" if any(r[0] in ("FAIL", "CRASH") for r in res) else "PASS"
    f = sum(r[2] for r in res)
    why = "; ".join(f"{os.path.basename(sc)}: {r[3]}" for sc, r in zip(script.split("|"), res) if r[2])
    if kind == "tex":
        open(tex_path, "w", encoding="utf8", newline="\n").write(pristine)
    else:
        shutil.move(bak, tgt)
    names = ",".join(os.path.basename(x) for x in script.split("|"))
    caught = st in ("FAIL", "CRASH")
    killed += caught
    print(f"   {code} {'抓到' if caught else '漏网!!'}  {desc:42s} -> {names} {st} "
          f"({f} fail)  {why[:90]}")
print(f"\n抓到 {killed}/{len(M)}")
