#!/usr/bin/env python3
"""table05_06_forward.py — 打印 Table 5/6（4.3 节，含障碍物的前向精度）

  Table 5  tab:res-rect-mf  Cases 3-5 / 9-11：多频，矩形 R1-R3 与楔形 W1-W3
  Table 6  tab:sq100        100 Hz 方形域，单张 tabular 左右两个列组：
              左列组 Cases 6-8 矩形 R4-R6，右列组 Cases 12-14 楔形 W4-W6
              （域尺度均为 128 / 256 / 512 m）


参考解为 COMSOL 数值解（理想几何用解析解，见 Table 4）。

取数层：归档汇总 xlsx。该 xlsx 可用 build_accuracy_xlsx.py 从训练日志重建，
其 --check 模式已验证 4.2-4.7 共 420 项（42 案例 × 5 组 × 2 量）逐值一致，
故这条链最终仍落到源数据（full_run_*.log）。

    python table05_06_forward.py [--tex]
"""
import _acctable as A


def table06():
    A.print_acc("tab:res-rect-mf",
                "Cases 3-5 / 9-11 · 多频前向精度（矩形 + 楔形）", "4.3",
                {3: "R1 (rect. 128m)", 4: "R2 (rect. 256m)",
                 5: "R3 (rect. 512m)", 9: "W1 (wedge 128m)",
                 10: "W2 (wedge 256m)", 11: "W3 (wedge 512m)"})


def table07_rect():
    A.print_acc("tab:sq100",
                "Cases 6-8 · 100 Hz 矩形波导（左列组）", "4.3",
                {6: "R4 (128m)", 7: "R5 (256m)", 8: "R6 (512m)"},
                ["单频表：只有 100 Hz 一组，Avg. 列即该频值"])


def table07_wedge():
    A.print_acc("tab:sq100",
                "Cases 12-14 · 100 Hz 楔形波导（右列组）", "4.3",
                {12: "W4 (128m)", 13: "W5 (256m)", 14: "W6 (512m)"},
                ["单频表：只有 100 Hz 一组，Avg. 列即该频值"])


if __name__ == "__main__":
    table06()
    table07_rect()
    table07_wedge()
    print()
