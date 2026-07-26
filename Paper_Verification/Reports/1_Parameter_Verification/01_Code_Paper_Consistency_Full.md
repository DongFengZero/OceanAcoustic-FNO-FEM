# Code-Paper Consistency

**Generated**: 2026-07-26 21:01:58

**Description**: Verify all parameters match between code and paper

---

## Output

```
======================================================================
CODE-PAPER CONSISTENCY CHECK
======================================================================
Parameters extracted from paper: 10

Paper parameters:
  G: 64
  L: 4
  m1: 16
  m2: 16
  lambda_m: 100
  lambda_p: 1.0
  lr: 0.001
  batch_size: 1
  epochs: 200
  gamma: 0.995

Training scripts found: 3
Scripts to check:
  - Experiment_Code\Main_Code\ocean_trainer_forward_b.py
  - run_all_verifications.py
  - Verification\run_all.py

Report written to: CODE_PAPER_CONSISTENCY_CHECK.md

[NEXT] Manual code review required to verify parameters
======================================================================

```


**Exit Code**: 0
