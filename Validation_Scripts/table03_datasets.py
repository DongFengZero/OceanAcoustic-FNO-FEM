#!/usr/bin/env python3
"""table03_datasets.py — 打印 Table 3（tab:datasets，4.1 节数据集总表）

覆盖 Cases 1-50 全部 22 个配置（R0-R10 / W0-W10）：域尺寸、网格步长、节点数、
是否含障碍物、频率、样本数等。这是结构性表格（配置声明），不是测量值。

取数：复用 T03_datasets.py 的 load_dataset_config()，直接读 COMSOL 网格 .mat
里的 Lx/Ly/节点数——与 verify.py 同一条路径，不另抄一份解析。

    python table03_datasets.py [--tex]
"""
import _tblcommon as K


def main():
    K.head("tab:datasets", "Cases 1-50 · 数据集配置总表（结构性）")
    mod = K.checker_module("T03_datasets")
    K.note(f"Dataset 根目录: {getattr(mod, 'DATASET_DIR', '?')}")
    K.note("取数：T03_datasets.py 的 load_dataset_config()（读 comsol_mesh_*.mat）")

    rows = K.tex_rows_of(0, "tab:datasets")
    if not rows:
        K.note("未能从 tex 抓到表体——检查 CH4_TEXDIR 是否指向已编译的论文目录")
        return

    K.note(f"tex 表体 {len(rows)} 行；下面逐行列出印刷值，并对能定位到 "
           f"Dataset 目录的配置做现场复核")
    w = [5, 8, 8, 8, 8, 10, 9, 10]
    K.row(["No.", "Dataset", "Lx(m)", "Ly(m)", "delta", "N(nodes)",
           "Obstacle", "复核"], w)
    K.rule(w)
    ok = miss = 0
    for r in rows:
        no = r[0].strip()
        did = r[1].strip() if len(r) > 1 else ""
        cfg = None
        try:
            cfg = mod.load_dataset_config(did)
        except Exception:
            cfg = None
        if cfg:
            ok += 1
            mark = "√ 同源"
            cells = [no, did, f"{cfg['lx']:.0f}", f"{cfg['ly']:.0f}",
                     str(cfg.get("delta", "—")), f"{cfg['n']:,}",
                     str(cfg.get("obstacle", "—")), mark]
        else:
            miss += 1
            cells = [no, did] + [c.strip() for c in r[2:7]] + ["印刷值"]
        K.row(cells[:len(w)], w)
    K.rule(w)
    K.note(f"现场复核 {ok} 行；另 {miss} 行仅列印刷值"
           f"（Dataset 目录不在本机时属正常）")
    K.note("完整逐格比对请运行： cd ch4_validation && python verify.py")

    if K.want_tex():
        print("\n  tex 数据行：")
        for r in rows:
            print("   ", " | ".join(r))


if __name__ == "__main__":
    main()
    print()
