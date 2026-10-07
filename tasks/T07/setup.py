import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
os.makedirs(WORK, exist_ok=True)
if not os.path.exists(os.path.join(WORK, "main.go")):
    print("work 目录即题目环境,main.go/main.go 已就位")
print("T07 环境就绪: " + WORK)
