#!/usr/bin/env python3
"""table10_12_abl_mesh_gen.py — 打印 Table 10-12（4.5 消融 / 4.6 网格 / 4.7 泛化）

  Table 10  tab:abl         单张 tabular 左右两个列组：
              左列组 Cases 25-28 矩形消融，右列组 Cases 29-32 楔形消融
              四组：去先验 / 去图修正 / 去先验监督 / 全模型
  Table 11  tab:mesh        单张 tabular 左右两个列组：
              左列组 Cases 33-35 矩形网格（R4 / R7 / R8）
              右列组 Cases 36-38 楔形网格（W4 / W7 / W8）
  Table 12  tab:gen-overall Cases 39-42：源位外推泛化（R9 / R10 / W9 / W10）


取数层：归档汇总 xlsx，可用 build_accuracy_xlsx.py 从训练日志重建（--check
已验证逐值一致），故最终仍可追到源数据。

    python table10_12_abl_mesh_gen.py [--tex]
"""
import _acctable as A

ABL_R = {25: "Full model", 26: "w/o physics prior",
         27: "w/o graph correction", 28: "w/o prior supervision"}
ABL_W = {29: "Full model", 30: "w/o physics prior",
         31: "w/o graph correction", 32: "w/o prior supervision"}


def table11_rect():
    A.print_acc("tab:abl", "Cases 25-28 · 矩形波导消融（左列组）", "4.5",
                ABL_R, ["逐项移除一个组件，其余设置不变"])


def table11_wedge():
    A.print_acc("tab:abl", "Cases 29-32 · 楔形波导消融（右列组）", "4.5",
                ABL_W, ["逐项移除一个组件，其余设置不变"])


def table12_rect():
    A.print_acc("tab:mesh", "Cases 33-35 · 矩形网格无关性（左列组）", "4.6",
                {33: "R4 (base mesh)", 34: "R7 (refined)",
                 35: "R8 (coarsened)"},
                ["同一物理配置、不同网格分辨率，检验精度是否随网格漂移"])


def table12_wedge():
    A.print_acc("tab:mesh", "Cases 36-38 · 楔形网格无关性（右列组）", "4.6",
                {36: "W4 (base mesh)", 37: "W7 (refined)",
                 38: "W8 (coarsened)"},
                ["同一物理配置、不同网格分辨率，检验精度是否随网格漂移"])


def table13():
    A.print_acc("tab:gen-overall", "Cases 39-42 · 源位外推泛化", "4.7",
                {39: "R9", 40: "R10", 41: "W9", 42: "W10"},
                ["源位落在训练区之外，检验外推能力"])


if __name__ == "__main__":
    for fn in (table11_rect, table11_wedge, table12_rect, table12_wedge, table13):
        fn()
    print()
