#!/usr/bin/env python3
"""table13_14_perf.py — 打印 Table 10（4.4 节，五方法场精度对比）

  Table 10  tab:perf-cmp   单张 tabular，左右两个列组：
              左列组 Cases 15-19 矩形（R1），右列组 Cases 20-24 楔形（W1）
              方法均为 Proposed / DeepONet / FNO / KNO / CNO

文件名沿用旧编号（R1 前的 Table 13/14），目录归属以本文件头的表号为准。

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


def table_rect():
    A.print_acc("tab:perf-cmp", "Cases 15-19 · 矩形波导五方法场精度（左列组）",
                "4.4", METHODS_R,
                ["同表内最优值在论文中加粗，此处不加粗以便机读"])


def table_wedge():
    A.print_acc("tab:perf-cmp", "Cases 20-24 · 楔形波导五方法场精度（右列组）",
                "4.4", METHODS_W,
                ["同表内最优值在论文中加粗，此处不加粗以便机读"])


if __name__ == "__main__":
    table_rect()
    table_wedge()
    print()
