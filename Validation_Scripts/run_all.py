#!/usr/bin/env python3
"""run_all.py — 一站式跑完 Validation_Scripts 下的全部脚本

给人工核验用：一条命令把 R1 第 4 章的 12 张表打印出来（或把 11 张图重绘出来），
逐个报告成败，最后给一行汇总。任何脚本抛异常都会被抓住并计入失败，不会静默跳过。

表号按 R1 编。脚本文件名沿用 R1 之前的编号，故清单里显式写出当前表号。

    python run_all.py                # 只打印表（快，不写任何文件）
    python run_all.py --figures      # 表 + 重绘图（会覆盖 Figures/ 下的 PDF）
    python run_all.py --xlsx-check   # 表 + 校验精度 xlsx 可从训练日志重建
    python run_all.py --all          # 全部
    python run_all.py --list         # 只列出将执行什么，不执行

先设好环境变量（与 verify.py 相同）：
    CH4_RAWROOT   Raw_Experimental_Data 的父目录
    CH4_TEXDIR    编译好的论文目录（含 .aux）

重要：--figures / --all 会重绘 PDF。matplotlib 把生成时间写进 PDF，所以即使
数据和代码一字未改，重跑出来的 PDF 字节 md5 也必然不同——核验脚本对此已登记
豁免（比对时剥掉时间戳字段），故重绘不会造成失败；但论文里的图仍是原来那张，
要让论文用上新图，需自行把产物复制到论文 Figures/ 目录。

只核验数值不需要重绘图——默认（不带参数）只打印表，不写任何文件。
"""
import argparse
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# (脚本, 说明, 期望打印的表数)
TABLES = [
    ("table03_datasets.py", "Table 3      数据集总表", 1),
    ("table04_05_ideal.py", "Table 4-5    理想波导 + 深度线", 2),
    ("table06_08_forward.py", "Table 6-7    前向精度", 3),
    ("table09_12_depthline.py", "Table 8-9    深度线 MAE", 4),
    ("table13_14_perf.py", "Table 10     五方法对比", 2),
    ("table15_19_abl_mesh_gen.py", "Table 11-13  消融/网格/泛化", 5),
    ("table20_21_runtime.py", "Table 14     运行时", 2),
]

FIGURES = [
    ("regen_ideal_panels.py", "Fig 3-4"),
    ("regen_results_bigfont.py", "Fig 5-9, 18-19"),
    ("advantage_depth_line.py", "Fig 10-13"),
    ("regen_method_grid.py", "Fig 14-17"),
    ("plot_generalization_split.py", "Fig 20"),
    ("regen_gen_extrap_bigfont.py", "Fig 21-22"),
    ("build_perf_figure.py", "Fig 23"),
]

def resolve(script):
    """成图脚本要跑权威副本，不是仓库副本。

    这些脚本用 `os.path.dirname(__file__)` 定位数据（results/、CaseNN/ 等），
    那些目录只在权威副本旁边（CH4_PLOTROOT，默认 D:\\Data）。仓库里这份是
    md5 相同的副本，留作核验比对用，就地跑会找不到数据——核验文档里那句
    "md5 相同但路径不通"说的就是这件事。两份字节相同，所以跑哪份都等价。
    """
    auth_root = os.environ.get("CH4_PLOTROOT", r"D:\Data")
    cand = os.path.join(auth_root, script)
    return cand if os.path.exists(cand) else os.path.join(HERE, script)


def run(script, *extra):
    """跑一个脚本，返回 (成功, 耗时, stdout, stderr)。"""
    t0 = time.time()
    target = resolve(script)
    try:
        cp = subprocess.run(
            [sys.executable, target] + list(extra),
            cwd=os.path.dirname(target), capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=1800)
        return cp.returncode == 0, time.time() - t0, cp.stdout, cp.stderr
    except subprocess.TimeoutExpired:
        return False, time.time() - t0, "", "超时（>1800s）"
    except Exception as e:                       # noqa: BLE001
        return False, time.time() - t0, "", repr(e)


def n_tables(stdout):
    """数 stdout 里打印了几张表（表头形如 `Table 7  [tab:...]`）。"""
    return len(re.findall(r"^Table\s+\S+\s+\[", stdout, re.M))


def sync_figures():
    """把重绘出的深度线 PDF 拷到论文 Figures/，让『图表同源』断言重新成立。

    内容本来就一致（同数据同代码），差的只是 PDF 内嵌时间戳。
    """
    import shutil
    out = []
    try:
        pkg = os.path.join(os.path.dirname(HERE), "ch4_validation")
        if pkg not in sys.path:
            sys.path.insert(0, pkg)
        from common import paths, depthline as DL
    except Exception as e:                       # noqa: BLE001
        return [("导入 ch4_validation 失败", repr(e))]
    for g in ("comparison_R1_model_advantage", "comparison_W1_model_advantage",
              "ablation_R1_module_advantage", "ablation_W1_module_advantage"):
        try:
            src = DL.figure_pdf(g)
            if not (src and os.path.exists(src)):
                out.append((g, "脚本产物不存在，跳过"))
                continue
            dst = os.path.join(paths.FIGDIR, os.path.basename(src))
            shutil.copy2(src, dst)
            out.append((g, "已同步"))
        except Exception as e:                   # noqa: BLE001
            out.append((g, "失败 %r" % (e,)))
    return out


