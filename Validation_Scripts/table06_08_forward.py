#!/usr/bin/env python3
"""table06_08_forward.py — 打印 Table 6/7/8（4.3 节，含障碍物的前向精度）

  Table 6  tab:res-rect-mf    Cases 3-5, 9-11：多频，矩形 R1-R3 与楔形 W1-W3
  Table 7  tab:res-rect-100   Cases 6-8：100 Hz，矩形 R4-R6（域 128/256/512 m）
  Table 8  tab:res-wedge-100  Cases 12-14：100 Hz，楔形 W4-W6

参考解为 COMSOL 数值解（理想几何用解析解，见 Table 4）。

取数层：归档汇总 xlsx。该 xlsx 可用 build_accuracy_xlsx.py 从训练日志重建，
其 --check 模式已验证 4.2-4.7 共 420 项（42 案例 × 5 组 × 2 量）逐值一致，
故这条链最终仍落到源数据（full_run_*.log）。

    python table06_08_forward.py [--tex]
"""
import _acctable as A


def table06():
    A.print_acc("tab:res-rect-mf",
                "Cases 3-5 / 9-11 · 多频前向精度（矩形 + 楔形）", "4.3",
                {3: "R1 (rect. 128m)", 4: "R2 (rect. 256m)",
                 5: "R3 (rect. 512m)", 9: "W1 (wedge 128m)",
                 10: "W2 (wedge 256m)", 11: "W3 (wedge 512m)"})


def table07():
    A.print_acc("tab:res-rect-100",
                "Cases 6-8 · 100 Hz 矩形波导（域尺度 128→512 m）", "4.3",
                {6: "R4 (128m)", 7: "R5 (256m)", 8: "R6 (512m)"},
                ["单频表：只有 100 Hz 一组，Avg. 列即该频值"])


def table08():
    A.print_acc("tab:res-wedge-100",
                "Cases 12-14 · 100 Hz 楔形波导（域尺度 128→512 m）", "4.3",
                {12: "W4 (128m)", 13: "W5 (256m)", 14: "W6 (512m)"},
                ["单频表：只有 100 Hz 一组，Avg. 列即该频值"])


if __name__ == "__main__":
    table06()
    table07()
    table08()
    print()
