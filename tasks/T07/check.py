import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
out = os.path.join(WORK, "result.json")
if os.path.exists(out):
    os.remove(out)
r = subprocess.run(["go", "run", "."], cwd=WORK, capture_output=True, text=True, timeout=180)
if r.returncode != 0:
    print("FAIL: go run 退出码", r.returncode, r.stderr[-300:])
    sys.exit(1)
if not os.path.exists(out):
    print("FAIL: 未生成 result.json")
    sys.exit(1)
data = json.load(open(out, encoding="utf-8"))
want = [{"username": "alice", "age": 22}, {"username": "bob", "age": 28}, {"username": "dave", "age": 35}]
if data == want:
    print("PASS: 3条互不相同的有效用户")
    sys.exit(0)
print("FAIL: 期望", want, "实得", data)
sys.exit(1)
