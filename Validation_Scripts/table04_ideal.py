#!/usr/bin/env python3
"""table04_ideal.py — 打印 Table 4（tab:ideal-overall）

对象：4.2 节理想波导，R0 (Case 1) / W0 (Case 2)，与解析解对比。
  Table 4  场精度：逐频 Sol/TL + Avg.

取数层
  Table 4  归档汇总 xlsx（该 xlsx 可用 build_accuracy_xlsx.py 从训练日志重建，
           --check 已验证 420 项逐值一致）

    python table04_ideal.py [--tex]
"""
import _acctable as A
import _tblcommon as K

CASES = {1: "R0 (rect.)", 2: "W0 (wedge)"}


def table04():
    A.print_acc("tab:ideal-overall",
                "Cases 1-2 · 理想波导场精度（vs 解析解）", "4.2", CASES,
                ["Avg. 列 = 四频均值（caption 声明，verify.py 有断言）"])


if __name__ == "__main__":
    table04()
    print()
