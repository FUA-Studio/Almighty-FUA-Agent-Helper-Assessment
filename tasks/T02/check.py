import subprocess, sys
ok = True
for name, uid in [("afaha_alice", 61001), ("afaha_bob", 61002), ("afaha_carol", 61003)]:
    r = subprocess.run(["getent", "passwd", name], capture_output=True, text=True)
    good = r.returncode == 0 and (":" + str(uid) + ":") in r.stdout
    print(("OK  " if good else "FAIL"), name, "->", r.stdout.strip()[:60] or "(空)")
    ok = ok and good
print("PASS: NSS 查询全部恢复正常" if ok else "FAIL: 仍有用户解析异常")
sys.exit(0 if ok else 1)
