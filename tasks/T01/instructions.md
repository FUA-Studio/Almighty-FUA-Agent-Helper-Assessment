# T01 Windows 更新 servicing CLSID 损坏修复

## 现象
- Windows 更新无法安装;SFC /SCANNOW 报错;DISM 报错
- 控制面板的程序与功能点开报: 接口未实现

## 已知线索(来自现场取证)
注册表 CLSID 项 {0823B6F8-F499-4d5e-B885-EA9CB4F43B24} 内容损坏:
- 默认值与 AppID 均被写坏,LocalServer32 指向不存在的 DLL
- 该 CLSID 对应 Component Based Servicing Worker( servicing 宿主)

## 任务
修复该注册表项,使其恢复为可正常拉起 servicing worker 的正确状态:
- 默认值: Component Based Servicing Worker
- AppID: {8D15A4F3-1BE5-4120-8A4D-2EF92A5DD58D}
- LocalServer32 默认值: 指向当前系统 WinSxS 内真实的 TiWorker.exe(路径随系统版本而变)
提示: 可先删除整个键再按上述语义重建;WinSxS 真实路径可用 dir 搜索 TiWorker.exe 获得。

完成后(管理员权限)运行: python run.py --check T01
