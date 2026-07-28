"""
registry.py — 第四章 40 个对象的清单与源映射
=============================================
一张表/一张图 = 一条记录。编号取自 aux（真实排版编号），
案例号决定 xlsx/log/npz 三源位置，plot 字段记录成图脚本。

这是"每张表/图源可追溯"的索引本体：报告里的源清单由此生成，
verify.py 的覆盖率检查也以此为分母——漏登记会被查出来。

字段
  slug    脚本与报告的文件名主干，形如 T04_ideal_overall / F03_ideal_rect
  label   tex 里的 \\label
  kind    table | figure
  sec     所属节号
  cases   涉及的 Case No. 列表（决定 xlsx / log / npz 源）
  epoch   'best' 表格取 best epoch；'last' 深度线表与全部图片取 ep200
  plot    Validation_Scripts/ 下的成图脚本（图片对象必填）
  asset   Figures/results/ 下的成图文件（图片对象必填）
  desc    一句话说明
"""

TABLES = [
    dict(slug="T03_datasets", label="tab:datasets", kind="table", sec="4.1",
         cases=list(range(1, 51)), epoch=None, desc="数据集总表 No.1-50（结构性，非测量值）"),
    dict(slug="T04_ideal_overall", label="tab:ideal-overall", kind="table", sec="4.2",
         cases=[1, 2], epoch="best", desc="解析解场精度 R0/W0"),
    dict(slug="T05_ideal_depthline", label="tab:ideal-depthline", kind="table", sec="4.2",
         cases=[1, 2], epoch="last", plot="regen_ideal_panels.py",
         desc="解析解深度线 MAE @y=44.7m"),
    dict(slug="T06_res_rect_mf", label="tab:res-rect-mf", kind="table", sec="4.3",
         cases=[3, 4, 5, 9, 10, 11], epoch="best", desc="多频前向精度 R1-R3/W1-W3"),
    dict(slug="T07_res_rect_100", label="tab:res-rect-100", kind="table", sec="4.3",
         cases=[6, 7, 8], epoch="best", desc="100Hz 方形域 矩形 R4-R6"),
    dict(slug="T08_res_wedge_100", label="tab:res-wedge-100", kind="table", sec="4.3",
         cases=[12, 13, 14], epoch="best", desc="100Hz 方形域 楔形 W4-W6"),
    dict(slug="T09_dl_cmp_rect", label="tab:dl-cmp-rect", kind="table", sec="4.4",
         cases=[15, 16, 17, 18, 19], epoch="last", plot="advantage_depth_line.py",
         desc="五方法深度线 TL @R1 y=56.1m"),
    dict(slug="T10_dl_cmp_wedge", label="tab:dl-cmp-wedge", kind="table", sec="4.4",
         cases=[20, 21, 22, 23, 24], epoch="last", plot="advantage_depth_line.py",
         desc="五方法深度线 TL @W1 y=30.4m"),
    dict(slug="T11_dl_abl_rect", label="tab:dl-abl-rect", kind="table", sec="4.5",
         cases=[25, 26, 27, 28], epoch="last", plot="advantage_depth_line.py",
         desc="消融深度线 TL @R1 y=71.9m"),
    dict(slug="T12_dl_abl_wedge", label="tab:dl-abl-wedge", kind="table", sec="4.5",
         cases=[29, 30, 31, 32], epoch="last", plot="advantage_depth_line.py",
         desc="消融深度线 TL @W1 y=33.4m"),
    dict(slug="T13_perf_rect", label="tab:perf-rect", kind="table", sec="4.4",
         cases=[15, 16, 17, 18, 19], epoch="best", desc="五方法逐频精度 R1"),
    dict(slug="T14_perf_wedge", label="tab:perf-wedge", kind="table", sec="4.4",
         cases=[20, 21, 22, 23, 24], epoch="best", desc="五方法逐频精度 W1"),
    dict(slug="T15_abl_rect", label="tab:abl-rect", kind="table", sec="4.5",
         cases=[25, 26, 27, 28], epoch="best", desc="消融逐频结果 R1"),
    dict(slug="T16_abl_wedge", label="tab:abl-wedge", kind="table", sec="4.5",
         cases=[29, 30, 31, 32], epoch="best", desc="消融逐频结果 W1"),
    dict(slug="T17_mesh_rect", label="tab:mesh-rect", kind="table", sec="4.6",
         cases=[33, 34, 35], epoch="best", desc="网格无关性 矩形"),
    dict(slug="T18_mesh_wedge", label="tab:mesh-wedge", kind="table", sec="4.6",
         cases=[36, 37, 38], epoch="best", desc="网格无关性 楔形"),
    dict(slug="T19_gen_overall", label="tab:gen-overall", kind="table", sec="4.7",
         cases=[39, 40, 41, 42], epoch="best", desc="泛化外推精度 R9/R10/W9/W10"),
    dict(slug="T20_runtime", label="tab:runtime", kind="table", sec="4.8",
         cases=[43, 44], epoch=None, desc="单轮计时与加速比"),
    dict(slug="T21_runtime_scale", label="tab:runtime-scale", kind="table", sec="4.8",
         cases=[45, 46, 47, 48, 49, 50], epoch=None, desc="跨域尺度推理耗时"),
]