def main():
    ap = argparse.ArgumentParser(
        description="一站式运行 Validation_Scripts 下的表/图脚本")
    ap.add_argument("--figures", action="store_true",
                    help="同时重绘图（会覆盖 Figures/ 下的 PDF）")
    ap.add_argument("--xlsx-check", action="store_true",
                    help="校验精度 xlsx 可从训练日志重建")
    ap.add_argument("--all", action="store_true", help="以上全部")
    ap.add_argument("--list", action="store_true", help="只列出，不执行")
    ap.add_argument("--verbose", action="store_true", help="打印每个脚本输出")
    ap.add_argument("--sync-figures", action="store_true",
                    help="重绘后把深度线 PDF 同步到论文 Figures/，恢复图表同源")
    a = ap.parse_args()
    do_fig = a.figures or a.all
    do_chk = a.xlsx_check or a.all

    plan = [("表", s, d, n) for s, d, n in TABLES]
    if do_chk:
        plan.append(("校验", "build_accuracy_xlsx.py", "精度 xlsx 可重建", 0))
    if do_fig:
        plan += [("图", s, d, 0) for s, d in FIGURES]

    if a.list:
        print("将执行 %d 个脚本：\n" % len(plan))
        for kind, s, d, _ in plan:
            print("  [%s] %-30s %s" % (kind, s, d))
        if not do_fig:
            print("\n（未含重绘图，加 --figures 或 --all）")
        return 0

    print("=" * 76)
    print("Validation_Scripts 一站式运行   共 %d 个脚本" % len(plan))
    print("=" * 76)
    if do_fig:
        print("警告：重绘会刷新 PDF 的内嵌时间戳，令核验的『图表同源』md5 断言")
        print("      失败（8 项）。跑完请把新产物同步到论文 Figures/ 目录，")
        print("      或用 --sync-figures 让本脚本跑完自动同步。")
        print("-" * 76)

    nbad, ntab, want = 0, 0, 0
    fails = []
    for kind, s, d, exp in plan:
        extra = ["--check"] if s == "build_accuracy_xlsx.py" else []
        ok, dt, out, err = run(s, *extra)
        mark = "OK  " if ok else "FAIL"
        got = n_tables(out)
        ntab += got
        want += exp
        tail = ""
        if exp:
            tail = "  表 %d/%d" % (got, exp)
            if got != exp:
                ok = False
                mark = "FAIL"
                err = err or "打印表数不符（%d != %d）" % (got, exp)
        if s == "build_accuracy_xlsx.py":
            m = re.search(r"SUMMARY total=(\d+) ok=(\d+) bad=(\d+)", out)
            if m:
                tot_, ok_, bad_ = m.groups()
                tail = ("  %s/%s 项一致" % (ok_, tot_) if bad_ == "0"
                        else "  %s 项不一致！" % bad_)
                if bad_ != "0":
                    ok = False
                    mark = "FAIL"
        print("[%s] %-30s %-26s %5.1fs%s"
              % (mark, s, d, dt, tail))
        if a.verbose and out:
            print(out)
        if not ok:
            nbad += 1
            fails.append((s, err or out[-300:]))

    if do_fig and a.sync_figures:
        print("-" * 76)
        print("同步深度线 PDF 到论文 Figures/（恢复图表同源）：")
        for g, n in sync_figures():
            print("  %-36s %s" % (g, n))

    print("-" * 76)
    print("表：打印 %d/%d 张%s" % (ntab, want,
          "  (缺 %d)" % (want - ntab) if ntab < want else ""))
    if do_fig:
        nf = len(FIGURES)
        bad_f = sum(1 for s, _ in FIGURES
                    if any(f[0] == s for f in fails))
        print("图：%d/%d 个成图脚本成功" % (nf - bad_f, nf))
    print("失败脚本：%d" % nbad)
    if fails:
        print("\n失败详情：")
        for name, err in fails:
            line = (err.strip().splitlines() or ["(无输出)"])[-1]
            # 子进程输出经管道可能带无法编码的替换字符，转义后再打印，
            # 否则这里自己会因 UnicodeEncodeError 崩掉。
            safe = line[:88].encode("ascii", "backslashreplace").decode()
            print("  %-30s %s" % (name, safe))
    print("\n权威判定请跑核验套件： cd ../ch4_validation && python verify.py")
    return 1 if nbad else 0


if __name__ == "__main__":
    sys.exit(main())
