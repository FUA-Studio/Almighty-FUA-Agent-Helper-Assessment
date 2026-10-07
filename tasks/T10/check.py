import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
f = os.path.join(HERE, 'solution.md')
if not os.path.exists(f):
    print('FAIL: 未找到 solution.md(请在本目录按 instructions.md 撰写诊断)')
    sys.exit(1)
txt = open(f, encoding='utf-8').read()
low = txt.lower()
ITEMS = [
    ('WinSxS/组件存储定位', r'dism'), 
    ('RestoreHealth/ScanHealth 修复', r'(restorehealth|scanhealth)'), 
    ('sfc 顺序说明', r'sfc'), 
    ('0x800f081f 含义', r'0x800f081f'), 
    ('Explorer Bags/BagsMRU 注册表', r'bags'), 
    ('新账户隔离验证', r'(新(建|的)?(管理)?(账户|用户)|new .*user|新建本地)'), 
    ('UWP 包重注册', r'appxpackage'), 
    ('顺序不可颠倒的理由', r'(顺序|先.*后|颠倒|之前)')
]
hit = 0
for name, pat in ITEMS:
    found = re.search(pat, low)
    print(('OK  ' if found else 'MISS'), name)
    hit += 1 if found else 0
score = hit / len(ITEMS)
print('得分: %d/%d' % (hit, len(ITEMS)))
if hit >= 6:
    print('PASS')
    sys.exit(0)
print('FAIL: 覆盖点不足(需≥6/8)')
sys.exit(1)
