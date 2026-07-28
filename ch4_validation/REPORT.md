# 第 4 章表格与图件核验主报告

- 结论：**PASS** — 3068 项通过 / 0 项失败 / 2 项豁免
- 覆盖：40/40 个对象（全覆盖）
- 核验脚本：34 个，全部通过
- 生成：2026-07-29 01:10:27
- 复现：`python verify.py`

每个对象的逐项明细在 `reports/<脚本名>.md`，本报告只汇总。

## 核验做了什么

表格与图件的印刷值，一律回到原始数据现场重算后比对，不信任任何
中间产物。链路分三层：

1. **源可追溯** — 每个数值都能指到 `Raw_Experimental_Data` 下的
   xlsx / 训练日志 / npz；成图脚本的两份副本须 md5 相同，否则图
   与核验可能分属两份数据。
2. **双渠道交叉** — 同一量在 xlsx 与训练日志里各取一次，先证两个
   渠道自身一致，再与印刷值比对。单渠道对得上不足以排除系统性错误。
3. **口径防漂移** — 插值网格数、插值方法、频率列表、坐标位数这些
   口径参数，从成图脚本源码里现场读出来断言，而非在核验脚本里写
   死。绘图脚本改了口径而图未重绘，这一层会立刻失败。

判定不设数值容差：源值按印刷位数四舍五入后须逐字符相等。容差会
同时掩盖真实偏差和补 0 伪造。

### 四类容易漏掉的检查

以下四项都不会引起编译错误，靠肉眼校对也很难发现，故各自做成独立断言：

**① 正文引用的数值** — 正文里复述的每个数字，既要与表格印刷值逐字符
相同，也要由源数据独立支持。只查前者会漏掉「正文与表格一起错」的情形，
所以两侧都查。

**② 派生数值的口径** — 正文里的倍数、差值、加速比，一律按**表格印刷值**
复算，读者拿表上三位小数就能验证。全精度口径有时会差 0.001（例如
`5.007779 − 3.174378 = 1.833` 而印刷值口径得 `1.834`），报告里两个口径
都写出来并说明取哪个，不做静默取舍。

**③ best epoch 与 last epoch** — 精度表取 best epoch，场图与深度线图取
ep200(last)，二者**本是不同轮次**（Case 14 的 best=129 与 last=200 差 71
轮）。所以判据是双侧的：caption 含 `last` **且** 不含 `best`，并把各 case
的 best 与 200 的差异列进报告。只查「含 last」的话，把 caption 改成
`best` 也照样通过。深度线族的表与图同取 last，判据相应改为「两侧声明
必须一致」，不能照搬场图族的「必然不同」。

**④ 引用完整性** — 本章有四种引用形式：散文单点、散文区间
（`Figs.~\ref{A}--\ref{B}`，中间各图自身 `\ref` 计数为 0）、散文并列、
表格 Fig. 列（`\ref{fig}\subref{sub}`）。只按单点统计会把区间内部的图
误判为漏引。跨对象核验用两级判据：宽判「是否被引」，严判「figure/table
环境**之外**是否有独立 `\ref`」——后者堵死靠区间或 caption 兜底的路径。

## 覆盖矩阵

