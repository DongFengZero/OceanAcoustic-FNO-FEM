# Fig. 10/11 — 五方法深度线对比 Fig 10/11

- 对象：`fig:dl-cmp-rect / fig:dl-cmp-wedge`（Fig. 10/11）
- 结论：**PASS** — 38 通过 / 0 失败 / 0 警告，共 38 项
- 脚本：`ch4_validation/scripts/FIG10_11_dl_cmp.py`
- 生成：2026-07-30 00:06:00

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
| fig:dl-cmp-rect 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| fig:dl-cmp-rect caption 声明 last epoch | 含 `Profiles are from the last epoch.` | PASS |
| fig:dl-cmp-rect caption 未误写 best epoch | 深度线族一律源自 ep200 npz | PASS |
| fig:dl-cmp-rect caption 标明 y=56.1 m | 含 `56.1` | PASS |
| fig:dl-cmp-rect caption 声明 five methods |  | PASS |
| fig:dl-cmp-wedge 全部 npz epoch == 200 (last) | 实得 [200]（5 份 npz） | PASS |
| fig:dl-cmp-wedge caption 声明 last epoch | 含 `Profiles are from the last epoch.` | PASS |
| fig:dl-cmp-wedge caption 未误写 best epoch | 深度线族一律源自 ep200 npz | PASS |
| fig:dl-cmp-wedge caption 标明 y=30.4 m | 含 `30.4` | PASS |
| fig:dl-cmp-wedge caption 声明 five methods |  | PASS |
| fig:dl-cmp-rect 与兄弟表 tab:dl-cmp-rect 同声明 last epoch | 图 `last` / 表 `last` | PASS |
| fig:dl-cmp-wedge 与兄弟表 tab:dl-cmp-wedge 同声明 last epoch | 图 `last` / 表 `last` | PASS |

## 3. 图上 Src 标注：npz 重算 vs PDF 文本层

> 每个频率面板标题带该频率实际选中样本的 source_pos，逐频独立选样，四组坐标互不相同，写错不报编译错。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp-rect 4 组 Src 吻合 | PDF [('44.5', '21.9'), ('25.9', '49.5'), ('120.7', '89.5'), ('77.5', '103.0')] / npz [('44.5', '21.9'), ('25.9', '49.5'), ('120.7', '89.5'), ('77.5', '103.0')] | PASS |
| fig:dl-cmp-rect 四个频率面板齐全 | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-cmp-rect 图例含 COMSOL |  | PASS |
| fig:dl-cmp-rect 图例含 DeepONet |  | PASS |
| fig:dl-cmp-rect 图例含 FNO |  | PASS |
| fig:dl-cmp-rect 图例含 KNO |  | PASS |
| fig:dl-cmp-rect 图例含 CNO |  | PASS |
| fig:dl-cmp-wedge 4 组 Src 吻合 | PDF [('80.7', '72.7'), ('117.6', '43.4'), ('113.4', '64.0'), ('88.0', '78.9')] / npz [('80.7', '72.7'), ('117.6', '43.4'), ('113.4', '64.0'), ('88.0', '78.9')] | PASS |
| fig:dl-cmp-wedge 四个频率面板齐全 | 图上 `['25', '50', '75', '100']` | PASS |
| fig:dl-cmp-wedge 图例含 COMSOL |  | PASS |
| fig:dl-cmp-wedge 图例含 DeepONet |  | PASS |
| fig:dl-cmp-wedge 图例含 FNO |  | PASS |
| fig:dl-cmp-wedge 图例含 KNO |  | PASS |
| fig:dl-cmp-wedge 图例含 CNO |  | PASS |

## 4. 图与表同源（Fig 10↔T9, Fig 11↔T10）

> 图与兄弟表是同一次 build_group 的两个产物。比对论文图件与脚本输出目录下同名 PDF 的 md5：相同即证明表里的 MAE 与图上的曲线出自同一次运行，不可能各自漂移。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp-rect 论文图件与脚本产物 md5 相同 | `e98b21f1` vs `e98b21f1` | PASS |
| fig:dl-cmp-wedge 论文图件与脚本产物 md5 相同 | `67fba98d` vs `67fba98d` | PASS |

## 5. 图与兄弟表的版面归属

> 每张图与其 MAE 表绑在同一个 minipage 内（表在上、图在下），这样读者看曲线时表值就在同屏；错位会让图表分页。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| fig:dl-cmp-rect 与兄弟表 tab:dl-cmp-rect 同处一个 minipage | 表在图之前 成立（间距 1064 字符） | PASS |
| fig:dl-cmp-wedge 与兄弟表 tab:dl-cmp-wedge 同处一个 minipage | 表在图之前 成立（间距 1059 字符） | PASS |

## 6. 正文引用

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 正文以区间引用覆盖 Fig 10/11 | 含 `Figs.~\ref{fig:dl-cmp-rect}--\ref{fig:dl-cmp-wedge}` | PASS |
| fig:dl-cmp-rect 编号为 10 | aux `10` | PASS |
| fig:dl-cmp-wedge 编号为 11 | aux `11` | PASS |

