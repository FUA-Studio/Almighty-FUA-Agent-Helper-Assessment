import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work')
main = open(os.path.join(WORK, 'main.js'), encoding='utf-8').read()
pre = open(os.path.join(WORK, 'preload.js'), encoding='utf-8').read()
ok = True
for f in ('main.js', 'preload.js'):
    r = subprocess.run(['node', '--check', os.path.join(WORK, f)], capture_output=True, text=True)
    if r.returncode != 0:
        print('FAIL 语法:', f, r.stderr[:200])
        ok = False
def chk(name, cond):
    global ok
    print(('OK  ' if cond else 'MISS'), name)
    ok = ok and cond
chk('不再全局保留原生fd(无 openedFileHandle=fd)', not re.search(r'openedFileHandle\\s*=\\s*fd', main))
chk('使用 close 释放句柄', 'close' in main)
chk('监听渲染进程崩溃(crashed/render-process-gone)', bool(re.search(r'(render-process-gone|crashed)', main)))
chk('printToPDF 前判断窗口销毁', 'isDestroyed' in main)
chk('printToPDF/print 有异常捕获', len(re.findall(r'try\\s*{[\\s\\S]{0,400}?printToPDF|printToPDF[\\s\\S]{0,200}catch', main)) > 0 or main.count('try') >= 2)
chk('preload 透传 unhandledrejection/uncaughtException', bool(re.search(r'(unhandledrejection|uncaughtException)', pre)))
chk('IPC handler 有 try-catch', len(re.findall(r'catch', main)) >= 2)
print('PASS: 连锁缺陷修复到位' if ok else 'FAIL: 尚有缺陷未处理')
sys.exit(0 if ok else 1)
