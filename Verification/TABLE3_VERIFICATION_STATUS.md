# Table 3 (Dataset Configuration) Verification Report

**Generated**: 2026-07-26
**Table**: Table 3 - Simulation datasets (No. 1-50)

---

## Table 3 Key Configurations (Sample)

| No. | Name | Lx×Ly | Δ | Frequencies | Obstacle (cx,cy,a,b) |
|-----|------|-------|---|-------------|----------------------|
| 1 | R0 | 128×128 | 1.0 | 25-100Hz | None |
| 2 | W0 | 128×128 | 1.0 | 25-100Hz | None |
| 3 | R1 | 128×128 | 1.0 | 25-100Hz | (64, 64, 16, 8) |
| 4 | R2 | 256×128 | 1.0 | 25-100Hz | (192, 32, 32, 8) |
| 5 | R3 | 512×128 | 1.0 | 25-100Hz | (384, 32, 64, 8) |
| 6 | R4 | 128×128 | 1.0 | 100Hz | (64, 64, 16, 8) |
| 7 | R5 | 256×256 | 1.0 | 100Hz | (192, 64, 32, 16) |
| 8 | R6 | 512×512 | 1.0 | 100Hz | (384, 128, 64, 32) |
| 9 | W1 | 128×128 | 1.0 | 25-100Hz | (96, 32, 16, 8) |
| 10 | W2 | 256×128 | 1.0 | 25-100Hz | (192, 32, 32, 8) |
| 11 | W3 | 512×128 | 1.0 | 25-100Hz | (384, 32, 64, 8) |
| 12 | W4 | 128×128 | 1.0 | 100Hz | (96, 32, 16, 8) |
| 13 | W5 | 256×256 | 1.0 | 100Hz | (192, 64, 32, 16) |
| 14 | W6 | 512×512 | 1.0 | 100Hz | (384, 128, 64, 32) |

---

## Verification Items

### 需要核查的项目:

1. **域尺寸**: Lx, Ly应与HDF5文件中的domain参数一致
2. **网格分辨率**: Δ应与mesh spacing一致
3. **频率列表**: Frequencies应与HDF5中的freq_list一致
4. **障碍物参数**: Obstacle (cx,cy,a,b)应与ellipse_params一致
5. **样本数量**: N应与HDF5文件中的样本总数一致
6. **几何类型**: Rect/Wedge应与geometry_type一致

---

## Data File Verification

**数据根目录**: D:\Data\Data_and_Code_Availability\Raw_Experimental_Data

### 样本数据集检查:

- No03_R1: ⚠️ 未找到HDF5文件
- No09_W1: ⚠️ 未找到HDF5文件
- No01_R0: ❌ 路径不存在
---

## 核查方法

### 手动核查步骤:

1. **选择样本数据集** (如No. 3 R1):
   ```bash
   cd D:/Data/Data_and_Code_Availability/Raw_Experimental_Data/4.3_Forward/No03_R1
   ```

2. **检查HDF5文件属性**:
   ```python
   import h5py
   with h5py.File('dataset.h5', 'r') as f:
       print('Frequencies:', f.attrs['freq_list'])
       print('Geometry:', f.attrs['geometry_type'])
       print('Obstacle:', f.attrs.get('ellipse_params', 'None'))
       print('Domain:', f.attrs.get('Lx', 'N/A'), f.attrs.get('Ly', 'N/A'))
   ```

3. **对比Table 3**:
   - Lx×Ly: 论文 vs HDF5
   - Frequencies: 论文 vs HDF5
   - Obstacle: 论文 vs HDF5

---

## 已知问题

### Obstacle列格式

论文Table 3中Obstacle列显示格式如:
- `(64,64,16,8)` - 矩形波导
- `(96,32,16,8)` - 楔形波导

**含义**: `(cx, cy, a, b)`
- `cx`: 椭圆中心x坐标
- `cy`: 椭圆中心y坐标
- `a`: 椭圆长半轴
- `b`: 椭圆短半轴

**需验证**: 这些值是否与HDF5中的`ellipse_params`一致

---

## 状态总结

### ✅ Table 3结构验证

- ✅ 表格包含50个数据集配置
- ✅ 列包括: No, Name, Geometry, Lx, Ly, Δ, Frequencies, N, Obstacle, Platform
- ✅ 分组清晰: Analytical, Forward, Comparison, Ablation, Mesh, Generalization, Runtime

### ⚠️ 需要进一步核查

由于数据文件较大且分散，建议:

1. **抽样验证**: 选择3-5个代表性数据集
   - No. 1-2 (分析验证)
   - No. 3, 9 (前向求解: R1, W1)
   - No. 25, 29 (消融实验)

2. **关键参数验证**:
   - Obstacle参数是否正确
   - 频率列表是否匹配
   - 域尺寸是否一致

3. **交叉验证**:
   - Table 3 ← → HDF5 attributes
   - Table 3 ← → 训练日志
   - Table 3 ← → 结果表格

---

## 建议行动

**优先级**: 中 - 投稿后审稿阶段可能需要

**理由**:
- Table 3是数据集配置的总览表
- 审稿人可能要求核对配置
- 当前验证已覆盖主要训练参数

**建议时间**: 修改稿阶段（如审稿人要求）

---

*报告生成时间: 2026-07-26*
*Table 3核查状态: 结构验证通过，数据核查待执行*