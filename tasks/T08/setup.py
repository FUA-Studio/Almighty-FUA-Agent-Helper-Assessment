import os, socket
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
assert os.path.exists(os.path.join(WORK, "main.go")), "main.go 缺失"
s = socket.socket()
try:
    s.connect(("127.0.0.1", 8080))
    s.close()
    print("警告: 8080 已被占用,check 前请先释放")
except Exception:
    s.close()
print("T08 环境就绪: " + WORK)
