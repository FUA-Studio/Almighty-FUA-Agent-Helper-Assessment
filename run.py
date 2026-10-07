#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AFAHA runner — terminal-bench 风格跨平台排障测评。用法见 README。"""
import argparse, json, os, platform, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TDIR = os.path.join(ROOT, "tasks")
RESULTS = os.path.join(ROOT, "results.json")
PY = sys.executable

TASKS = {
 "T01": {"name": "WIN: 更新servicing CLSID损坏修复", "plat": "win"},
 "T02": {"name": "Linux: NSS dbm索引库页损坏", "plat": "linux", "root": True},
 "T03": {"name": "Linux: ld.so.cache哈希桶损坏", "plat": "linux", "root": True},
 "T04": {"name": "Python: 分页采集三重隐藏bug", "plat": "any"},
 "T05": {"name": "Rust: 空category+滞后均值", "plat": "any", "need": ["cargo"]},
 "T06": {"name": "Rust: peek(Err)静默吞数据", "plat": "any", "need": ["cargo"]},
 "T07": {"name": "Go: 循环变量复用致输出重复", "plat": "any", "need": ["go"]},
 "T08": {"name": "Go: 幻觉应答服务", "plat": "any", "need": ["go"]},
 "T09": {"name": "Electron: 静默闪退连锁bug", "plat": "any", "need": ["node"]},
 "T10": {"name": "WIN三重耦合故障诊断(笔试)", "plat": "any"},
}

def plat_ok(tid):
    p = TASKS[tid]["plat"]
    s = platform.system()
    return (p == "any") or (p == "win" and s == "Windows") or (p == "linux" and s == "Linux")

def skip_reason(tid):
    if not plat_ok(tid):
        return "平台不匹配(需要" + TASKS[tid]["plat"] + ")"
    miss = [t for t in (TASKS[tid].get("need") or []) if not shutil.which(t)]
    if miss:
        return "缺少工具链: " + ','.join(miss)
    if TASKS[tid].get("root") and hasattr(os, "geteuid") and os.geteuid() != 0:
        return "需要 root"
    return None

def run_step(tid, step):
    d = os.path.join(TDIR, tid)
    print("===== " + tid + " " + step + " =====")
    r = subprocess.run([PY, os.path.join(d, step + ".py")], cwd=d)
    return r.returncode == 0

def do_task(tid, interactive):
    res = {"task": tid, "name": TASKS[tid]["name"]}
    sr = skip_reason(tid)
    if sr:
        res.update(skipped=True, reason=sr, passed=None)
        print("[SKIP] %s: %s" % (tid, sr))
        return res
    if not run_step(tid, "setup"):
        res.update(skipped=True, reason="setup失败", passed=None)
        return res
    print("故障环境已布置。阅读 tasks/" + tid + "/instructions.md 并排查修复。")
    print("完成后运行: python run.py --check " + tid)
    if interactive:
        try:
            input(">>> 修复完成后按回车开始评分...")
        except EOFError:
            pass
    passed = run_step(tid, "check")
    res.update(skipped=False, passed=passed)
    print("[%s] => %s" % (tid, "PASS" if passed else "FAIL"))
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--task")
    ap.add_argument("--setup")
    ap.add_argument("--check")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.list:
        for tid, t in TASKS.items():
            print(tid, t["plat"], t["name"])
        return
    if a.all:
        results = [do_task(tid, interactive=False) for tid in TASKS]
        json.dump(results, open(RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("已写入", RESULTS)
        return
    if a.setup:
        run_step(a.setup, "setup")
        return
    if a.check:
        run_step(a.check, "check")
        return
    if a.task:
        do_task(a.task, interactive=True)
        return
    ap.print_help()

if __name__ == "__main__":
    main()
