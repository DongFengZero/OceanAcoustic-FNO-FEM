#!/usr/bin/env python3
"""table15_19_abl_mesh_gen.py — 打印 Table 15-19（4.5 消融 / 4.6 网格 / 4.7 泛化）

  Table 15  tab:abl-rect     Cases 25-28：矩形消融（去先验 / 去图修正 / 去先验监督）
  Table 16  tab:abl-wedge    Cases 29-32：楔形消融，同四组
  Table 17  tab:mesh-rect    Cases 33-35：矩形网格无关性（R4 / R7 / R8）
  Table 18  tab:mesh-wedge   Cases 36-38：楔形网格无关性（W4 / W7 / W8）
  Table 19  tab:gen-overall  Cases 39-42：源位外推泛化（R9 / R10 / W9 / W10）

取数层：归档汇总 xlsx，可用 build_accuracy_xlsx.py 从训练日志重建（--check
已验证逐值一致），故最终仍可追到源数据。

    python table15_19_abl_mesh_gen.py [--tex]
"""
import _acctable as A

ABL_R = {25: "Full model", 26: "w/o physics prior",
         27: "w/o graph correction", 28: "w/o prior supervision"}
ABL_W = {29: "Full model", 30: "w/o physics prior",
         31: "w/o graph correction", 32: "w/o prior supervision"}


def table15():
    A.print_acc("tab:abl-rect", "Cases 25-28 · 矩形波导消融", "4.5", ABL_R,
                ["逐项移除一个组件，其余设置不变"])


def table16():
    A.print_acc("tab:abl-wedge", "Cases 29-32 · 楔形波导消融", "4.5", ABL_W,
                ["逐项移除一个组件，其余设置不变"])


def table17():
    A.print_acc("tab:mesh-rect", "Cases 33-35 · 矩形网格无关性", "4.6",
                {33: "R4 (base mesh)", 34: "R7 (refined)",
                 35: "R8 (coarsened)"},
                ["同一物理配置、不同网格分辨率，检验精度是否随网格漂移"])


def table18():
    A.print_acc("tab:mesh-wedge", "Cases 36-38 · 楔形网格无关性", "4.6",
                {36: "W4 (base mesh)", 37: "W7 (refined)",
                 38: "W8 (coarsened)"},
                ["同一物理配置、不同网格分辨率，检验精度是否随网格漂移"])


def table19():
    A.print_acc("tab:gen-overall", "Cases 39-42 · 源位外推泛化", "4.7",
                {39: "R9", 40: "R10", 41: "W9", 42: "W10"},
                ["源位落在训练区之外，检验外推能力"])


if __name__ == "__main__":
    for fn in (table15, table16, table17, table18, table19):
        fn()
    print()
