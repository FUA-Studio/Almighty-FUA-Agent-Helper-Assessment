# T03 ld.so.cache 哈希桶局部损坏

## 现象
- /opt/afaha_t03/hello 依赖的 libafaha.so.1 明明在搜索路径内,ldd 却报 not found
- 其它程序动态链接完全正常;库文件本身 ELF 完好;ld.so.conf 文本正确
- ldconfig 直接运行返回 0 不报错;设 LD_LIBRARY_PATH 绕过缓存故障即消失
- 重装任何软件包无效

## 任务
定位根因并彻底修复,使 ldd /opt/afaha_t03/hello 正常解析、程序能直接运行输出 answer=42。
不得删除或重编译 libafaha.so.1 与 hello 本体。

完成后运行: python run.py --check T03(需要 root;setup 需本机有 gcc)
