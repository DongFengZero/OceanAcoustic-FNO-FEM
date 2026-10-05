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
         cases=list(range(1, 51)), epoch=None,
         desc="数据集总表 No.1-50（结构性，非测量值）"),
    dict(slug="T04_ideal_overall", label="tab:ideal-overall", kind="table",
         sec="4.2", cases=[1, 2], epoch="best", desc="解析解场精度 R0/W0"),
    dict(slug="T05_res_rect_mf", label="tab:res-rect-mf", kind="table",
         sec="4.3", cases=[3, 4, 5, 9, 10, 11], epoch="best",
         desc="多频前向精度 R1-R3/W1-W3（矩形与楔形同表）"),
    dict(slug="T06_sq100", label="tab:sq100", kind="table", sec="4.3",
         cases=[6, 7, 8, 12, 13, 14], epoch="best",
         desc="100Hz 方形域精度 R4-R6/W4-W6（矩形与楔形并排）"),
    dict(slug="T07_dl_cmp", label="tab:dl-cmp", kind="table", sec="4.4",
         cases=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24], epoch="last",
         plot="fig06_07_dl/fig06_07_dl.py",
         desc="五方法深度线 TL（矩形 R1 y=56.1m 与楔形 W1 y=30.4m 并排）"),
    dict(slug="T08_dl_abl", label="tab:dl-abl", kind="table", sec="4.5",
         cases=[25, 26, 27, 28, 29, 30, 31, 32], epoch="last",
         plot="fig06_07_dl/fig06_07_dl.py",
         desc="消融深度线 TL（矩形 y=71.9m 与楔形 y=33.4m 并排）"),
    dict(slug="T09_perf_cmp", label="tab:perf-cmp", kind="table", sec="4.4",
         cases=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24], epoch="best",
         desc="五方法逐频精度，矩形与楔形分块同表"),
    dict(slug="T10_abl", label="tab:abl", kind="table", sec="4.5",
         cases=[25, 26, 27, 28, 29, 30, 31, 32], epoch="best",
         desc="消融逐频结果，矩形与楔形分块同表"),
    dict(slug="T11_mesh", label="tab:mesh", kind="table", sec="4.6",
         cases=[33, 34, 35, 36, 37, 38], epoch="best",
         desc="网格无关性，矩形与楔形并排"),
    dict(slug="T12_gen_overall", label="tab:gen-overall", kind="table",
         sec="4.7", cases=[39, 40, 41, 42], epoch="best",
         desc="泛化外推精度 R9/R10/W9/W10"),
    dict(slug="T13_runtime", label="tab:runtime", kind="table", sec="4.8",
         cases=[43, 44, 45, 46, 47, 48, 49, 50], epoch=None,
         desc="推理耗时：多 GPU 基准(a) 与跨域尺度(b) 同表"),
]

FIGURES = [
    dict(slug="F03_ideal", label="fig:ideal", kind="figure", sec="4.2",
         cases=[1, 2], epoch="last", plot="fig03_ideal/fig03_ideal.py",
         asset="Case01_R0_grid2.pdf|Case02_W0_grid2.pdf",
         desc="R0/W0 解析解验证（矩形与楔形合并为一张）"),
    dict(slug="F04_res_128", label="fig:res-128", kind="figure", sec="4.3",
         cases=[3, 9], epoch="last", plot="fig04_05_10_fields/fig04_05_10_fields.py",
         asset="Case03_R1_TL.pdf|Case09_W1_TL.pdf", desc="128x128 TL 场"),
    dict(slug="F05_sq100", label="fig:sq100", kind="figure", sec="4.3",
         cases=[6, 7, 8, 12, 13, 14], epoch="last",
         plot="fig04_05_10_fields/fig04_05_10_fields.py",
         asset=("Case06_R4_TL.pdf|Case07_R5_TL.pdf|Case08_R6_TL.pdf|"
                "Case12_W4_TL.pdf|Case13_W5_TL.pdf|Case14_W6_TL.pdf"),
         desc="100Hz 方形域 TL 场（矩形与楔形合并为一张）"),
    dict(slug="F06_dl_cmp", label="fig:dl-cmp", kind="figure", sec="4.4",
         cases=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24], epoch="last",
         plot="fig06_07_dl/fig06_07_dl.py",
         asset=("comparison_R1_model_advantage.pdf|comparison_W1_model_advantage.pdf|"
                "dl_legend_cmp.pdf"),
         desc="五方法深度线 TL（矩形与楔形合并为一张）"),
    dict(slug="F07_dl_abl", label="fig:dl-abl", kind="figure", sec="4.5",
         cases=[25, 26, 27, 28, 29, 30, 31, 32], epoch="last",
         plot="fig06_07_dl/fig06_07_dl.py",
         asset=("ablation_R1_module_advantage.pdf|ablation_W1_module_advantage.pdf|"
                "dl_legend_abl.pdf"),
         desc="消融变体深度线 TL（矩形与楔形合并为一张）"),
    dict(slug="F08_perf_cmp_r", label="fig:perf-cmp-r", kind="figure", sec="4.4",
         cases=[15, 16, 17, 18, 19], epoch="last",
         plot="fig08_09_perf_grid/fig08_09_perf_grid.py",
         asset="perf_grid_R1.pdf", desc="五方法场对比网格 R1"),
    dict(slug="F09_perf_cmp_w", label="fig:perf-cmp-w", kind="figure", sec="4.4",
         cases=[20, 21, 22, 23, 24], epoch="last",
         plot="fig08_09_perf_grid/fig08_09_perf_grid.py",
         asset="perf_grid_W1.pdf", desc="五方法场对比网格 W1"),
    dict(slug="F10_mesh", label="fig:mesh", kind="figure", sec="4.6",
         cases=[33, 34, 35, 36, 37, 38], epoch="last",
         plot="fig04_05_10_fields/fig04_05_10_fields.py",
         asset=("Case33_R4_TL.pdf|Case34_R7_TL.pdf|Case35_R8_TL.pdf|"
                "Case36_W4_TL.pdf|Case37_W7_TL.pdf|Case38_W8_TL.pdf"),
         desc="网格无关性 TL 场（矩形与楔形合并为一张）"),
    dict(slug="F11_gen_split", label="fig:gen-split", kind="figure", sec="4.7",
         cases=[39, 40, 41, 42], epoch=None,
         plot="fig11_gen_split/fig11_gen_split.py",
         asset="generalization_split.pdf", desc="泛化训练/外推区划分示意"),
    dict(slug="F12_gen_grid", label="fig:gen-grid", kind="figure", sec="4.7",
         cases=[39, 42], epoch="last",
         plot="fig04_05_10_fields/fig04_05_10_fields.py",
         asset="gen_extrap_R9.pdf|gen_extrap_W10.pdf",
         desc="源位置外推 TL 场（矩形 R9 深区 + 楔形 W10 远区；R10/W9 在补充材料 Fig. S7）"),
    dict(slug="F13_perf", label="fig:perf", kind="figure", sec="4.8",
         cases=[43, 44, 45, 46, 47, 48, 49, 50], epoch=None,
         plot="fig13_perf/fig13_perf.py",
         asset="perf_merged.pdf", desc="计算性能与可扩展性"),
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
