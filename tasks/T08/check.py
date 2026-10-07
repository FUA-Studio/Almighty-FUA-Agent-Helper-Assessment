import json, os, socket, subprocess, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
def port_open(p):
    s = socket.socket()
    try:
        s.connect(("127.0.0.1", p))
        s.close()
        return True
    except Exception:
        s.close()
        return False
def post(q):
    req = urllib.request.Request("http://127.0.0.1:8080/ask", data=json.dumps({"query": q}).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode())["answer"]
proc = subprocess.Popen(["go", "run", "."], cwd=WORK, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        if port_open(8080):
            break
        time.sleep(1)
    else:
        print("FAIL: 服务未在60秒内监听8080")
        sys.exit(1)
    a1 = post("计算水从20度升到80度需要多少热量")
    a2 = post("虚空之刃的月相引力常数是多少")
finally:
    try:
        proc.kill()
    except Exception:
        pass
templates = ["耦合换算", "经验常数", "非线性变化", "边界条件", "修正系数", "微弱偏移", "目标物理量", "优化参数取值"]
ok1 = ("252000" in a1.replace(",", ""))
ok2 = (not any(t in a2 for t in templates))
print("热量题:", a1[:120])
print("虚构题:", a2[:120])
if ok1 and ok2:
    print("PASS: 真实问题给出正确计算,虚构问题诚实回答")
    sys.exit(0)
if not ok1:
    print("FAIL: 热量题未给出正确数值252000")
if not ok2:
    print("FAIL: 虚构题仍在输出模板幻觉")
sys.exit(1)
