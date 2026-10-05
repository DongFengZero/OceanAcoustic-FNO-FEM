#!/usr/bin/env python3
"""run_all.py — 一站式跑完 Validation_Scripts 下的全部脚本

给人工核验用：一条命令把 R1 第 4 章的 12 张表打印出来（或把 Fig. 3-13 与补充材料
Figs. S1-S7 重绘出来），
逐个报告成败，最后给一行汇总。任何脚本抛异常都会被抓住并计入失败，不会静默跳过。

脚本名与清单中的表号、图号均按 R1 正文及补充材料编排。

    python run_all.py                # 只打印表（快，不写任何文件）
    python run_all.py --figures      # 表 + 重绘图（产物写入各 figNN_*/out/）
    python run_all.py --xlsx-check   # 表 + 校验精度 xlsx 可从训练日志重建
    python run_all.py --all          # 全部
    python run_all.py --list         # 只列出将执行什么，不执行

先设好环境变量（与 verify.py 相同）：
    CH4_RAWROOT   Raw_Experimental_Data 的父目录
    CH4_TEXDIR    编译好的论文目录（含 .aux）

重绘的 PDF 只写入各成图目录的 out/，不会改动论文 Figures/ 下的图件。PDF 内嵌
生成时间，重绘后字节 md5 必然不同；核验比对时剥掉时间戳字段，故不受影响。
要让论文用上新图，需自行把 out/ 下的产物复制到论文 Figures/ 目录。

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
    ("table04_ideal.py", "Table 4      理想波导", 1),
    ("table05_06_forward.py", "Table 5-6    前向精度", 3),
    ("table07_08_depthline.py", "Table 7-8    深度线 MAE", 4),
    ("table09_perf_cmp.py", "Table 9     五方法对比", 2),
    ("table10_12_abl_mesh_gen.py", "Table 10-12  消融/网格/泛化", 5),
    ("table13_runtime.py", "Table 13     运行时", 2),
]

FIGURES = [
    ("fig03_ideal/fig03_ideal.py", "Fig 3"),
    ("fig04_05_10_fields/fig04_05_10_fields.py", "Fig 4, 5, 10, 12(R9/W10)"),
    ("fig06_07_dl/fig06_07_dl.py", "Fig 6-7"),
    ("fig08_09_perf_grid/fig08_09_perf_grid.py", "Fig 8-9"),
    ("fig11_gen_split/fig11_gen_split.py", "Fig 11"),
    ("fig13_perf/fig13_perf.py", "Fig 13"),
    ("figS1_S7_supplementary/figS1_S7_supplementary.py", "Fig S1-S7"),
]

def resolve(script):
    """表/图脚本都在本目录内（R1 整理后），数据经 _figpaths / CH4_RAWROOT 解析，就地运行。"""
    return os.path.join(HERE, script)


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
    """数 stdout 里打印了几张表（表头形如 `Table 6  [tab:...]`）。"""
    return len(re.findall(r"^Table\s+\S+\s+\[", stdout, re.M))


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
        print("重绘产物写入各 figNN_*/out/，不改动论文 Figures/。")
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


    print("-" * 76)
    print("表：Table 3-13 共打印 %d/%d 个表块%s" % (ntab, want,
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
