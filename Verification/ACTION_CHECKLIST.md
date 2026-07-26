# 🚨 立即行动清单 - 论文修正

**优先级**: 🔴 **紧急** - 投稿前必须修正  
**发现时间**: 2026-07-26

---

## ❌ 发现的问题

**FNO宽度参数不一致**:
- 论文声称: **W = 32**
- 实际训练: **W = 48** (训练日志已确认)
- 差异: **+50%** 模型容量

---

## ✅ 需要修改的位置

### **1. 主要修改**

**文件**: `OE_submission.tex`  
**位置**: Section 4.1, Line 582

**原文**:
```latex
The FNO prior uses G=64, W=32, L=4 Fourier layers, and
```

**改为**:
```latex
The FNO prior uses G=64, W=48, L=4 Fourier layers, and
```

### **2. 全文搜索检查**

在论文中搜索以下关键词，确保没有其他地方错误引用：
- [ ] "W=32"
- [ ] "width 32"
- [ ] "32-dimensional"
- [ ] "hidden dimension 32"

### **3. 相关章节检查**

- [ ] Section 3.1 (FNO Physics-Prior) - 检查是否提到宽度
- [ ] Section 4.1 (Experimental Setup) - **主要修改位置** ✓
- [ ] Supplementary Material - 检查参数表

---

## 📊 已验证的正确参数

以下参数已确认一致，**无需修改**:

| 参数 | 值 | 状态 |
|------|-----|------|
| G (grid size) | 64 | ✓ |
| L (Fourier layers) | 4 | ✓ |
| m1, m2 (modes) | 16 | ✓ |
| λ_m | 100 | ✓ |
| λ_p | 1.0 | ✓ |
| lr | 0.001 | ✓ |
| batch_size | 1 | ✓ |
| epochs | 200 | ✓ |
| γ | 0.995 | ✓ |

---

## 📝 建议的修改流程

1. **立即修改** (5分钟):
   - 打开 `OE_submission.tex`
   - 找到 Line 582
   - 将 `W=32` 改为 `W=48`

2. **全文检查** (10分钟):
   - Ctrl+F 搜索 "32"
   - 检查所有相关上下文

3. **重新编译** (2分钟):
   ```bash
   pdflatex OE_submission.tex
   ```

4. **验证修改** (3分钟):
   - 确认PDF中显示 `W=48`
   - 检查表格、图片说明是否受影响

---

## 🔍 验证证据

### **代码证据**:
```python
# trainer.py Line 3535
parser.add_argument('--hidden_channels', type=int, default=48)

# models.py Line 641
width=max(16, self.interm_channels)  # = max(16, 48) = 48
```

### **训练日志证据**:
```
文件: No03_R1/training_run/logs/full_run_20260710_221657.log
内容: hidden_channels = 48
```

---

## ⚠️ 不修改的后果

如果不修改论文:
1. **可重现性受损**: 读者按W=32训练会得到更差结果
2. **审稿人质疑**: 如果审稿人检查代码会发现不一致
3. **科学诚信**: 参数描述与实际实验不符

---

## ✅ 修改后的好处

1. **准确性**: 参数描述与实际训练一致
2. **可重现**: 读者能复现论文结果
3. **透明度**: 诚实报告实际使用的参数

---

## 📋 检查清单

在投稿前确认:
- [ ] Line 582 已修改: W=32 → W=48
- [ ] 全文搜索"32"，确认无其他错误引用
- [ ] PDF重新编译成功
- [ ] 参数表（如有）已更新
- [ ] Supplementary material已更新
- [ ] 所有作者已知晓此修改

---

**预计修改时间**: 20分钟  
**风险评估**: 低 - 仅修改一个数值  
**影响范围**: Section 4.1 一处

---

*清单生成时间: 2026-07-26*  
*建议立即执行*
