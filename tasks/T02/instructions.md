# T02 Linux NSS dbm 二进制索引页损坏

## 现象(高度碎片化,无单一明确报错)
- 部分用户 id/getent 查不到,但 cat /etc/passwd 里条目完整且 md5 正常
- su 报 user does not exist 但用户明明存在;同一命令两个终端结果不同
- 文本文件、磁盘、glibc 包全部完好;重装软件包无效

## 任务
找出根因并彻底修复,使 afaha_alice / afaha_bob / afaha_carol 三个用户的
getent/id 查询全部恢复正常且结果正确。允许重建缓存或调整 NSS 源顺序,
但不得删除这三个系统用户本身。

完成后运行: python run.py --check T02(需要 root)

提示: 本题为一次性容器/VM 设计,setup 已备份 /etc/nsswitch.conf 到 .afaha.bak
