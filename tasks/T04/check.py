import json, os, subprocess, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
sys.path.insert(0, HERE)
from catalog import expected
def up():
    try:
        urllib.request.urlopen("http://127.0.0.1:8931/list?page=1&size=1", timeout=2)
        return True
    except Exception:
        return False
if not up():
    subprocess.Popen([sys.executable, os.path.join(HERE, "goods_api.py")], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(1.5)
script = os.path.join(WORK, "fetch_goods.py")
out = os.path.join(WORK, "output_goods.json")
if os.path.exists(out):
    os.remove(out)
try:
    r = subprocess.run([sys.executable, script], cwd=WORK, timeout=90, capture_output=True, text=True)
    print(r.stdout[-200:], r.stderr[-200:])
except subprocess.TimeoutExpired:
    print("FAIL: 脚本90秒未结束(疑似死循环)")
    sys.exit(1)
if not os.path.exists(out):
    print("FAIL: 未生成 output_goods.json")
    sys.exit(1)
got = json.load(open(out, encoding="utf-8"))
exp = expected()
if got == exp:
    print("PASS: %d 条商品与期望完全一致" % len(exp))
    sys.exit(0)
print("FAIL: 期望%d条且逐条一致, 实得%d条" % (len(exp), len(got)))
print("期望头2条:", exp[:2])
print("实得头2条:", got[:2])
sys.exit(1)
