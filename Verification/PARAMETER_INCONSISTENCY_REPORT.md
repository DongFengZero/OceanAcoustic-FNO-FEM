# ⚠️ 代码-论文参数不一致报告

**Generated**: 2026-07-26  
**严重程度**: 高

---

## 🔴 **发现的不一致**

### **FNO宽度参数 (W)**

| 来源 | 声明值 | 实际值 | 状态 |
|------|--------|--------|------|
| **论文** (Section 4.1, Line 582) | W = 32 | - | 📄 |
| **代码** (models.py Line 641) | - | `max(16, interm_channels)` | 💻 |
| **代码** (trainer.py Line 3535) | - | `hidden_channels=48` (默认) | 💻 |
| **实际运行值** | - | **W = 48** | ⚠️ |

**不一致**: 论文声称W=32，但代码默认使用W=48

---

## 📍 **代码追踪**

### **Step 1: 命令行参数定义**
**文件**: `ocean_trainer_forward_b.py`  
**Line 3535-3536**:
```python
parser.add_argument('--hidden_channels', type=int, default=48,
                    help='隐藏层通道数')
```

### **Step 2: 传递给模型**
**Line 3429**:
```python
model = GNNModel_Forward(
    ...
    interm_channels=args.hidden_channels,  # = 48
    ...
)
```

### **Step 3: 模型初始化**
**文件**: `deq_modules/models.py`  
**Line 935**:
```python
def __init__(self, ..., interm_channels=32, ...):  # 默认32，但被覆盖
    ...
    self.interm_channels = interm_channels  # = 48
```

### **Step 4: FNO Prior初始化**
**Line 639-641**:
```python
self.fno_corr = _FNOScatterField(
    node_xy=self.p[:self.N, :2], freq_list=self.freq_list,
    grid=64, width=max(16, self.interm_channels), modes=16)
    #                  ^^^^^^^^^^^^^^^^^^^^^^^^^
    #                  = max(16, 48) = 48
```

### **Step 5: FNO类定义**
**Line 103**:
```python
def __init__(self, ..., width: int = 32, ...):
    ...
    self.width = int(width)  # 实际接收到 48
```

---

## 🔍 **验证方法**

### **检查实际运行的参数**:

```bash
# 1. 查看训练日志中的参数
grep "hidden_channels" training_log.txt

# 2. 运行时打印
python ocean_trainer_forward_b.py ... --hidden_channels 32  # 强制使用32
```

### **检查模型权重**:

```python
import torch
checkpoint = torch.load('model.pth')
fno_lift_weight = checkpoint['model']['implicit_layer.fno_corr.lift.weight']
print(f"FNO width = {fno_lift_weight.shape[0]}")  # 应该是48，不是32
```

---

## 📊 **影响分析**

### **1. 模型容量差异**

| 参数 | W=32 | W=48 | 差异 |
|------|------|------|------|
| FNO参数量 | ~32K | ~72K | +125% |
| 计算量 | 基准 | ~2.25×基准 | +125% |

### **2. 对实验结果的影响**

- ⚠️ **论文报告的精度**可能基于W=48的模型
- ⚠️ **消融实验中"Full model"**可能使用W=48
- ⚠️ **与基线对比**可能不公平（如果基线使用W=32）

### **3. 可重现性问题**

读者按照论文W=32训练：
- 可能获得**更低的精度**
- 模型参数量减少**44%**
- 训练速度可能更快，但效果更差

---

## ✅ **验证其他相关参数**

| 参数 | 论文 | 代码 (trainer.py) | 代码 (models.py) | 实际值 | 状态 |
|------|------|-------------------|------------------|--------|------|
| G (grid) | 64 | - | Line 641: `grid=64` | 64 | ✅ 一致 |
| L (layers) | 4 | - | Line 104: `n_layers=4` | 4 | ✅ 一致 |
| modes | 16 | - | Line 641: `modes=16` | 16 | ✅ 一致 |
| **W (width)** | **32** | **Line 3535: 48** | **Line 641: max(16,48)** | **48** | ❌ **不一致** |

---

## 🎯 **建议修正方案**

### **Option 1: 修改论文** (推荐)

**修改位置**: Section 4.1, Line 582

**原文**:
> The FNO prior uses G=64, **W=32**, L=4 Fourier layers, and...

**改为**:
> The FNO prior uses G=64, **W=48**, L=4 Fourier layers, and...

**理由**: 
- 代码中多处使用48
- 已有的实验结果基于W=48
- 修改论文比重新训练更快

### **Option 2: 修改代码**

**修改位置**: `ocean_trainer_forward_b.py` Line 3535

**原代码**:
```python
parser.add_argument('--hidden_channels', type=int, default=48, ...)
```

**改为**:
```python
parser.add_argument('--hidden_channels', type=int, default=32, ...)
```

**理由**: 
- 符合论文描述
- 需要重新训练所有模型
- 精度可能下降

### **Option 3: 明确说明** (补充方案)

在论文中添加脚注或说明：
> Note: The hidden dimension of the graph correction module is set to 48, which also determines the FNO prior width through width=max(16, hidden_channels).

---

## 📝 **待确认问题**

1. [ ] **实验结果是基于W=32还是W=48?**
   - 检查训练日志
   - 检查保存的模型权重形状

2. [ ] **消融实验中各变体的W值是否一致?**
   - "w/o prior"使用的W值
   - "w/o graph"使用的W值

3. [ ] **基线模型的W值**
   - FNO基线: Line 3446硬编码`width=32` ✓
   - DeepONet基线: `hidden=128` ✓
   - KNO/CNO基线: 需检查

---

## 🔬 **建议验证步骤**

1. **立即检查**: 查看已保存模型的权重形状
   ```python
   ckpt = torch.load('Case03_R1_ep200.pth')
   lift_w = ckpt['model']['implicit_layer.fno_corr.lift.weight']
   print(f"实际FNO width = {lift_w.shape[0]}")
   ```

2. **对比训练**: 用W=32重新训练Case 3，对比精度差异

3. **更新论文**: 根据验证结果修正论文参数描述

---

## 总结

**状态**: ⚠️ **严重不一致 - 需要立即修正**

**影响**: 
- 模型容量差异 +125%
- 可重现性受影响
- 读者无法复现论文结果

**推荐操作**: 
1. 验证实际运行的模型使用W=48
2. 修改论文Section 4.1: W=32 → W=48
3. 检查其他可能的参数不一致

---

*报告生成时间: 2026-07-26*  
*优先级: 高 - 需要在论文投稿前修正*
