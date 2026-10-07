import os, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
os.makedirs(os.path.join(WORK, "src"), exist_ok=True)
for f in ["Cargo.toml", "src/main.rs", "data.csv"]:
    shutil.copy(os.path.join(HERE, f) if os.path.exists(os.path.join(HERE, f)) else os.path.join(HERE, "work", f), os.path.join(WORK, f))
print("T06 环境就绪: " + WORK)
