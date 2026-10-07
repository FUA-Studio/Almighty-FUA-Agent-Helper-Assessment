# T04 分页商品采集脚本修复

## 业务需求
从分页 API 拉取商品数据并导出 JSON:
- GET http://127.0.0.1:8931/list?page=N&size=20
- 从 page=1 开始,直到返回的 data.has_more 为 false
- 只收集 status==1 的有效商品
- 每条补全 source_page 字段(记录来自第几页)
- 最终写入 work/output_goods.json(全部有效商品列表)

## 现象
- 现有脚本 work/fetch_goods.py 运行不报错、退出码 0、输出文件存在
- 但导出数据大量重复(同一页内多条记录内容完全相同),与真实目录不符
- API 偶发抖动时脚本可能永远不结束

## 要求
修复 work/fetch_goods.py(mock API 本身不得修改),使输出与真实目录完全一致,
且网络异常时不得死循环。API 已由 setup 启动在 127.0.0.1:8931。
修复完成后运行: python run.py --check T04