| 对象 | 编号 | 类型 | 节 | 核验项 | 结论 | 明细 |
|---|---|---|---|---|---|---|
| `T03_datasets` | tab:datasets | table | 4.1 | 303 | PASS | [T03_datasets](reports/T03_datasets.md) |
| `T04_ideal_overall` | tab:ideal-overall | table | 4.2 | 87 | PASS | [T04_ideal_overall](reports/T04_ideal_overall.md) |
| `T05_ideal_depthline` | tab:ideal-depthline | table | 4.2 | 42 | PASS | [T05_ideal_depthline](reports/T05_ideal_depthline.md) |
| `T06_res_rect_mf` | tab:res-rect-mf | table | 4.3 | 277 | PASS | [T06_res_rect_mf](reports/T06_res_rect_mf.md) |
| `T07_res_rect_100` | tab:res-rect-100 | table | 4.3 | 80 | PASS | [T07_res_rect_100](reports/T07_res_rect_100.md) |
| `T08_res_wedge_100` | tab:res-wedge-100 | table | 4.3 | 90 | PASS | [T08_res_wedge_100](reports/T08_res_wedge_100.md) |
| `T09_dl_cmp_rect` | tab:dl-cmp-rect | table | 4.4 | 100 | PASS | [T09_dl_cmp_rect](reports/T09_dl_cmp_rect.md) |
| `T10_dl_cmp_wedge` | tab:dl-cmp-wedge | table | 4.4 | 97 | PASS | [T10_dl_cmp_wedge](reports/T10_dl_cmp_wedge.md) |
| `T11_dl_abl_rect` | tab:dl-abl-rect | table | 4.5 | 85 | PASS | [T11_dl_abl_rect](reports/T11_dl_abl_rect.md) |
| `T12_dl_abl_wedge` | tab:dl-abl-wedge | table | 4.5 | 86 | PASS | [T12_dl_abl_wedge](reports/T12_dl_abl_wedge.md) |
| `T13_perf_rect` | tab:perf-rect | table | 4.4 | 194 | PASS | [T13_perf_rect](reports/T13_perf_rect.md) |
| `T14_perf_wedge` | tab:perf-wedge | table | 4.4 | 198 | PASS | [T14_perf_wedge](reports/T14_perf_wedge.md) |
| `T15_abl_rect` | tab:abl-rect | table | 4.5 | 118 | PASS | [T15_abl_rect](reports/T15_abl_rect.md) |
| `T16_abl_wedge` | tab:abl-wedge | table | 4.5 | 118 | PASS | [T16_abl_wedge](reports/T16_abl_wedge.md) |
| `T17_mesh_rect` | tab:mesh-rect | table | 4.6 | 55 | PASS | [T17_mesh_rect](reports/T17_mesh_rect.md) |
| `T18_mesh_wedge` | tab:mesh-wedge | table | 4.6 | 55 | PASS | [T18_mesh_wedge](reports/T18_mesh_wedge.md) |
| `T19_gen_overall` | tab:gen-overall | table | 4.7 | 118 | PASS | [T19_gen_overall](reports/T19_gen_overall.md) |
| `T20_runtime` | tab:runtime | table | 4.8 | 47 | PASS | [T20_runtime](reports/T20_runtime.md) |
| `T21_runtime_scale` | tab:runtime-scale | table | 4.8 | 41 | PASS | [T21_runtime_scale](reports/T21_runtime_scale.md) |
| `F03_ideal_rect` | fig:ideal-rect | figure | 4.2 | 37 | PASS | [FIG03_ideal_rect](reports/FIG03_ideal_rect.md) |
| `F04_ideal_wedge` | fig:ideal-wedge | figure | 4.2 | 38 | PASS | [FIG04_ideal_wedge](reports/FIG04_ideal_wedge.md) |
| `F05_res_128` | fig:res-128 | figure | 4.3 | 94 | PASS | [FIG05_07_res_fields](reports/FIG05_07_res_fields.md) |
| `F06_res_256` | fig:res-256 | figure | 4.3 | 94 | PASS | [FIG05_07_res_fields](reports/FIG05_07_res_fields.md) |
| `F07_res_512` | fig:res-512 | figure | 4.3 | 94 | PASS | [FIG05_07_res_fields](reports/FIG05_07_res_fields.md) |
| `F08_res_rect_100` | fig:res-rect-100 | figure | 4.3 | 86 | PASS | [FIG08_09_res_100](reports/FIG08_09_res_100.md) |
| `F09_res_wedge_100` | fig:res-wedge-100 | figure | 4.3 | 86 | PASS | [FIG08_09_res_100](reports/FIG08_09_res_100.md) |
| `F10_dl_cmp_rect` | fig:dl-cmp-rect | figure | 4.4 | 38 | PASS | [FIG10_11_dl_cmp](reports/FIG10_11_dl_cmp.md) |
| `F11_dl_cmp_wedge` | fig:dl-cmp-wedge | figure | 4.4 | 38 | PASS | [FIG10_11_dl_cmp](reports/FIG10_11_dl_cmp.md) |
| `F12_dl_abl_rect` | fig:dl-abl-rect | figure | 4.5 | 44 | PASS | [FIG12_13_dl_abl](reports/FIG12_13_dl_abl.md) |
| `F13_dl_abl_wedge` | fig:dl-abl-wedge | figure | 4.5 | 44 | PASS | [FIG12_13_dl_abl](reports/FIG12_13_dl_abl.md) |
| `F14_perf_rect` | fig:perf-rect | figure | 4.4 | 60 | PASS | [FIG14_15_perf_grid](reports/FIG14_15_perf_grid.md) |
| `F15_perf_wedge` | fig:perf-wedge | figure | 4.4 | 60 | PASS | [FIG14_15_perf_grid](reports/FIG14_15_perf_grid.md) |
| `F16_abl_rect` | fig:abl-rect | figure | 4.5 | 62 | PASS | [FIG16_17_abl_grid](reports/FIG16_17_abl_grid.md) |
| `F17_abl_wedge` | fig:abl-wedge | figure | 4.5 | 62 | PASS | [FIG16_17_abl_grid](reports/FIG16_17_abl_grid.md) |
| `F18_mesh_rect` | fig:mesh-rect | figure | 4.6 | 106 | PASS | [FIG18_19_mesh](reports/FIG18_19_mesh.md) |
| `F19_mesh_wedge` | fig:mesh-wedge | figure | 4.6 | 106 | PASS | [FIG18_19_mesh](reports/FIG18_19_mesh.md) |
| `F20_gen_split` | fig:gen-split | figure | 4.7 | 52 | PASS | [FIG20_gen_split](reports/FIG20_gen_split.md) |
| `F21_gen_grid` | fig:gen-grid | figure | 4.7 | 54 | PASS | [FIG21_22_gen_extrap](reports/FIG21_22_gen_extrap.md) |
| `F22_gen_grid_wedge` | fig:gen-grid-wedge | figure | 4.7 | 54 | PASS | [FIG21_22_gen_extrap](reports/FIG21_22_gen_extrap.md) |
| `F23_perf` | fig:perf | figure | 4.8 | 54 | PASS | [FIG23_perf](reports/FIG23_perf.md) |