FIGURES = [
    dict(slug="F03_ideal_rect", label="fig:ideal-rect", kind="figure", sec="4.2",
         cases=[1], epoch="last", plot="regen_ideal_panels.py",
         asset="Case01_R0_grid2.pdf", desc="R0 解析解验证网格图"),
    dict(slug="F04_ideal_wedge", label="fig:ideal-wedge", kind="figure", sec="4.2",
         cases=[2], epoch="last", plot="regen_ideal_panels.py",
         asset="Case02_W0_grid2.pdf", desc="W0 解析解验证网格图"),
    dict(slug="F05_res_128", label="fig:res-128", kind="figure", sec="4.3",
         cases=[3, 9], epoch="last", plot="regen_results_bigfont.py",
         asset="Case03_R1_TL.pdf|Case09_W1_TL.pdf", desc="128x128 TL 场"),
    dict(slug="F06_res_256", label="fig:res-256", kind="figure", sec="4.3",
         cases=[4, 10], epoch="last", plot="regen_results_bigfont.py",
         asset="Case04_R2_TL.pdf|Case10_W2_TL.pdf", desc="256x128 TL 场"),
    dict(slug="F07_res_512", label="fig:res-512", kind="figure", sec="4.3",
         cases=[5, 11], epoch="last", plot="regen_results_bigfont.py",
         asset="Case05_R3_TL.pdf|Case11_W3_TL.pdf", desc="512x128 TL 场"),
    dict(slug="F08_res_rect_100", label="fig:res-rect-100", kind="figure", sec="4.3",
         cases=[6, 7, 8], epoch="last", plot="regen_wide_fields.py",
         asset="Case06_R4_TL.pdf|Case07_R5_TL.pdf|Case08_R6_TL.pdf",
         desc="100Hz 矩形方形域 TL 场"),
    dict(slug="F09_res_wedge_100", label="fig:res-wedge-100", kind="figure", sec="4.3",
         cases=[12, 13, 14], epoch="last", plot="regen_wide_fields.py",
         asset="Case12_W4_TL.pdf|Case13_W5_TL.pdf|Case14_W6_TL.pdf",
         desc="100Hz 楔形方形域 TL 场"),
    dict(slug="F10_dl_cmp_rect", label="fig:dl-cmp-rect", kind="figure", sec="4.4",
         cases=[15, 16, 17, 18, 19], epoch="last", plot="advantage_depth_line.py",
         asset="advantage_depthline_R1.pdf", desc="五方法深度线曲线 R1"),
    dict(slug="F11_dl_cmp_wedge", label="fig:dl-cmp-wedge", kind="figure", sec="4.4",
         cases=[20, 21, 22, 23, 24], epoch="last", plot="advantage_depth_line.py",
         asset="advantage_depthline_W1.pdf", desc="五方法深度线曲线 W1"),
    dict(slug="F12_dl_abl_rect", label="fig:dl-abl-rect", kind="figure", sec="4.5",
         cases=[25, 26, 27, 28], epoch="last", plot="advantage_depth_line.py",
         asset="advantage_depthline_abl_R1.pdf", desc="消融深度线曲线 R1"),
    dict(slug="F13_dl_abl_wedge", label="fig:dl-abl-wedge", kind="figure", sec="4.5",
         cases=[29, 30, 31, 32], epoch="last", plot="advantage_depth_line.py",
         asset="advantage_depthline_abl_W1.pdf", desc="消融深度线曲线 W1"),
    dict(slug="F14_perf_rect", label="fig:perf-rect", kind="figure", sec="4.4",
         cases=[15, 16, 17, 18, 19], epoch="last", plot="regen_method_grid.py",
         asset="perf_grid_R1.pdf", desc="五方法场对比网格 R1"),
    dict(slug="F15_perf_wedge", label="fig:perf-wedge", kind="figure", sec="4.4",
         cases=[20, 21, 22, 23, 24], epoch="last", plot="regen_method_grid.py",
         asset="perf_grid_W1.pdf", desc="五方法场对比网格 W1"),
    dict(slug="F16_abl_rect", label="fig:abl-rect", kind="figure", sec="4.5",
         cases=[25, 26, 27, 28], epoch="last", plot="regen_method_grid.py",
         asset="abl_grid_R1.pdf", desc="消融场对比网格 R1"),
    dict(slug="F17_abl_wedge", label="fig:abl-wedge", kind="figure", sec="4.5",
         cases=[29, 30, 31, 32], epoch="last", plot="regen_method_grid.py",
         asset="abl_grid_W1.pdf", desc="消融场对比网格 W1"),
    dict(slug="F18_mesh_rect", label="fig:mesh-rect", kind="figure", sec="4.6",
         cases=[33, 34, 35], epoch="last", plot="regen_wide_fields.py",
         asset="Case33_R4_TL.pdf|Case34_R7_TL.pdf|Case35_R8_TL.pdf",
         desc="网格无关性 矩形 TL 场"),
    dict(slug="F19_mesh_wedge", label="fig:mesh-wedge", kind="figure", sec="4.6",
         cases=[36, 37, 38], epoch="last", plot="regen_wide_fields.py",
         asset="Case36_W4_TL.pdf|Case37_W7_TL.pdf|Case38_W8_TL.pdf",
         desc="网格无关性 楔形 TL 场"),
    dict(slug="F20_gen_split", label="fig:gen-split", kind="figure", sec="4.7",
         cases=[39, 40, 41, 42], epoch=None, plot="plot_generalization_split.py",
         asset="generalization_split.pdf", desc="泛化训练/外推区划分示意"),
    dict(slug="F21_gen_grid", label="fig:gen-grid", kind="figure", sec="4.7",
         cases=[39, 40], epoch="last", plot="regen_gen_extrap_bigfont.py",
         asset="gen_extrap_R9.pdf|gen_extrap_R10.pdf", desc="矩形外推 TL 场"),
    dict(slug="F22_gen_grid_wedge", label="fig:gen-grid-wedge", kind="figure", sec="4.7",
         cases=[41, 42], epoch="last", plot="regen_gen_extrap_bigfont.py",
         asset="gen_extrap_W9.pdf|gen_extrap_W10.pdf", desc="楔形外推 TL 场"),
    dict(slug="F23_perf", label="fig:perf", kind="figure", sec="4.8",
         cases=[43, 44, 45, 46, 47, 48, 49, 50], epoch=None, plot="build_perf.py",
         asset="perf_summary.pdf", desc="计算性能与可扩展性"),
]

ALL = TABLES + FIGURES


def by_slug(slug):
    for r in ALL:
        if r["slug"] == slug:
            return r
    raise KeyError(slug)


def by_label(label):
    for r in ALL:
        if r["label"] == label:
            return r
    raise KeyError(label)


def of_section(sec):
    return [r for r in ALL if r["sec"] == sec]
