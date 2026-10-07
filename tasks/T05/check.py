import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
EXPECT = {"A": {30.0, 2, 15.0}, "B": {20.0, 2, 10.0}}
r = subprocess.run(["cargo", "run", "-q"], cwd=WORK, capture_output=True, text=True, timeout=300)
if r.returncode != 0:
    print("FAIL: cargo run 退出码", r.returncode, r.stderr[-300:])
    sys.exit(1)
try:
    data = json.loads(r.stdout)
except Exception as e:
    print("FAIL: 输出不是合法JSON", e)
    sys.exit(1)
got = {d.get("category", ""): {d.get("total"), d.get("count"), round(d.get("avg", -1), 6)} for d in data}
ok = True
for c, exp in EXPECT.items():
    if c not in got or exp != got[c]:
        ok = False
        print("FAIL:", c, "期望", exp, "实得", got.get(c))
if ok:
    print("PASS: category 正确且均值正确")
    sys.exit(0)
sys.exit(1)