## 跨对象核验

这些检查不属于任何单个表或图，只能在全局做。

| 检查 | 核验项 | 结论 | 明细 |
|---|---|---|---|
| Tables 13-16 等宽版式一致性 | 23 | PASS | [T13_16_layout](reports/T13_16_layout.md) |
| 全章表格引用完整性（无孤表/无悬空/独立正文引用） | 65 | PASS | [TABALL_refs](reports/TABALL_refs.md) |
| 全章图件引用完整性（无孤图/无悬空/独立正文引用） | 66 | PASS | [FIGALL_refs](reports/FIGALL_refs.md) |

## 已知缺口

如实记录三处，避免读者以为核验是全覆盖的：

1. **Fig 23 的数值是硬编码在成图脚本里的。** 成图脚本
   `build_perf_figure.py` 不读 xlsx，而是把 thr/spd/nodes/time 四组常量
   写在源码中。故这张图的风险不是「图与脚本不一致」，而是「脚本常量与
   表值脱钩」——表更新而常量未同步，图会静默过期。核验用 ast 解析源码
   取出这 12 个常量与 xlsx 逐值比对，堵住这条路径。

2. **场图与深度线族的取样口径不同。** 场图族（Figs 14-17、21-22）用
   `pick_rows` 取每频率前 2 个样本，caption 写 "the first two"；
   深度线族（Figs 3-4）用 `pick_two` 按深度线 MAE 择优，caption 写
   "best-matching ... ordered by depth-line MAE"。两者都不是代表性
   抽样，故图上名次不代表全测试集——Fig 16/17 的中段名次与 Tables 15/16
   不同即源于此，已在其 caption 中说明。

3. **图上误差与表格 TL 不可互相反算。** 图上 `Avg` 是单样本场误差均值，
   表里的 TL 是全测试集平均，样本集不同。故只核排序或端点是否同向，
   不核数值相等。五方法组两侧完整排序一致；四变体组仅端点一致，中段
   名次因聚合口径而互换，属正常。

## 目录结构

```
ch4_validation/
├── verify.py              主程序：跑全部核验并生成本报告
├── REPORT.md              本报告（自动生成）
├── common/                共用层
│   ├── paths.py           数据与 tex 路径解析
│   ├── registry.py        40 个对象的注册表（19 表 + 21 图）
│   ├── metrics.py         xlsx / 训练日志取数与舍入比对
│   ├── depthline.py       深度线组重算（复用成图脚本自身函数）
│   ├── texparse.py        tex/aux 解析：表体、caption、label、引用
│   └── report.py          Checker：断言累积与 Markdown 渲染
├── scripts/               表格核验，一表一脚本
├── scripts_figures/       图件核验，同版式的图合并为一份
└── reports/               各对象的逐项明细（自动生成）
```

