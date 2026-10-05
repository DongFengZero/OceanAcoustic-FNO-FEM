# ch4_validation — 论文表格与图件的可复现核验

对 R1 论文第 4 章的 **12 张表** 与 **11 张图**（Tables 3--13、Figures 3--13）
做逐值核验：把每一个印刷出来的数字，回到 `Raw_Experimental_Data` 下的原始数据
现场重算一遍，再与 tex 里排出来的值逐字符比对。

表 1--2（缩写表、符号表）与图 1--2（几何示意、方法框图）是描述性对象，不含
测量值，不在核验范围内。

```bash
python verify.py            # 全跑，生成 REPORT.md
```

结果见 [REPORT.md](REPORT.md)，各对象的逐项明细在 `reports/`。

## 为什么不信任中间产物

汇总用的 xlsx 可能是手工整理的，图可能是旧版脚本产的，正文里的数字可能
是从早期草稿抄来的。所以核验不接受任何一方的说法，而是要求多个独立渠道
互相印证：

| 层 | 做法 |
|---|---|
| 源可追溯 | 每个数值都指到 xlsx / 训练日志 / npz；图件与其成图脚本产物一致 |
| 双渠道交叉 | 同一量在 xlsx 与训练日志各取一次，先证两渠道一致，再比印刷值 |
| 口径防漂移 | 插值网格数、插值方法、坐标位数等从成图脚本源码现场读出来断言 |

比对分两层，容差策略不同，不可混为一谈：

- **印刷值 vs. tex 排版值——零容差。** 源值按印刷位数四舍五入后须与排版数字
  逐字符相等。这一层若设容差，会同时掩盖真实偏差和"补 0 伪造"——`1.210`
  到底是真值还是 `1.21` 补的零，只有回到全精度才能判定。
- **源 vs. 源（xlsx vs. 训练日志）——小数值容差。** 同一量从汇总 xlsx 读出、
  又从日志的损失项现场重算，两渠道须一致到相对容差 `2e-6`（绝对下限
  `1e-9`）。二者**不要求逐位相同**：xlsx 存的是为显示已舍入的值，日志侧是
  全精度重算，所以第 7～8 位有效数字可能不同。因此只要求**在表格实际给出的
  有效数字范围内一致**即可——对到这个精度就足以确认两渠道是同一次运行。

## 四类容易漏掉的检查

这四项都不会引起编译错误，肉眼校对也很难发现：

**正文引用的数值.** 正文复述的每个数字，既要与表格印刷值逐字符相同，也要
由源数据独立支持。只查前者会漏掉「正文与表格一起错」。

**派生数值的口径.** 倍数、差值、加速比一律按**表格印刷值**复算，读者拿表
上三位小数就能验证。全精度口径有时差 0.001（`5.007779 − 3.174378 = 1.833`
而印刷值口径得 `1.834`），报告里两个口径都写出来。

**best epoch 与 last epoch.** 精度表取 best epoch，场图与深度线图取
ep200(last)，二者**本是不同轮次**（Case 14 的 best=129 与 last=200 差 71 轮）。
判据是双侧的：caption 含 `last` **且** 不含 `best`。只查「含 last」的话，把
caption 改成 `best` 也照样通过。深度线族的表与图同取 last，判据相应改为
「两侧声明必须一致」。

**引用完整性.** R1 把矩形与楔形合并后，正文对每张图/表**各写一次** `\ref`
（含 `Fig.~\ref{fig:perf}(a,b)` 这类面板后缀），不再使用区间引用
`Figs.~\ref{A}--\ref{B}`。跨对象核验用两级判据：宽判「是否被引」，严判
「figure/table 环境**之外**是否有独立 `\ref`」——后者堵死靠 caption 交叉
引用兜底的路径；对已移入补充材料的对象（无 label）另行登记豁免。

## 核验程序本身如何被检验

核验全部通过，只说明"被检查的部分"没有发现不一致；它不能证明核验程序本身没有漏洞。为此另设两项自检，放在 `selftest/` 下：

**1. 变异测试** `selftest/mutation_test.py`：复制论文目录，每次只植入一处真实可能发生的错误，再运行负责该对象的核验脚本，检查它能否报错。植入的错误类型包括：末位抄错、两行对调、舍入错、少写末位的 0、caption 的 epoch 说法写错、正文引用值写错、推导倍数写错、Table 3 元数据写错，以及放错图件。植入前先运行一遍未改动的副本，确认零误报。

当前结果：**21 个植入错误抓到 20 个**。漏网的是 M21：正文中没有 "(Case~N)" 括注的数，被换成同一张表里另一个合法的印刷值时无法发现，属于已知局限。

**2. 独立重算深度线** `selftest/independent_depthline.py`：核验套件计算深度线时直接调用成图脚本自己的函数，这样能保证口径一致；但如果那个函数本身算错，表、图和核验会"一致地错"。这个脚本与成图脚本、核验套件**不共用任何代码**：
- 自己解析 tex，按表头印出的声源坐标定位样本，按印出的 y 值定位深度线；
- 沿深度线逐点求值插值函数（`CloughTocher2DInterpolator`），不经过整张网格；
- 重算 Table S1、7、8 全部 80 格。

当前结果：**80 格 0 处不符**。敏感性已验证：把障碍物屏蔽倍数从 1.10 改为 1.00，80 格中 72 格不符；把深度线偏移一行，79 格不符。

```bash
python selftest/independent_depthline.py
python selftest/mutation_test.py        # 约 10 分钟；结束后请重跑 verify.py 恢复 reports/
```

## 用法

```bash
python verify.py                 # 全跑并生成 REPORT.md
python verify.py T04 T06         # 只跑指定对象（slug 或 label 子串）
python verify.py --kind figure    # 只跑图 / table
python verify.py --sec 4.3        # 只跑某节
python verify.py --list           # 列出对象与脚本，不执行
```

退出码 0 表示全部通过，便于接进 CI。子集运行不会覆盖 `REPORT.md`。

单个对象也可以直接跑，输出同样落到 `reports/`：

```bash
python scripts/T05_res_rect_mf.py
python scripts_figures/FIG05_sq100.py
```

## 结构

```
ch4_validation/
├── verify.py              主程序：跑全部核验并生成 REPORT.md
├── REPORT.md              主报告（自动生成）
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

`registry.py` 登记全部 23 个对象，是覆盖率的分母——注册了但没有对应脚本
的对象会在报告里显示「待实现」，不会被静默漏掉。

## 依赖与路径

Python 3.9+，需要 `numpy` / `pandas` / `openpyxl` / `scipy` / `h5py` /
`torch`（读 `train_test_split.pth`），以及 `pdftotext`（Poppler，从图件 PDF
的文本层抽取标注做比对）。

路径在 `common/paths.py` 解析。数据目录默认取本仓库的上一级
（`../Data_and_Code_Availability/Raw_Experimental_Data`），论文 tex 目录无法
从仓库位置推断，故给了默认值并支持环境变量覆盖：

```bash
export CH4_TEXDIR=/path/to/OE_Revision_R1_Submission   # 含 OE_submission.tex/.aux 与 Figures/results
export CH4_RAWROOT=/path/to/parent-of-Data_and_Code_Availability
python verify.py
```

核验会读取论文的 `.aux` 取图表编号，故需先编译过一次 tex。
