# AFAHA — Almighty-FUA-Agent-Helper-Assessment

终端排障能力测评套件（terminal-bench 风格、跨平台、零依赖起步）。

## 快速开始
    git clone <本仓库> && cd AFAHA
    python run.py --list          # 查看任务与平台适配
    python run.py --task T04      # 布置故障 → 按 instructions.md 修复 → 回车评分
    python run.py --all           # 跑全部(自动跳过平台不符/缺工具链的)

## 工作流（与 terminal-bench 对齐）
    setup 布置故障环境 → 被测 agent 只阅读 tasks/Txx/instructions.md（只有症状无答案）
    → 排查修复 → check 独立评分 → results.json 汇总

## 任务矩阵
| ID | 平台 | 依赖 | 主题 |
|----|------|------|------|
| T01 | Windows | PowerShell | 注册表 CLSID 损坏致更新/安装程序报接口未实现 |
| T02 | Linux(root) | libnss-db | NSS dbm 二进制索引页损坏(文本完好/getent 误导) |
| T03 | Linux(root) | gcc | ld.so.cache 哈希桶损坏(库在但部分程序找不到) |
| T04 | 双平台 | python3 | 分页采集:共享字典/异常吞噬/状态污染三重隐藏bug |
| T05 | 双平台 | cargo | 分类统计:空category+滞后均值(可编译的所有权变体) |
| T06 | 双平台 | cargo | peek(Err) 静默吞掉剩余全部数据 |
| T07 | 双平台 | go | 循环变量复用→输出全为最后一条 |
| T08 | 双平台 | go | 幻觉应答服务(不处理用户输入) |
| T09 | 双平台 | node+npm | Electron 静默闪退连锁bug(fd泄漏→打印/导出引爆) |
| T10 | 双平台 | - | Windows 三重耦合故障诊断(笔试题) |

## 评分
每题 check.py 独立验证最终产物/环境状态输出 PASS/FAIL；
    python run.py --all 汇总生成 results.json（含跳过原因）。

## 注意
- T02/T03 会真实修改系统 NSS / ld.so.cache，请在一次性容器/VM 里运行。
- T01 只在真实 Windows 上运行；setup 只破坏题目涉及的 CLSID 键。
- T07 的循环别名bug特意写成与 Go 版本无关的变体(外部复用变量+取指针)。
- T09 评分采用静态检查(崩溃需 GUI 交互复现，CI 无法点击)。
