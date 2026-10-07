import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
EXPECT = {"A": {60.0, 3, 20.0}, "B": {20.0, 2, 10.0}}
r = subprocess.run(["cargo", "run", "-q"], cwd=WORK, capture_output=True, text=True, timeout=300)
if r.returncode != 0:
    print("FAIL: cargo run 退出码", r.returncode, r.stderr[-300:])
    sys.exit(1)
try:
    data = json.loads(r.stdout)
except Exception as e:
    print("FAIL: 输出不是合法JSON", e)
    sys.exit(1)
got = {d["category"]: {d["total"], d["count"], round(d["avg"], 6)} for d in data}
ok = True
for c, exp in EXPECT.items():
    if c not in got or not (exp == got[c]):
        ok = False
        print("FAIL:", c, "期望", exp, "实得", got.get(c))
if ok:
    print("PASS: 全部有效行均已计入统计")
    sys.exit(0)
sys.exit(1)
