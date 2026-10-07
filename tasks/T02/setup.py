import os, random, shutil, subprocess, sys
USERS = [("afaha_alice", 61001), ("afaha_bob", 61002), ("afaha_carol", 61003)]
DBDIR = "/var/lib/misc/nss_db"
NSW = "/etc/nsswitch.conf"
def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
for name, uid in USERS:
    if sh("id " + name).returncode != 0:
        r = sh("useradd -M -u %d -s /usr/sbin/nologin %s" % (uid, name))
        if r.returncode != 0:
            open("/etc/passwd", "a").write("%s:x:%d:%d::/tmp:/bin/false\\n" % (name, uid, uid))
            open("/etc/group", "a").write("%s:x:%d:\\n" % (name, uid))
if not os.path.exists("/usr/bin/makedb"):
    print("安装 libnss-db ...")
    sh("apt-get install -y -qq libnss-db db-util >/dev/null 2>&1")
if not os.path.exists("/usr/bin/makedb"):
    print("FAIL: 缺少 makedb(libnss-db), 无法布置本题")
    sys.exit(1)
if not os.path.exists(NSW + ".afaha.bak"):
    shutil.copy(NSW, NSW + ".afaha.bak")
txt = open(NSW).read().splitlines()
out = []
for ln in txt:
    if ln.startswith("passwd:"):
        ln = "passwd: db [NOTFOUND=return UNAVAIL=return TRYAGAIN=return] files"
    out.append(ln)
open(NSW, "w").write(chr(10).join(out) + chr(10))
os.makedirs(DBDIR, exist_ok=True)
for f in ("passwd", "group", "shadow"):
    dst = os.path.join(DBDIR, f + ".db")
    for args in (["makedb", "-o", dst, "/etc/" + f], ["makedb", dst, "/etc/" + f]):
        subprocess.run(args, capture_output=True, text=True)
        if os.path.exists(dst) and os.path.getsize(dst) > 100:
            break
def symptom():
    r = subprocess.run(["getent", "passwd", "afaha_alice"], capture_output=True, text=True)
    return ("afaha_alice" not in r.stdout) or ("61001" not in r.stdout)
ok = False
for attempt in range(12):
    for f in ("passwd.db", "group.db"):
        p = os.path.join(DBDIR, f)
        sz = os.path.getsize(p)
        with open(p, "r+b") as fh:
            fh.seek(int(sz * random.uniform(0.3, 0.85)))
            fh.write(bytes(random.getrandbits(8) for _ in range(512)))
    if symptom():
        ok = True
        break
print("症状自校验:" + ("已复现(getent 查不到 afaha_alice)" if ok else "未能复现(本机NSS行为不同)"))
sys.exit(0 if ok else 1)
