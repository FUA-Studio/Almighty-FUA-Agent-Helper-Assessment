# T09 Electron 编辑器静默闪退(连锁bug)

## 现象
- npm start 后主窗口正常渲染,无任何报错
- 反复执行 打开→修改→另存为→新建 数轮后(8~15次),点击【导出PDF】或【打印】→ 程序瞬间静默退出,窗口消失,控制台无任何 error/exception
- 单纯静态读代码很难发现;必须交互触发;修一处另一处依旧潜伏

## 任务
修复 work/ 内的连锁缺陷,要求全部处理:
1. 文件句柄泄漏: 每处 fs.open 的 fd 用完必须 close;新建/另存为覆盖全局句柄前先关闭旧 fd;不要长期持有原生 fd(建议只存路径字符串,按路径 open-write-close)
2. 崩溃可见化: 主进程监听 webContents 的 crashed / render-process-gone,写日志;preload 监听 unhandledrejection/uncaughtException 并透传给主进程记录
3. printToPDF/print 前判断窗口销毁,并加完整异常捕获(失败经 IPC 返回前端提示而非静默崩)
4. 各 IPC handler 包裹 try-catch

完成后运行: python run.py --check T09(需要 node;评分=静态检查+语法检查)
