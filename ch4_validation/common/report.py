"""
report.py — 单对象核验的记账与报告落地
=======================================
每个对象（一张表或一张图）一个 Checker 实例，产出一份 Markdown 报告。
报告固定四段，缺一段即视为该对象未核验完：

  1. 源清单      每条源的绝对可定位路径 + 角色（→ 可追溯）
  2. 双渠道交叉   xlsx 与 log 在同一 best epoch 下是否互相印证
  3. 印刷值比对   源值按印刷位数舍入后与 tex 印刷值逐字符比较
  4. 文段引用     正文引用该对象的数值是否与表格印刷值同值同位数

退出码 0 = 全通过；有 FAIL 则非 0，便于 verify.py 汇总。
"""
import os
import sys
import time

from . import paths


class Checker:
    def __init__(self, slug, title, obj_kind, tex_label, tex_number=None):
        self.slug = slug                # T04_ideal_overall
        self.title = title              # 人读标题
        self.kind = obj_kind            # 'table' | 'figure'
        self.label = tex_label
        self.number = tex_number
        self.sources = []
        self.sections = []              # [(标题, [行]), ...]
        self.cur = None
        self.n_pass = self.n_fail = self.n_warn = self.n_exempt = 0
        self.t0 = time.time()

    # ── 源清单 ────────────────────────────────────────────────────
    def source(self, role, path, note=""):
        self.sources.append((role, paths.rel(path) if path else "(缺失)", note))

    # ── 分段 ──────────────────────────────────────────────────────
    def section(self, name, cols=("检查项", "源值 / 印刷值", "结论")):
        self.cur = {"name": name, "cols": cols, "rows": []}
        self.sections.append(self.cur)

    def note(self, text):
        """写入一行说明（不计入通过率），用于交代口径或已知差异。"""
        if self.cur is None:
            self.section("说明")
        self.cur["rows"].append(("_note", text))

    def check(self, ok, item, detail="", warn_only=False):
        if self.cur is None:
            self.section("核验")
        if ok:
            self.n_pass += 1
            tag = "PASS"
        elif warn_only:
            self.n_warn += 1
            tag = "WARN"
        else:
            self.n_fail += 1
            tag = "**FAIL**"
        self.cur["rows"].append((item, detail, tag))
        return ok

    def exempt(self, item, reason):
        """登记一条豁免。豁免不是跳过：单列成行、必须带理由、计入总数，
        这样报告读者能看见『哪些断言被有意排除、为什么』。"""
        if self.cur is None:
            self.section("核验")
        self.n_exempt += 1
        self.cur["rows"].append((item, reason, "豁免"))
        return True

    def eq(self, item, src, printed, nd=3, warn_only=False):
        """源值 vs 印刷值。detail 里同时写出两侧，失败时无需再查脚本。"""
        from .metrics import eq_print, fmt
        ok = eq_print(src, printed, nd)
        s = "None" if src is None else f"{src!r}"[:24]
        detail = f"源 {s} → `{fmt(src, nd)}` / 印刷 `{printed}`"
        return self.check(ok, item, detail, warn_only)

    # ── 落地 ──────────────────────────────────────────────────────
    def total(self):
        return self.n_pass + self.n_fail + self.n_warn + self.n_exempt

    def verdict(self):
        return "PASS" if self.n_fail == 0 else "FAIL"

    def render(self):
        L = []
        num = f"{'Table' if self.kind == 'table' else 'Fig.'} {self.number}" if self.number else self.label
        L.append(f"# {num} — {self.title}")
        L.append("")
        L.append(f"- 对象：`{self.label}`（{num}）")
        ex = f" / {self.n_exempt} 豁免" if self.n_exempt else ""
        L.append(f"- 结论：**{self.verdict()}** — {self.n_pass} 通过 / "
                 f"{self.n_fail} 失败 / {self.n_warn} 警告{ex}，共 {self.total()} 项")
        L.append(f"- 脚本：`ch4_validation/scripts/{self.slug}.py`")
        L.append(f"- 生成：{time.strftime('%Y-%m-%d %H:%M:%S')}")
        L.append("")
        L.append("## 1. 源清单")
        L.append("")
        L.append("| 角色 | 路径 | 说明 |")
        L.append("|---|---|---|")
        for role, p, note in self.sources:
            L.append(f"| {role} | `{p}` | {note} |")
        L.append("")
        for sec in self.sections:
            L.append(f"## {sec['name']}")
            L.append("")
            notes = [r for r in sec["rows"] if r[0] == "_note"]
            rows = [r for r in sec["rows"] if r[0] != "_note"]
            for _, t in notes:
                L.append(f"> {t}")
                L.append("")
            if rows:
                L.append("| " + " | ".join(sec["cols"]) + " |")
                L.append("|" + "---|" * len(sec["cols"]))
                for r in rows:
                    L.append("| " + " | ".join(str(x) for x in r) + " |")
                L.append("")
        return "\n".join(L) + "\n"

    def finish(self, quiet=False):
        out = paths.report_path(self.slug)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(self.render())
        if not quiet:
            ex = f" / {self.n_exempt} exempt" if self.n_exempt else ""
            print(f"[{self.verdict()}] {self.slug}: "
                  f"{self.n_pass} pass / {self.n_fail} fail / {self.n_warn} warn{ex} "
                  f"-> {paths.rel(out)}")
        return 0 if self.n_fail == 0 else 1


def main(fn):
    """脚本入口装饰器：统一 sys.exit 语义。"""
    def wrapper():
        c = fn()
        sys.exit(c.finish())
    return wrapper
