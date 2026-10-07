# T06 Rust 分类统计(peek 陷阱)

## 现象
- cargo build 成功、运行不 panic、输出 JSON、退出码 0
- 但只要 CSV 中存在任意一行解析失败,其后所有有效数据全部被静默跳过
- 统计总数偏少、无任何报错

## 任务
修复 work/src/main.rs:让所有有效行都计入统计(解析失败的行跳过并继续,不中断整体流程)。
期望输出(按 category 排序): A total=60 count=3 avg=20; B total=20 count=2 avg=10。

完成后运行: python run.py --check T06(需要本机有 cargo)
