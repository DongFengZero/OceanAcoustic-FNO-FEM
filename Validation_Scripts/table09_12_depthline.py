#!/usr/bin/env python3
"""table09_12_depthline.py — 打印 Table 9-12（深度线 TL-MAE）

  Table 8   tab:dl-cmp  Cases 15-19 (R1 矩形) | 20-24 (W1 楔形)，五方法
  Table 9   tab:dl-abl  Cases 25-28 (R1 矩形) | 29-32 (W1 楔形)，四消融组

R1 把矩形/楔形并进**同一张 tabular**：左列组矩形、右列组楔形，故整表一次就能
取全。SPEC 里同一 label 出现两次是因为左右两半的取数分组不同，tex 行只打印一次。

这四张表**不在 xlsx 里**：数值由成图脚本 advantage_depth_line.py 从 ep200 的
npz 现场提取，所以 caption 标 last epoch。本脚本复用 common/depthline.py 的
recompute()，与 verify.py 走同一条重算路径（不复制算法），得到的是全精度值，
论文印刷 3 位小数。

    python table09_12_depthline.py [--tex]
"""
import _tblcommon as K

# label → (标题, 组名, 行定义[(No., 印刷名, 脚本内标签)])
SPEC = [
    ("tab:dl-cmp", "Cases 15-19 · R1 矩形深度线，五方法（左列组）",
     "comparison_R1_model_advantage",
     [(15, "Proposed", "Proposed (Ours)"), (16, "DeepONet", "DeepONet"),
      (17, "FNO", "FNO"), (18, "KNO", "KNO"), (19, "CNO", "CNO")]),
    ("tab:dl-cmp", "Cases 20-24 · W1 楔形深度线，五方法（右列组）",
     "comparison_W1_model_advantage",
     [(20, "Proposed", "Proposed (Ours)"), (21, "DeepONet", "DeepONet"),
      (22, "FNO", "FNO"), (23, "KNO", "KNO"), (24, "CNO", "CNO")]),
    ("tab:dl-abl", "Cases 25-28 · R1 矩形深度线，四消融组（左列组）",
     "ablation_R1_module_advantage",
     [(25, "Full model", "Full (Ours)"),
      (26, "w/o physics prior", "w/o prior"),
      (27, "w/o graph correction", "w/o graph"),
      (28, "w/o prior supervision", "w/o prior-sup.")]),
    ("tab:dl-abl", "Cases 29-32 · W1 楔形深度线，四消融组（右列组）",
     "ablation_W1_module_advantage",
     [(29, "Full model", "Full (Ours)"),
      (30, "w/o physics prior", "w/o prior"),
      (31, "w/o graph correction", "w/o graph"),
      (32, "w/o prior supervision", "w/o prior-sup.")]),
]


def one(label, title, group, rows, tex=True):
    from common import depthline as DL
    K.head(label, title)
    K.note(f"成图脚本: {getattr(DL.script(), '__file__', '?')}   组: {group}")
    K.note("取数：common/depthline.py 的 recompute()（与 verify.py 同源，全精度）")
    try:
        rec = DL.recompute(group)
    except Exception as e:
        K.note(f"重算失败：{e}")
        return
    K.note(f"公共深度线 y = {rec['y_line']:.1f} m（行号 {rec['row']}，"
           f"force_y={rec.get('force_y')}）")
    meths = rec["methods"]          # 行序
    er = rec["er"]                  # {freq: [各方法值]}
    w = [24] + [11] * 4
    K.row(["No.  Method"] + [f"{f}Hz" for f in K.FREQS], w)
    K.rule(w)
    for no, shown, tag in rows:
        i = meths.index(tag) if tag in meths else None
        vals = ["—" if i is None else f"{er[f][i]:.3f}" for f in K.FREQS]
        K.row([f"{no}  {shown}"] + vals, w)
    K.rule(w)
    K.row(["  表头源坐标 Src(x,y)"] +
          [f"({rec['src'][f][0]:.1f},{rec['src'][f][1]:.1f})"
           for f in K.FREQS], w)
    K.note("TL-MAE 单位 dB；论文印刷 3 位小数，最优值加粗（此处不加粗）")
    if K.want_tex() and tex:
        print("\n  tex 数据行（左列组矩形 | 右列组楔形，同表）：")
        for r in K.tex_rows(label):
            print("   ", " | ".join(r))


if __name__ == "__main__":
    seen = set()
    for label, title, group, rows in SPEC:
        one(label, title, group, rows, tex=label not in seen)
        seen.add(label)
    print()
