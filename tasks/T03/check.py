import subprocess, sys
r = subprocess.run(["ldd", "/opt/afaha_t03/hello"], capture_output=True, text=True)
if "not found" in r.stdout:
    print("FAIL: ldd 仍解析不到:", r.stdout.strip()[:200])
    sys.exit(1)
r2 = subprocess.run(["/opt/afaha_t03/hello"], capture_output=True, text=True)
if r2.returncode == 0 and "answer=42" in r2.stdout:
    print("PASS: 动态链接已恢复", r2.stdout.strip())
    sys.exit(0)
print("FAIL: 运行异常", r2.stdout, r2.stderr)
sys.exit(1)
