#!/usr/bin/env python3
"""table13_14_perf.py — 打印 Table 13/14（4.4 节，五方法场精度对比）

  Table 13  tab:perf-rect   Cases 15-19：矩形，Proposed / DeepONet / FNO / KNO / CNO
  Table 14  tab:perf-wedge  Cases 20-24：楔形，同五方法

所有基线与本文模型同输入、同训练调度、同网格采样，在同一 held-out 划分上
对同一参考解评估（见论文 4.4 节的对照协议）。

取数层：归档汇总 xlsx，可用 build_accuracy_xlsx.py 从训练日志重建（--check
已验证逐值一致），故最终仍可追到源数据。

    python table13_14_perf.py [--tex]
"""
import _acctable as A

METHODS_R = {15: "Proposed", 16: "DeepONet", 17: "FNO",
             18: "KNO", 19: "CNO"}
METHODS_W = {20: "Proposed", 21: "DeepONet", 22: "FNO",
             23: "KNO", 24: "CNO"}


def table13():
    A.print_acc("tab:perf-rect", "Cases 15-19 · 矩形波导五方法场精度", "4.4",
                METHODS_R, ["同表内最优值在论文中加粗，此处不加粗以便机读"])


def table14():
    A.print_acc("tab:perf-wedge", "Cases 20-24 · 楔形波导五方法场精度", "4.4",
                METHODS_W, ["同表内最优值在论文中加粗，此处不加粗以便机读"])


if __name__ == "__main__":
    table13()
    table14()
    print()
