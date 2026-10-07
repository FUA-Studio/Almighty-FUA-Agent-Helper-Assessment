# T07 Go 用户过滤导出(循环别名陷阱)

## 现象
- go run . 编译运行成功、无 panic、退出码 0、生成 result.json
- 打印 total items: 3(条数正确)
- 但 result.json 里所有对象全部是最后一条有效记录 dave/35 的内容,全部重复

## 任务
修复 work/main.go,使 result.json 输出 3 条互不相同的有效用户(alice/22, bob/28, dave/35)。
禁止改 users.json 输入。

完成后运行: python run.py --check T07(需要本机有 go)
