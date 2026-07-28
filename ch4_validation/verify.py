#!/usr/bin/env python3
"""
verify.py — 第 4 章全部表格与图件的核验主程序
==============================================

用法
    python verify.py                 # 全跑，生成 REPORT.md
    python verify.py T04 T06         # 只跑指定对象（前缀匹配 slug 或 label）
    python verify.py --kind table    # 只跑表 / figure
    python verify.py --sec 4.3       # 只跑某节
    python verify.py --list          # 列出全部对象与其核验脚本，不执行
    python verify.py --quiet         # 只打印汇总行

退出码
    0  全部已实现对象通过
    1  有对象失败
    2  用法错误

覆盖率以 common/registry.py 的 40 条记录（19 表 + 21 图）为分母。
一个脚本可覆盖多个对象（例如 FIG05_07_res_fields.py 同时核 Fig 5/6/7），
映射见 SCRIPT_MAP；注册但无脚本的对象会显示「待实现」，不会被静默漏掉。
"""
import argparse
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:                      # Windows 控制台默认 GBK，会吃掉报告里的中文
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

from common import registry                                     # noqa: E402

PKG = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.join(PKG, "reports")

# ── 对象 → 核验脚本 ────────────────────────────────────────────────
# 表侧一对一；图侧多为合并式（同一版式的几张图共用一份链路）。
SCRIPT_MAP = {
    # 表：scripts/<slug>.py
    **{r["slug"]: ("scripts", r["slug"]) for r in registry.ALL
       if r["kind"] == "table"},
    # 图：scripts_figures/<脚本名>.py
    "F03_ideal_rect":     ("scripts_figures", "FIG03_ideal_rect"),
    "F04_ideal_wedge":    ("scripts_figures", "FIG04_ideal_wedge"),
    "F05_res_128":        ("scripts_figures", "FIG05_07_res_fields"),
    "F06_res_256":        ("scripts_figures", "FIG05_07_res_fields"),
    "F07_res_512":        ("scripts_figures", "FIG05_07_res_fields"),
    "F08_res_rect_100":   ("scripts_figures", "FIG08_09_res_100"),
    "F09_res_wedge_100":  ("scripts_figures", "FIG08_09_res_100"),
    "F10_dl_cmp_rect":    ("scripts_figures", "FIG10_11_dl_cmp"),
    "F11_dl_cmp_wedge":   ("scripts_figures", "FIG10_11_dl_cmp"),
    "F12_dl_abl_rect":    ("scripts_figures", "FIG12_13_dl_abl"),
    "F13_dl_abl_wedge":   ("scripts_figures", "FIG12_13_dl_abl"),
    "F14_perf_rect":      ("scripts_figures", "FIG14_15_perf_grid"),
    "F15_perf_wedge":     ("scripts_figures", "FIG14_15_perf_grid"),
    "F16_abl_rect":       ("scripts_figures", "FIG16_17_abl_grid"),
    "F17_abl_wedge":      ("scripts_figures", "FIG16_17_abl_grid"),
    "F18_mesh_rect":      ("scripts_figures", "FIG18_19_mesh"),
    "F19_mesh_wedge":     ("scripts_figures", "FIG18_19_mesh"),
    "F20_gen_split":      ("scripts_figures", "FIG20_gen_split"),
    "F21_gen_grid":       ("scripts_figures", "FIG21_22_gen_extrap"),
    "F22_gen_grid_wedge": ("scripts_figures", "FIG21_22_gen_extrap"),
    "F23_perf":           ("scripts_figures", "FIG23_perf"),
}

# ── 跨对象核验（不属于单个表/图，单独计入） ────────────────────────
CROSS_CHECKS = [
    ("T13_16_layout", "scripts", "T13_16_layout",
     "Tables 13-16 等宽版式一致性"),
    ("TABALL_refs", "scripts", "TABALL_refs",
     "全章表格引用完整性（无孤表/无悬空/独立正文引用）"),
    ("FIGALL_refs", "scripts_figures", "FIGALL_refs",
     "全章图件引用完整性（无孤图/无悬空/独立正文引用）"),
]


