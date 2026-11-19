# Table — — 正文推导与独立数值（不挂靠表/图）

- 对象：`prose`（Table —）
- 结论：**PASS** — 19 通过 / 0 失败 / 0 警告，共 19 项
- 脚本：`ch4_validation/scripts/PROSE_derived.py`
- 生成：2026-11-19 23:50:11

## 1. 源清单

| 角色 | 路径 | 说明 |
|---|---|---|
| 印刷面 tex | `../JASA/OE期刊/paper_R2/OE_submission.tex` | 4.1 / 4.4 节与第 5 章正文 |
| 训练代码 | `OceanAcoustic-FNO-FEM_github/Experiment_Code/Main_Code/ocean_trainer_forward_b.py` | 学习率调度、通道宽度 |
| 模型代码 | `OceanAcoustic-FNO-FEM_github/Experiment_Code/Main_Code/deq_modules/models.py` | FNO 网格/模态/层数 |
| 运行时 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.8_Performance/Case43-50_推理时间性能分析.xlsx` | 网格节点数（Table 13 同源） |
| 精度 xlsx | `Data_and_Code_Availability/Raw_Experimental_Data/4.4_Comparison/Case15-24_数据汇总.xlsx` | 基线 TL（Table 9 同源） |

## 1. 4.1 节超参数 ↔ 训练代码默认值

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| γ (ExponentialLR)：代码 `0.995` / 正文 `\gamma=0.995` | 代码默认值与正文一致 | PASS |
| G (FNO 网格)：代码 `64` / 正文 `$G=64$` | 代码默认值与正文一致 | PASS |
| W (通道宽度)：代码 `48` / 正文 `$W=48$` | 代码默认值与正文一致 | PASS |
| L (Fourier 层数)：代码 `4` / 正文 `$L=4$` | 代码默认值与正文一致 | PASS |
| m1=m2 (保留模态)：代码 `16` / 正文 `$m_1=m_2=16$` | 代码默认值与正文一致 | PASS |

## 2. 第 5 章三维代价段：推导量现场重算（节点数取自 4.8 节 xlsx）

> R2 结论删去了 R1 的三个具体推导量（每层模态张量 5.9×10^5、三维每层权重 9.4×10^6、FFT 代价 96 倍），只保留 O(G²logG)→O(G³logG) 的量级陈述；故不再断言那三个数，改核量级陈述本身在正文中。

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 最大网格节点数 N = 337,351（xlsx）出现在正文 | Lx = 512 m | PASS |
| 三维节点数 N^{3/2}（R2 正文取 2 位有效数字） | `337351^1.5 = 1.9594e+08` → `2.0\times10^{8}` | PASS |
| FFT 代价陈述 O(G²logG) → O(G³logG) 在正文中 |  | PASS |

## 3. 参考解数量 ↔ Table 3

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 全部 32 个多频算例 N = 8000 |  | PASS |
| 全部 50 个算例每频 2000 |  | PASS |
| 18 个单频算例 N = 2000（故不能写成『每个算例 8000』） |  | PASS |
| 结论限定为『每个多频算例 8000 个有限元解』（不写成每个算例） |  | PASS |
| 4.1 节写明每频 2000 个声源位置 |  | PASS |
| 正文不再有『每个算例 8000』的旧说法 |  | PASS |

## 4. 4.4 节基线 TL 门槛 ↔ 精度 xlsx

| 检查项 | 源值 / 印刷值 | 结论 |
|---|---|---|
| 矩形 R1 DeepONet 平均 TL > 2.6 dB | `3.484` | PASS |
| 矩形 R1 KNO 平均 TL > 2.6 dB | `2.738` | PASS |
| 矩形 R1 CNO 平均 TL > 2.6 dB | `2.634` | PASS |
| FNO 不在此列（正文单独给出 1.305 dB） | `1.305` | PASS |
| 正文门槛字面量 2.6 |  | PASS |

