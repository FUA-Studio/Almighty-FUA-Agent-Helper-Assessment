# T05 Rust 分类统计(静默数据错误)

## 现象
- cargo build 无任何警告/错误、运行不 panic、退出码 0、输出 JSON
- 但输出里所有 category 字段全部是空字符串
- 平均值统计与真实值系统性偏差(数值错乱)

## 任务
修复 work/src/main.rs(两处隐蔽 bug),使输出为:
  A: total=30 count=2 avg=15;  B: total=20 count=2 avg=10
(按 category 正确分组,category 字段为真实名称,均值为算术平均)

完成后运行: python run.py --check T05(需要本机有 cargo)
