import os, shutil, subprocess, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
os.makedirs(WORK, exist_ok=True)
shutil.copy(os.path.join(HERE, "broken_fetch_goods.py"), os.path.join(WORK, "fetch_goods.py"))
def up():
    try:
        urllib.request.urlopen("http://127.0.0.1:8931/list?page=1&size=1", timeout=2)
        return True
    except Exception:
        return False
if not up():
    subprocess.Popen([sys.executable, os.path.join(HERE, "goods_api.py")], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(1.5)
print("mock API: " + ("up" if up() else "DOWN"))
print("工作目录: " + WORK)