def script_path(entry):
    """(子目录, 脚本名) -> 绝对路径；不存在返回 None。"""
    if entry is None:
        return None
    sub, name = entry
    p = os.path.join(PKG, sub, f"{name}.py")
    return p if os.path.exists(p) else None


def parse_report(name):
    """从报告首部取回结论与计数，不在此重复判定逻辑。"""
    p = os.path.join(REPORTS, f"{name}.md")
    if not os.path.exists(p):
        return None
    head = open(p, encoding="utf-8").read(1200)
    m = re.search(r"\*\*(PASS|FAIL)\*\*\s*—\s*(\d+)\s*通过\s*/\s*(\d+)\s*失败"
                  r"\s*/\s*(\d+)\s*警告(?:\s*/\s*(\d+)\s*豁免)?", head)
    if not m:
        return None
    return dict(verdict=m.group(1), n_pass=int(m.group(2)),
                n_fail=int(m.group(3)), n_warn=int(m.group(4)),
                n_exempt=int(m.group(5) or 0),
                report=os.path.relpath(p, PKG).replace("\\", "/"))


def run_script(path):
    """执行一个核验脚本，返回 (returncode, 耗时秒)。"""
    t0 = time.time()
    r = subprocess.run([sys.executable, path], cwd=PKG,
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, time.time() - t0, (r.stdout or "") + (r.stderr or "")


def write_report(objs, missing, results, tot, bad):
    """生成 REPORT.md：结论 + 覆盖矩阵 + 分节明细 + 已知缺口。"""
    L = []
    ok = not bad
    L.append("# 第 4 章表格与图件核验主报告")
    L.append("")
    L.append(f"- 结论：**{'PASS' if ok else 'FAIL'}** — "
             f"{tot['n_pass']} 项通过 / {tot['n_fail']} 项失败"
             + (f" / {tot['n_exempt']} 项豁免" if tot["n_exempt"] else ""))
    L.append(f"- 覆盖：{sum(len(v['owners']) for v in results.values())}"
             f"/{len(objs)} 个对象"
             + (f"，{len(missing)} 个待实现" if missing else "（全覆盖）"))
    L.append(f"- 核验脚本：{len(results)} 个"
             + (f"，失败 {len(bad)} 个" if bad else "，全部通过"))
    L.append(f"- 生成：{time.strftime('%Y-%m-%d %H:%M:%S')}")
    L.append(f"- 复现：`python verify.py`")
    L.append("")
    L.append("每个对象的逐项明细在 `reports/<脚本名>.md`，本报告只汇总。")
    L.append("")
    L.append("## 核验做了什么")
    L.append("")
    L.extend([
        "表格与图件的印刷值，一律回到原始数据现场重算后比对，不信任任何",
        "中间产物。链路分三层：",
        "",
        "1. **源可追溯** — 每个数值都能指到 `Raw_Experimental_Data` 下的",
        "   xlsx / 训练日志 / npz；成图脚本的两份副本须 md5 相同，否则图",
        "   与核验可能分属两份数据。",
        "2. **双渠道交叉** — 同一量在 xlsx 与训练日志里各取一次，先证两个",
        "   渠道自身一致，再与印刷值比对。单渠道对得上不足以排除系统性错误。",
        "3. **口径防漂移** — 插值网格数、插值方法、频率列表、坐标位数这些",
        "   口径参数，从成图脚本源码里现场读出来断言，而非在核验脚本里写",
        "   死。绘图脚本改了口径而图未重绘，这一层会立刻失败。",
        "",
        "判定不设数值容差：源值按印刷位数四舍五入后须逐字符相等。容差会",
        "同时掩盖真实偏差和补 0 伪造。",
    ])
    L.append("")
    L.append("### 四类容易漏掉的检查")
    L.append("")
    L.extend([
        "以下四项都不会引起编译错误，靠肉眼校对也很难发现，故各自做成独立断言：",
        "",
        "**① 正文引用的数值** — 正文里复述的每个数字，既要与表格印刷值逐字符",
        "相同，也要由源数据独立支持。只查前者会漏掉「正文与表格一起错」的情形，",
        "所以两侧都查。",
        "",
        "**② 派生数值的口径** — 正文里的倍数、差值、加速比，一律按**表格印刷值**",
        "复算，读者拿表上三位小数就能验证。全精度口径有时会差 0.001（例如",
        "`5.007779 − 3.174378 = 1.833` 而印刷值口径得 `1.834`），报告里两个口径",
        "都写出来并说明取哪个，不做静默取舍。",
        "",
        "**③ best epoch 与 last epoch** — 精度表取 best epoch，场图与深度线图取",
        "ep200(last)，二者**本是不同轮次**（Case 14 的 best=129 与 last=200 差 71",
        "轮）。所以判据是双侧的：caption 含 `last` **且** 不含 `best`，并把各 case",
        "的 best 与 200 的差异列进报告。只查「含 last」的话，把 caption 改成",
        "`best` 也照样通过。深度线族的表与图同取 last，判据相应改为「两侧声明",
        "必须一致」，不能照搬场图族的「必然不同」。",
        "",
        "**④ 引用完整性** — 本章有四种引用形式：散文单点、散文区间",
        "（`Figs.~\\ref{A}--\\ref{B}`，中间各图自身 `\\ref` 计数为 0）、散文并列、",
        "表格 Fig. 列（`\\ref{fig}\\subref{sub}`）。只按单点统计会把区间内部的图",
        "误判为漏引。跨对象核验用两级判据：宽判「是否被引」，严判「figure/table",
        "环境**之外**是否有独立 `\\ref`」——后者堵死靠区间或 caption 兜底的路径。",
    ])
    L.append("")

    # ── 覆盖矩阵 ──────────────────────────────────────────────────
    L.append("## 覆盖矩阵")
    L.append("")
    L.append("| 对象 | 编号 | 类型 | 节 | 核验项 | 结论 | 明细 |")
    L.append("|---|---|---|---|---|---|---|")
    owner_of = {}
    for name, v in results.items():
        for r in v["owners"]:
            owner_of[r["slug"]] = (name, v)
    for r in objs:
        hit = owner_of.get(r["slug"])
        if hit is None:
            L.append(f"| `{r['slug']}` | {r['label']} | {r['kind']} | "
                     f"{r['sec']} | — | 待实现 | — |")
            continue
        name, v = hit
        rep = v["rep"]
        if rep is None:
            L.append(f"| `{r['slug']}` | {r['label']} | {r['kind']} | "
                     f"{r['sec']} | — | **ERR** | `{name}` |")
        else:
            n = rep["n_pass"] + rep["n_fail"] + rep["n_warn"] + rep["n_exempt"]
            L.append(f"| `{r['slug']}` | {r['label']} | {r['kind']} | "
                     f"{r['sec']} | {n} | {rep['verdict']} | "
                     f"[{name}]({rep['report']}) |")
    L.append("")

    # ── 跨对象核验 ────────────────────────────────────────────────
    cross = [(n, s, f, d) for n, s, f, d in CROSS_CHECKS if n in results]
    if cross:
        L.append("## 跨对象核验")
        L.append("")
        L.append("这些检查不属于任何单个表或图，只能在全局做。")
        L.append("")
        L.append("| 检查 | 核验项 | 结论 | 明细 |")
        L.append("|---|---|---|---|")
        for name, _sub, _fn, desc in cross:
            rep = results[name]["rep"]
            if rep is None:
                L.append(f"| {desc} | — | **ERR** | `{name}` |")
            else:
                n = (rep["n_pass"] + rep["n_fail"]
                     + rep["n_warn"] + rep["n_exempt"])
                L.append(f"| {desc} | {n} | {rep['verdict']} | "
                         f"[{name}]({rep['report']}) |")
        L.append("")

    # ── 已知缺口 ──────────────────────────────────────────────────
    L.append("## 已知缺口")
    L.append("")
    L.extend([
        "如实记录三处，避免读者以为核验是全覆盖的：",
        "",
        "1. **Fig 23 无成图脚本可比对。** 仓库内没有生成 `perf_merged.pdf` 的",
        "   脚本（`build_perf.py` 只产 xlsx 不画图），故这张图无法做「脚本产物",
        "   vs 论文图件 md5 同源」的比对。改以「图上标注 vs 表值」逐点核验替代，",
        "   强度略低。其余 20 张图都有 md5 同源或数值复现两道锁。",
        "",
        "2. **场图的样本选择是索引顺序，非代表性抽样。** 场图族用 `pick_rows`",
        "   取每频率前 2 个样本，caption 称 \"two representative held-out",
        "   samples\"。这 8 个样本给的是个案观感，不是全测试集的代表值——",
        "   Fig 16/17 的中段名次与 Tables 15/16 不同就源于此（已在 caption 中",
        "   加了说明）。深度线族用 `pick_sample` 取 MAE 最优样本，口径不同。",
        "",
        "3. **图上误差与表格 TL 不可互相反算。** 图上 `Avg` 是单样本场误差均值，",
        "   表里的 TL 是全测试集平均，样本集不同。故只核排序或端点是否同向，",
        "   不核数值相等。五方法组两侧完整排序一致；四变体组仅端点一致，中段",
        "   名次因聚合口径而互换，属正常。",
    ])
    L.append("")
    L.append("## 目录结构")
    L.append("")
    L.append("```")
    L.extend([
        "ch4_validation/",
        "├── verify.py              主程序：跑全部核验并生成本报告",
        "├── REPORT.md              本报告（自动生成）",
        "├── common/                共用层",
        "│   ├── paths.py           数据与 tex 路径解析",
        "│   ├── registry.py        40 个对象的注册表（19 表 + 21 图）",
        "│   ├── metrics.py         xlsx / 训练日志取数与舍入比对",
        "│   ├── depthline.py       深度线组重算（复用成图脚本自身函数）",
        "│   ├── texparse.py        tex/aux 解析：表体、caption、label、引用",
        "│   └── report.py          Checker：断言累积与 Markdown 渲染",
        "├── scripts/               表格核验，一表一脚本",
        "├── scripts_figures/       图件核验，同版式的图合并为一份",
        "└── reports/               各对象的逐项明细（自动生成）",
    ])
    L.append("```")
    L.append("")
    if bad:
        L.append("## 失败项")
        L.append("")
        for name in sorted(bad):
            v = results[name]
            rep = v["rep"]
            if rep is None:
                L.append(f"- `{name}`：脚本退出码 {v['rc']}，未产出可解析报告")
                tail = (v["out"] or "").strip().splitlines()
                if tail:
                    L.append(f"  - `{tail[-1][:200]}`")
            else:
                L.append(f"- `{name}`：{rep['n_fail']} 项失败 → "
                         f"[{rep['report']}]({rep['report']})")
        L.append("")
    open(os.path.join(PKG, "REPORT.md"), "w", encoding="utf-8",
         newline="\n").write("\n".join(L) + "\n")


def select(args):
    """按命令行条件挑出要核的 registry 对象。"""
    objs = list(registry.ALL)
    if args.kind:
        objs = [r for r in objs if r["kind"] == args.kind]
    if args.sec:
        objs = [r for r in objs if r["sec"] == args.sec]
    if args.only:
        keys = [k.lower() for k in args.only]
        objs = [r for r in objs
                if any(k in r["slug"].lower() or k in r["label"].lower()
                       for k in keys)]
    return objs


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("only", nargs="*", help="只跑匹配的对象（slug 或 label 子串）")
    ap.add_argument("--kind", choices=["table", "figure"])
    ap.add_argument("--sec")
    ap.add_argument("--list", action="store_true", help="列出对象与脚本，不执行")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-cross", action="store_true", help="跳过跨对象核验")
    ap.add_argument("--no-report", action="store_true", help="不写 REPORT.md")
    args = ap.parse_args()

    objs = select(args)
    if not objs:
        print("没有匹配的对象", file=sys.stderr)
        return 2

    if args.list:
        print(f"{'对象':22s} {'编号':6s} {'类型':7s} {'节':5s} 核验脚本")
        for r in objs:
            p = script_path(SCRIPT_MAP.get(r["slug"]))
            rel = os.path.relpath(p, PKG).replace("\\", "/") if p else "（待实现）"
            print(f"{r['slug']:22s} {r['label']:6s} {r['kind']:7s} "
                  f"{r['sec']:5s} {rel}")
        return 0
    # 合并式脚本只跑一次：先按脚本去重，再把结果分发回各对象
    todo, missing = {}, []
    for r in objs:
        p = script_path(SCRIPT_MAP.get(r["slug"]))
        if p is None:
            missing.append(r)
        else:
            todo.setdefault(p, []).append(r)

    if not args.no_cross and not args.only and not args.kind and not args.sec:
        for name, sub, fn, _desc in CROSS_CHECKS:
            p = script_path((sub, fn))
            if p:
                todo.setdefault(p, [])

    results, t_all = {}, time.time()
    for i, (p, owners) in enumerate(sorted(todo.items()), 1):
        name = os.path.splitext(os.path.basename(p))[0]
        rc, dt, out = run_script(p)
        rep = parse_report(name)
        results[name] = dict(rc=rc, dt=dt, rep=rep, owners=owners, out=out)
        if not args.quiet:
            if rep:
                tail = f" / {rep['n_exempt']} 豁免" if rep["n_exempt"] else ""
                print(f"[{rep['verdict']}] {name}: {rep['n_pass']} 通过 / "
                      f"{rep['n_fail']} 失败 / {rep['n_warn']} 警告{tail}"
                      f"  ({dt:.1f}s)")
            else:
                print(f"[ERR ] {name}: 未产出可解析报告  ({dt:.1f}s)")
                if out.strip():
                    print("   " + out.strip().splitlines()[-1][:160])

    n_obj_done = sum(len(v["owners"]) for v in results.values())
    tot = {k: sum((v["rep"] or {}).get(k, 0) for v in results.values())
           for k in ("n_pass", "n_fail", "n_warn", "n_exempt")}
    bad = [k for k, v in results.items()
           if v["rc"] != 0 or v["rep"] is None or v["rep"]["n_fail"]]

    print()
    print(f"对象 {n_obj_done}/{len(objs)} 已核"
          + (f"，{len(missing)} 待实现" if missing else "")
          + f"；核验项 {tot['n_pass']} 通过 / {tot['n_fail']} 失败"
          + (f" / {tot['n_exempt']} 豁免" if tot["n_exempt"] else "")
          + f"；脚本 {len(results)} 个，失败 {len(bad)} 个"
          + f"；耗时 {time.time() - t_all:.0f}s")

    # 只有全量运行才写主报告：子集跑出的报告会缺对象、缺跨对象核验，
    # 覆盖上去会让 REPORT.md 看起来"少了一半"。
    subset = bool(args.only or args.kind or args.sec or args.no_cross)
    if args.no_report:
        pass
    elif subset:
        print("（子集运行，未覆盖 REPORT.md；全量请跑 `python verify.py`）")
    else:
        write_report(objs, missing, results, tot, bad)
        print("主报告 -> REPORT.md")

    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
