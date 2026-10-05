# 第 4 章表格与图件核验主报告

- 结论：**PASS** — 3362 项通过 / 0 项失败 / 16 项豁免
- 覆盖：23/23 个对象（全覆盖）
- 核验脚本：28 个，全部通过
- 生成：2026-10-05 21:31:06
- 复现：`python verify.py`

每个对象的逐项明细在 `reports/<脚本名>.md`，本报告只汇总。

## 核验做了什么

表格与图件的印刷值，一律回到原始数据现场重算后比对，不信任任何
中间产物。链路分三层：

1. **源可追溯** — 每个数值都能指到 `Raw_Experimental_Data` 下的
   xlsx / 训练日志 / npz。成图脚本按图号收在 `Validation_Scripts/
   figNN_*/`（R1 整理后的布局，一份脚本一个目录），核验从该脚本
   自身的源码读口径，并核 paper 图件与其产物的一致（PDF 的字节
   md5 因 matplotlib 每次都写新的 /CreationDate 而必然不同，故比对
   时剥掉时间戳字段；该约定在各脚本里显式登记为豁免，不隐去）。
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

**④ 引用完整性** — R1 把矩形与楔形合并后，正文对每张图/表**各写一次**
`\ref`（含 `Fig.~\ref{fig:perf}(a,b)` 这类面板后缀），不再使用区间引用
`Figs.~\ref{A}--\ref{B}`。跨对象核验仍用两级判据：宽判「是否被引」，
严判「figure/table 环境**之外**是否有独立 `\ref`」——后者堵死靠 caption
交叉引用兜底的路径；对已从正文删除的对象（无 label）另行登记豁免。

## 覆盖矩阵

| 对象 | 编号 | 类型 | 节 | 核验项 | 结论 | 明细 |
|---|---|---|---|---|---|---|
| `T03_datasets` | tab:datasets | table | 4.1 | 423 | PASS | [T03_datasets](reports/T03_datasets.md) |
| `T04_ideal_overall` | tab:ideal-overall | table | 4.2 | 87 | PASS | [T04_ideal_overall](reports/T04_ideal_overall.md) |
| `TS1_ideal_depthline` | tab:S1 | table | 4.2 | 51 | PASS | [TS1_ideal_depthline](reports/TS1_ideal_depthline.md) |
| `T05_res_rect_mf` | tab:res-rect-mf | table | 4.3 | 263 | PASS | [T05_res_rect_mf](reports/T05_res_rect_mf.md) |
| `T06_sq100` | tab:sq100 | table | 4.3 | 139 | PASS | [T06_sq100](reports/T06_sq100.md) |
| `T07_dl_cmp` | tab:dl-cmp | table | 4.4 | 174 | PASS | [T07_dl_cmp](reports/T07_dl_cmp.md) |
| `T08_dl_abl` | tab:dl-abl | table | 4.5 | 157 | PASS | [T08_dl_abl](reports/T08_dl_abl.md) |
| `T09_perf_cmp` | tab:perf-cmp | table | 4.4 | 408 | PASS | [T09_perf_cmp](reports/T09_perf_cmp.md) |
| `T10_abl` | tab:abl | table | 4.5 | 344 | PASS | [T10_abl](reports/T10_abl.md) |
| `T11_mesh` | tab:mesh | table | 4.6 | 113 | PASS | [T11_mesh](reports/T11_mesh.md) |
| `T12_gen_overall` | tab:gen-overall | table | 4.7 | 118 | PASS | [T12_gen_overall](reports/T12_gen_overall.md) |
| `T13_runtime` | tab:runtime | table | 4.8 | 92 | PASS | [T13_runtime](reports/T13_runtime.md) |
| `F03_ideal` | fig:ideal | figure | 4.2 | 37 | PASS | [FIG03_ideal](reports/FIG03_ideal.md) |
| `F04_res_128` | fig:res-128 | figure | 4.3 | 51 | PASS | [FIG04_res_128](reports/FIG04_res_128.md) |
| `F05_sq100` | fig:sq100 | figure | 4.3 | 113 | PASS | [FIG05_sq100](reports/FIG05_sq100.md) |
| `F06_dl_cmp` | fig:dl-cmp | figure | 4.4 | 74 | PASS | [FIG06_dl_cmp](reports/FIG06_dl_cmp.md) |
| `F07_dl_abl` | fig:dl-abl | figure | 4.5 | 79 | PASS | [FIG07_dl_abl](reports/FIG07_dl_abl.md) |
| `F08_perf_cmp_r` | fig:perf-cmp-r | figure | 4.4 | 91 | PASS | [FIG08_09_perf_cmp](reports/FIG08_09_perf_cmp.md) |
| `F09_perf_cmp_w` | fig:perf-cmp-w | figure | 4.4 | 91 | PASS | [FIG08_09_perf_cmp](reports/FIG08_09_perf_cmp.md) |
| `F10_mesh` | fig:mesh | figure | 4.6 | 113 | PASS | [FIG10_mesh](reports/FIG10_mesh.md) |
| `F11_gen_split` | fig:gen-split | figure | 4.7 | 52 | PASS | [FIG11_gen_split](reports/FIG11_gen_split.md) |
| `F12_gen_grid` | fig:gen-grid | figure | 4.7 | 58 | PASS | [FIG12_gen_extrap](reports/FIG12_gen_extrap.md) |
| `F13_perf` | fig:perf | figure | 4.8 | 54 | PASS | [FIG13_perf](reports/FIG13_perf.md) |

## 跨对象核验

这些检查不属于任何单个表或图，只能在全局做。

| 检查 | 核验项 | 结论 | 明细 |
|---|---|---|---|
| Tables 9-10 等宽版式一致性 | 16 | PASS | [T09_10_layout](reports/T09_10_layout.md) |
| 全章表格引用完整性（无孤表/无悬空/独立正文引用） | 42 | PASS | [TABALL_refs](reports/TABALL_refs.md) |
| 全章图件引用完整性（无孤图/无悬空/独立正文引用） | 36 | PASS | [FIGALL_refs](reports/FIGALL_refs.md) |
| 补充材料 Figs. S1-S7：图上数值↔npz、印刷字号、正文/回复信交叉引用 | 65 | PASS | [FIGS1_S7_supplementary](reports/FIGS1_S7_supplementary.md) |
| 从正文出发：每个小数须为本节所引表的印刷值（括注 Case 则须在该行）、推导量或配置 | 109 | PASS | [PROSE_numbers](reports/PROSE_numbers.md) |
| 正文中不挂靠表/图的数值：超参数↔代码、三维推导量、样本数、基线门槛 | 20 | PASS | [PROSE_derived](reports/PROSE_derived.md) |

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
│   ├── registry.py        23 个对象的注册表（12 表 + 11 图）
│   ├── metrics.py         xlsx / 训练日志取数与舍入比对
│   ├── depthline.py       深度线组重算（复用成图脚本自身函数）
│   ├── texparse.py        tex/aux 解析：表体、caption、label、引用
│   └── report.py          Checker：断言累积与 Markdown 渲染
├── scripts/               表格核验，一表一脚本
├── scripts_figures/       图件核验，同版式的图合并为一份
└── reports/               各对象的逐项明细（自动生成）
```

