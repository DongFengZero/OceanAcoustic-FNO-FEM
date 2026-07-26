# Chapter 4 - 3 Decimal Places Verification

**Requirement**: All numerical data in tables should have 3 decimal places

---

## Issues Found

- **2 decimal places**: 306 (need to add 0)
- **1 decimal place**: 18 (need to add 00)
- **Integers**: 16 (need to add .000)
- **Total**: 340

---

### 2 Decimal Places (add 0)

- Line 694: `2.94` → `2.940`
- Line 694: `0.41` → `0.410`
- Line 694: `0.99` → `0.990`
- Line 694: `0.13` → `0.130`
- Line 694: `2.92` → `2.920`
- Line 694: `0.73` → `0.730`
- Line 694: `1.51` → `1.510`
- Line 694: `0.77` → `0.770`
- Line 694: `2.09` → `2.090`
- Line 694: `0.51` → `0.510`
- Line 695: `6.12` → `6.120`
- Line 695: `0.36` → `0.360`
- Line 695: `0.46` → `0.460`
- Line 695: `0.15` → `0.150`
- Line 695: `2.77` → `2.770`
- Line 695: `0.59` → `0.590`
- Line 695: `4.18` → `4.180`
- Line 695: `0.96` → `0.960`
- Line 695: `3.38` → `3.380`
- Line 695: `0.51` → `0.510`
- Line 712: `0.15` → `0.150`
- Line 712: `0.13` → `0.130`
- Line 712: `0.34` → `0.340`
- Line 712: `0.43` → `0.430`
- Line 713: `0.11` → `0.110`
- Line 713: `0.07` → `0.070`
- Line 713: `0.45` → `0.450`
- Line 713: `1.23` → `1.230`
- Line 751: `2.48` → `2.480`
- Line 751: `0.70` → `0.700`
- ... and 276 more

---

### 1 Decimal Place (add 00)

- Line 1018: `1563.1` → `1563.100`
- Line 1018: `479.5` → `479.500`
- Line 1018: `424.6` → `424.600`
- Line 1018: `129.6` → `129.600`
- Line 1018: `649.2` → `649.200`
- Line 1037: `685.3` → `685.300`
- Line 1037: `327.9` → `327.900`
- Line 1038: `162.6` → `162.600`
- Line 1157: `56.0` → `56.000`
- Line 1157: `48.9` → `48.900`
- Line 1157: `95.5` → `95.500`
- Line 1157: `50.7` → `50.700`
- Line 1157: `62.8` → `62.800`
- Line 1158: `75.6` → `75.600`
- Line 1158: `35.2` → `35.200`
- Line 1158: `67.0` → `67.000`
- Line 1158: `29.2` → `29.200`
- Line 1158: `51.7` → `51.700`

---

### Integers (add .000)

- Line 1159: `686` → `686.000`
- Line 1159: `206` → `206.000`
- Line 1159: `214` → `214.000`
- Line 1159: `149` → `149.000`
- Line 1159: `314` → `314.000`
- Line 1160: `828` → `828.000`
- Line 1160: `179` → `179.000`
- Line 1160: `173` → `173.000`
- Line 1160: `122` → `122.000`
- Line 1160: `325` → `325.000`
- Line 1228: `128` → `128.000`
- Line 1229: `256` → `256.000`
- Line 1230: `512` → `512.000`
- Line 1232: `128` → `128.000`
- Line 1233: `256` → `256.000`
- Line 1234: `512` → `512.000`

---

## Auto-Fix Script

Use the following Python script to automatically fix all issues:

```python
import re

with open('OE_submission.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 2 decimal places by adding 0
content = re.sub(r'\b2\.94\b', '2.940', content)
content = re.sub(r'\b0\.41\b', '0.410', content)
content = re.sub(r'\b0\.99\b', '0.990', content)
content = re.sub(r'\b0\.13\b', '0.130', content)
content = re.sub(r'\b2\.92\b', '2.920', content)
# ... (continue for all)

with open('OE_submission.tex', 'w', encoding='utf-8') as f:
    f.write(content)
```
