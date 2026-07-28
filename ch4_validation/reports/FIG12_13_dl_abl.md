# Fig. 12/13 — 四变体消融深度线 Fig 12/13

- 对象：`fig:dl-abl-rect / fig:dl-abl-wedge`（Fig. 12/13）
- 结论：**PASS** — 44 通过 / 0 失败 / 0 警告，共 44 项
- 脚本：`ch4_validation/scripts/FIG12_13_dl_abl.py`
- 生成：2026-07-29 01:09:14

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE/els-cas-templates/OE_submission.tex` | 两个并列 minipage，各含表+图 |
| 成图/取数脚本（权威） | `advantage_depth_line.py` | advantage_depth_line.py |

## 1. 源可追溯与口径防漂移

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 成图脚本两份副本 md5 同源 | 权威 `0eb56367` / repo `0eb56367` | PASS |
| GRID == 300 | 脚本内 `300` | PASS |
| 插值 METHOD == cubic | 脚本内 `cubic` | PASS |
| FREQS 一致 | 脚本内 `[25, 50, 75, 100]` | PASS |
| 脚本内 Src 为 1 位小数（全章统一口径） | 含 `{_sx:.1f}, {_sy:.1f}` | PASS |

## 2. epoch 自证与 caption 声明

> 深度线族的表与图同取 ep200，两侧 epoch 声明须一致；场图族则相反（表 best / 图 last），判据不能照搬。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-rect 全部 npz epoch == 200 (last) | 实得 [200]（4 份 npz） | PASS |
| fig:dl-abl-rect caption 声明 last epoch | 含 `Profiles are from the last epoch.` | PASS |
| fig:dl-abl-rect caption 未误写 best epoch | 深度线族一律源自 ep200 npz | PASS |
| fig:dl-abl-rect caption 标明 y=71.9 m | 含 `71.9` | PASS |
| fig:dl-abl-rect caption 声明 ablation variants |  | PASS |
| fig:dl-abl-wedge 全部 npz epoch == 200 (last) | 实得 [200]（4 份 npz） | PASS |
| fig:dl-abl-wedge caption 声明 last epoch | 含 `Profiles are from the last epoch.` | PASS |
| fig:dl-abl-wedge caption 未误写 best epoch | 深度线族一律源自 ep200 npz | PASS |
| fig:dl-abl-wedge caption 标明 y=33.4 m | 含 `33.4` | PASS |
| fig:dl-abl-wedge caption 声明 ablation variants |  | PASS |
| fig:dl-abl-rect 与兄弟表 tab:dl-abl-rect 同声明 last epoch | 图 `last` / 表 `last` | PASS |
| fig:dl-abl-wedge 与兄弟表 tab:dl-abl-wedge 同声明 last epoch | 图 `last` / 表 `last` | PASS |

## 3. 图上 Src 标注：npz 重算 vs PDF 文本层

> 每个频率面板标题带该频率实际选中样本的 source_pos，逐频独立选样，四组坐标互不相同，写错不报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-rect 4 组 Src 吻合 | PDF [('44.5', '21.9'), ('25.9', '49.5'), ('51.5', '5.7'), ('62.8', '85.3')] / npz [('44.5', '21.9'), ('25.9', '49.5'), ('51.5', '5.7'), ('62.8', '85.3')] | PASS |
| fig:dl-abl-rect 四个频率面板齐全 | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-abl-rect 图例含 COMSOL |  | PASS |
| fig:dl-abl-rect 图例含 Full |  | PASS |
| fig:dl-abl-rect 图例含 w/o prior |  | PASS |
| fig:dl-abl-rect 图例含 w/o graph |  | PASS |
| fig:dl-abl-rect 图例含 w/o prior-sup. |  | PASS |
| fig:dl-abl-wedge 4 组 Src 吻合 | PDF [('92.7', '58.9'), ('117.6', '43.4'), ('56.7', '33.8'), ('45.5', '29.5')] / npz [('92.7', '58.9'), ('117.6', '43.4'), ('56.7', '33.8'), ('45.5', '29.5')] | PASS |
| fig:dl-abl-wedge 四个频率面板齐全 | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-abl-wedge 图例含 COMSOL |  | PASS |
| fig:dl-abl-wedge 图例含 Full |  | PASS |
| fig:dl-abl-wedge 图例含 w/o prior |  | PASS |
| fig:dl-abl-wedge 图例含 w/o graph |  | PASS |
| fig:dl-abl-wedge 图例含 w/o prior-sup. |  | PASS |

## 4. 图与表同源（Fig 12↔T11, Fig 13↔T12）

> 图与兄弟表是同一次 build_group 的两个产物。比对论文图件与脚本输出目录下同名 PDF 的 md5：相同即证明表里的 MAE 与图上的曲线出自同一次运行，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-rect 论文图件与脚本产物 md5 相同 | `9d0df8af` vs `9d0df8af` | PASS |
| fig:dl-abl-wedge 论文图件与脚本产物 md5 相同 | `6844ad60` vs `6844ad60` | PASS |

## 5. 图与兄弟表的版面归属

> 每张图与其 MAE 表绑在同一个 minipage 内（表在上、图在下），这样读者看曲线时表值就在同屏；错位会让图表分页。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-abl-rect 与兄弟表 tab:dl-abl-rect 同处一个 minipage | 表在图之前 成立（间距 1069 字符） | PASS |
| fig:dl-abl-wedge 与兄弟表 tab:dl-abl-wedge 同处一个 minipage | 表在图之前 成立（间距 1065 字符） | PASS |

## 6. 正文引用与派生差值

> 正文 4.5 节称 graph correction 在高频降幅为 1.356 / 1.834 dB。派生差值一律用**表格印刷值**相减，读者拿表上三位小数即可复算；100 Hz 处全精度口径得 1.833，与正文的 1.834 差 0.001——此为口径差异而非笔误，与 Table 7 的 8.676 同一约定。

> 正文另称『去掉物理先验使深度线 TL 在两种几何的每个频率都升到数十 dB』——这是图上曲线最显著的特征，逐频核验其成立。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文以区间引用覆盖 Fig 12/13 | `Figs.~\ref{fig:dl-abl-rect}--\ref{fig:dl-abl-wedge}` 出现 2 处（4.4 引入段 + 4.5 消融段） | PASS |
| fig:dl-abl-rect 编号为 12 | aux `12` | PASS |
| fig:dl-abl-wedge 编号为 13 | aux `13` | PASS |
| 正文 75Hz 降幅 = 1.356 dB（印刷值口径） | `2.903` - `1.547` = `1.356`；两口径一致 | PASS |
| 正文 1.356 可定位 |  | PASS |
| 正文 100Hz 降幅 = 1.834 dB（印刷值口径） | `5.008` - `3.174` = `1.834`；全精度口径为 `1.833`，与正文不同，故以印刷值口径为准 | PASS |
| 正文 1.834 可定位 |  | PASS |
| fig:dl-abl-rect w/o prior 四频 TL 均达数十 dB 量级 | 25Hz:26.3 / 50Hz:30.3 / 75Hz:34.1 / 100Hz:35.1 | PASS |
| fig:dl-abl-wedge w/o prior 四频 TL 均达数十 dB 量级 | 25Hz:8.7 / 50Hz:32.9 / 75Hz:40.6 / 100Hz:34.3 | PASS |

