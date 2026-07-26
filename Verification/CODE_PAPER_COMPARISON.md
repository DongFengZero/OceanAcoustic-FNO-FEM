# Code-Paper Parameter Verification Report

**Generated**: 2026-07-26

This report compares all parameters described in the paper with actual code implementation.

---

## Parameter Comparison

| Parameter | Paper | Code | Match | Location |
|-----------|-------|------|-------|----------|
| **G** | 64 | 64 | ✓ | `deq_modules/models.py Line 103` |
| **W** | 32 | 32 | ✓ | `deq_modules/models.py Line 103` |
| **L** | 4 | 4 | ✓ | `deq_modules/models.py Line 104` |
| **m1** | 16 | 16 | ✓ | `deq_modules/models.py Line 103` |
| **m2** | 16 | 16 | ✓ | `deq_modules/models.py Line 103` |
| **lambda_m** | 100 | 100 | ✓ | `ocean_trainer_forward_b.py Line 3543 (--loss_w_rel_mse)` |
| **lambda_p** | 1.0 | 1.0 | ✓ | `ocean_trainer_forward_b.py Line 3557 (--loss_w_prior)` |
| **lr** | 0.001 | 0.001 | ✓ | `ocean_trainer_forward_b.py Line 1088 (AdamW optimizer)` |
| **batch_size** | 1 | 1 | ✓ | `ocean_trainer_forward_b.py Line 3516 (--batch_size)` |
| **epochs** | 200 | 200 | ✓ | `ocean_trainer_forward_b.py Line 3514 (--epochs)` |
| **gamma** | 0.995 | 0.995 | ✓ | `ocean_trainer_forward_b.py Line 1096 (ExponentialLR)` |

**Summary**: 11/11 parameters verified

---

## Code Implementation Details

### FNO Architecture (_FNOScatterField)
**File**: `Experiment_Code/Main_Code/deq_modules/models.py`

```python
class _FNOScatterField(nn.Module):
    def __init__(self, node_xy: torch.Tensor, freq_list,
                 grid: int = 64,      # G in paper
                 width: int = 32,     # W in paper
                 modes: int = 16,     # m1=m2 in paper
                 n_layers: int = 4,   # L in paper
                 k_nn: int = 8):
        ...
        self.lift = nn.Linear(5, self.width)  # 5-channel input
        self.specs = nn.ModuleList([
            _SpectralConv2d(self.width, self.width, modes, modes)
            for _ in range(max(1, n_layers))])  # L layers
        self.proj1 = nn.Linear(self.width, 128)
        self.proj2 = nn.Linear(128, 2)  # Output: [real, imag]
```

### Training Configuration
**File**: `Experiment_Code/Main_Code/ocean_trainer_forward_b.py`

```python
# Optimizer (Line 1088)
self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3)

# Command-line arguments (Lines 3514-3557)
parser.add_argument('--epochs', type=int, default=200)
parser.add_argument('--batch_size', type=int, default=1)
parser.add_argument('--loss_w_rel_mse', type=float, default=1.0e2)  # lambda_m
parser.add_argument('--loss_w_prior', type=float, default=1.0)      # lambda_p
```

### Input Construction
**Code confirms 5-channel input** (Line 95-96):
```python
# forward_source input channels (grid x grid):
# [源高斯图, 源高斯图, x, y, freq]
```

**Matches paper Equation 3**:
```
inp(x,y) = [g(x,y), g(x,y), x̂, ŷ, f/f_max]
```

---

## Issues Found

✓ **No issues found** - All parameters match!

---

## Recommendations

### Verified Items:

✓ FNO grid size G=64
✓ FNO width W=32
✓ Fourier layers L=4
✓ Mode truncation m1=m2=16
✓ Loss weights λ_m=100, λ_p=1.0
✓ Learning rate 0.001
✓ Batch size 1
✓ Training epochs 200
✓ Input: 5-channel format
✓ Output: Realified [real, imag]

---

## Summary

**Parameters checked**: 11
**Verified matches**: 11
**Issues**: 0

**Status**: ✓ **PASS** - All parameters verified

---

*Report generated: 2026-07-26*
*Code verification version: 1.0*