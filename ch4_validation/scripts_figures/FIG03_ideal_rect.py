#!/usr/bin/env python3
"""
Fig. 3 (fig:ideal-rect) 核验脚本
验证矩形理想波导解析验证图（R0, Case 1）的数值可追溯性
"""
import sys, os, importlib.util
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from common import paths, report
from common import texparse as T

# 导入绘图脚本作为口径防漂移的权威源
# 用基于 __file__ 的绝对路径：相对路径会依赖 cwd 恰为 scripts_figures/，
# 从 verify.py（cwd=包根）或克隆后的任意位置调用都会断。
SCRIPT = (Path(__file__).resolve().parents[2]
          / "Validation_Scripts" / "regen_ideal_panels.py")
spec = importlib.util.spec_from_file_location("rip", SCRIPT)
RIP = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RIP)

LABEL = "fig:ideal-rect"
CASE = "Case01_R0"
CASE_NO = 1

# Table 5 (tab:ideal-depthline) 印刷的 R0 行：TL MAE 与 Src 坐标（2位小数）
TABLE5_R0 = {
    25:  {"tl": 0.151, "src": (39.5, 36.4)},
    50:  {"tl": 0.130, "src": (49.5, 38.1)},
    75:  {"tl": 0.341, "src": (87.5, 107.8)},
    100: {"tl": 0.430, "src": (22.7, 54.0)},
}


