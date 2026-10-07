import os, random, shutil, subprocess, sys
WORK = "/opt/afaha_t03"
LIBDIR = WORK + "/lib"
def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)
if not shutil.which("gcc"):
    print("FAIL: 缺少 gcc,无法布置本题")
    sys.exit(1)
os.makedirs(LIBDIR, exist_ok=True)
open(WORK + "/afaha.c", "w").write("int afaha_answer(void){return 42;}")
sh("gcc -shared -fPIC -o " + LIBDIR + "/libafaha.so.1 " + WORK + "/afaha.c")
open(WORK + "/hello.c", "w").write("#include <stdio.h>" + chr(10) + "extern int afaha_answer(void);" + chr(10) + "int main(void){printf(" + chr(34) + "answer=%d" + chr(92) + "n" + chr(34) + ", afaha_answer()); return 0;}" + chr(10))
sh("gcc -o " + WORK + "/hello " + WORK + "/hello.c -L" + LIBDIR + " -lafaha")
conf = "/etc/ld.so.conf.d/afaha.conf"
open(conf, "w").write(LIBDIR + chr(10))
sh("ldconfig")
r = sh("ldd " + WORK + "/hello")
if "not found" in r.stdout or "afaha" not in r.stdout:
    print("ldd 输出:", r.stdout)
    print("FAIL: 依赖未建立")
    sys.exit(1)
CACHE = "/etc/ld.so.cache"
sz = os.path.getsize(CACHE)
ok = False
for attempt in range(15):
    data = bytearray(open(CACHE, "rb").read())
    pos = int(sz * random.uniform(0.35, 0.9))
    for i in range(160):
        data[pos + i] = (data[pos + i] ^ 0x5A) & 0xFF
    open(CACHE, "wb").write(bytes(data))
    r = sh("ldd " + WORK + "/hello 2>&1")
    if "not found" in r.stdout:
        ok = True
        break
    sh("ldconfig")
print("症状自校验:" + ("已复现(ldd 找不到 libafaha)" if ok else "未能复现"))
sys.exit(0 if ok else 1)