def run():
    c = report.Checker("FIG03_ideal_rect",
                       "Fig. 3 矩形理想波导解析验证（R0, Case 1）",
                       "figure", LABEL, "ideal-rect")

    # ── A ────────────────────────────────────────────────────────
    c.section("1. 数据源与绘图脚本")
    c.note("验证 npz 文件存在、绘图脚本可导入、口径防漂移（函数签名不变）")

    npz_path = paths.npz_path(CASE_NO)
    c.check(npz_path and os.path.exists(npz_path), "npz 文件存在",
            paths.rel(npz_path) if npz_path else "未找到")

    # ★ 绘图脚本按 CASE_ROOT=D:\Data\Case1-2 取数，而权威原始数据在
    #   Raw_Experimental_Data 下。二者必须逐字节相同，否则图与核验分属两份数据。
    import hashlib
    mirror = Path(RIP.CASE_ROOT) / CASE / f"{CASE}__TL原始数据_ep200.npz"
    same = (mirror.exists() and npz_path and
            hashlib.md5(mirror.read_bytes()).hexdigest() ==
            hashlib.md5(Path(npz_path).read_bytes()).hexdigest())
    c.check(same, "绘图脚本取数目录与 Raw_Experimental_Data 同源",
            f"md5 相同（{paths.rel(str(mirror))}）" if same else "两份 npz 不一致")

    c.check(SCRIPT.exists(), "绘图脚本存在", str(SCRIPT))
    c.check(hasattr(RIP, 'load'), "load 函数可导入", "口径防漂移")
    c.check(hasattr(RIP, 'pick_sample'), "pick_sample 函数可导入", "口径防漂移")
    c.check(hasattr(RIP, 'FREQS'), "FREQS 常量可导入", str(RIP.FREQS))

    # ── B ────────────────────────────────────────────────────────
    c.section("2. Epoch 自证（npz metadata）")
    c.note("验证 npz 内的 epoch 字段与 caption 声明一致")

    data = RIP.load(CASE)
    epoch = int(data['epoch'])
    c.check(epoch == 200, "npz epoch 字段", f"epoch={epoch}, 预期 200 (last)")

    # ★ 双侧判据：不能只查"caption 有 last 字样"。图取 ep200(last)，
    #   而表取 best epoch，两者本是不同轮。须同时断言 caption 未误写 best，
    #   否则把 caption 改成 best 也照样通过。
    from common import metrics as M
    be = M.xlsx_case(paths.xlsx_path('4.2'), CASE_NO)['best_epoch']
    c.check(be is not None, f"xlsx 记录 Case {CASE_NO} 的 best epoch", f"best={be}")
    c.note(f"Case {CASE_NO}: best epoch={be}，图取 last=200。"
           + ("二者恰好相等（巧合），但 caption 仍应按数据来源写 last。"
              if be == 200 else
              f"二者相差 {abs(200 - be)} 轮，caption 写 best 即为错。"))

    cap = T.caption_of(LABEL)
    c.check('best epoch' not in cap,
            "caption 未误写 best epoch",
            "图源自 ep200 npz，非 best-epoch 评估")
    has_last = 'last epoch' in cap or 'final epoch' in cap
    c.check(has_last, "Caption 声明 epoch", "声明 'last epoch'" if has_last else "未声明")

    # ── C ────────────────────────────────────────────────────────
    c.section("3. 深度线 MAE 反向验证（与 Table 5 对齐）")
    c.note("从 npz 全精度重算 MAE，舍入 3 位后与 Table 5 印刷值比对")

    for freq in RIP.FREQS:
        idx, mae_full = RIP.pick_sample(data, freq)
        mae_3dp = round(mae_full, 3)
        tl_printed = TABLE5_R0[freq]["tl"]

        c.check(mae_3dp == tl_printed,
                f"{freq} Hz TL MAE (idx={idx})",
                f"npz全精度 {mae_full:.9f} → 3dp {mae_3dp:.3f} / 表印 {tl_printed:.3f}")

    # ── D ────────────────────────────────────────────────────────
    c.section("4. Source 坐标反向验证（与 Table 5 / 图标题对齐）")
    c.note("从 npz source_pos 舍入 1 位后与 Table 5 Src 列、图面板标题比对。"
           "全章坐标统一 1 位小数（深度线与场图同口径）。")

    for freq in RIP.FREQS:
        idx, _ = RIP.pick_sample(data, freq)
        x_full, y_full = (float(v) for v in data['source_pos'][idx])
        x_1dp, y_1dp = round(x_full, 1), round(y_full, 1)
        src_printed = TABLE5_R0[freq]["src"]

        ok = (x_1dp, y_1dp) == src_printed
        c.check(ok, f"{freq} Hz Src 坐标 (idx={idx})",
                f"npz全精度 ({x_full:.6f},{y_full:.6f}) → 1dp ({x_1dp:.1f},{y_1dp:.1f}) / 表印 {src_printed}")

    # ── E ────────────────────────────────────────────────────────
    c.section("5. 图文件存在性")
    c.note("验证论文引用的 PDF 文件存在")

    pdf_rel = "Figures/results/Case01_R0_grid2.pdf"
    pdf_path = Path(paths.TEX).parent / pdf_rel
    c.check(pdf_path.exists(), "图片文件存在", pdf_rel)

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 样本选择一致性")
    c.note("确认 pick_sample 返回的样本索引与预期一致（4频率8样本中MAE最小者）")

    expected_idx = {25: 1, 50: 3, 75: 4, 100: 7}  # 从重算结果得出
    for freq in RIP.FREQS:
        idx, _ = RIP.pick_sample(data, freq)
        c.check(idx == expected_idx[freq],
                f"{freq} Hz 样本索引",
                f"idx={idx}, 预期={expected_idx[freq]}")

    # ── F ────────────────────────────────────────────────────────
    c.section("6. 正文引用：被引 + 说明与图内容相符")
    txt = T.tex_text()
    hits = T.sentences_with(r"rectangular case in Fig", txt)
    c.check(bool(hits), "正文（4.2 节）引用本图",
            f"tex 行 {T.line_of(hits[0][0], txt)}" if hits else "未找到")

    # 正文称 "Two held-out samples at every frequency" —— 逐条核结构
    c.note("正文断言『每个频率两个留出样本』。npz 共 8 个样本、4 个频率，"
           "每频率恰 2 个；图按 pick_two 排两列(a/b)，与该断言一致。")
    c.check(bool(hits) and "Two held-out samples at every frequency" in
            txt[max(0, hits[0][0] - 300):hits[0][0] + 200],
            "正文该断言可定位", "含 `Two held-out samples at every frequency`")
    freqs = [int(f) for f in data["freq"]]
    per = {f: freqs.count(f) for f in set(freqs)}
    c.check(len(freqs) == 8 and set(per.values()) == {2},
            "npz 每频率恰 2 个样本", f"频率计数 {per}")
    for freq in RIP.FREQS:
        ids = RIP.pick_two(data, freq)
        c.check(len(ids) == 2 and len(set(ids)) == 2,
                f"{freq} Hz 图上取 2 个不同样本", f"idx={list(ids)}")

    # ── G ────────────────────────────────────────────────────────
    c.section("7. caption 的取样措辞与实际机制相符")
    c.note("本图用 pick_two：按 y=Y_LINE 行的 MAE 升序取前 2 个，是**择优**"
           "取样。caption 若含混称 representative，读者会以为是随机抽样，"
           "故要求写明按深度线 MAE 择优。（场图族用 pick_rows 按索引顺序取前 "
           "2 个，措辞是 the first two，两者不可混用。）")
    cap_s = T.caption_of(LABEL) or ""
    # 校验语义而非字面：措辞可以是 "best-matching ... ordered by depth-line MAE"
    # 或 "of lowest depth-line MAE"，只要点明依 MAE 择优即可，避免题注一改写
    # 断言就失败。
    c.check("depth-line MAE" in cap_s, "caption 写明排序依据为深度线 MAE", "")
    c.check(any(w in cap_s for w in ("best-matching", "lowest", "smallest")),
            "caption 点明是择优取样（best-matching / lowest 等）",
            "不可只说取两个样本而不说依据")
    c.check("representative" not in cap_s,
            "caption 未含混使用 representative", "择优取样不应称 representative")
    # 证实确为升序择优：首列样本的 MAE 应不大于次列
    for freq in RIP.FREQS:
        i0, i1 = RIP.pick_two(data, freq)[:2]
        m0 = RIP.pick_sample(data, freq)[1]
        c.check(i0 == RIP.pick_sample(data, freq)[0],
                f"{freq} Hz a 列即 MAE 最优样本",
                f"pick_two 首个 idx={i0}，pick_sample idx="
                f"{RIP.pick_sample(data, freq)[0]}，MAE={m0:.6f}")

    return c


if __name__ == "__main__":
    sys.exit(run().finish())
