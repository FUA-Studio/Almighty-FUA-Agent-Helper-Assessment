import json, urllib.request, urllib.parse
API_URL = "http://127.0.0.1:8931/list"
PAGE_SIZE = 20
all_goods = []
resp_json = {}
page = 1
def parse_one_page(resp_data, page_num):
    goods_list = resp_data.get("data", {}).get("items", [])
    item_out = {}
    for item in goods_list:
        if item.get("status") != 1:
            continue
        item_out["id"] = item["id"]
        item_out["name"] = item["name"]
        item_out["price"] = item["price"]
        item_out["source_page"] = page_num
        all_goods.append(item_out)
    return resp_data.get("data", {}).get("has_more", False)
while True:
    payload = urllib.parse.urlencode({"page": page, "size": PAGE_SIZE})
    try:
        r = urllib.request.urlopen(API_URL + "?" + payload, timeout=8)
        resp_json = json.loads(r.read().decode())
    except Exception:
        pass
    has_more = parse_one_page(resp_json, page)
    if not has_more:
        break
    page = page + 1
with open("output_goods.json", "w", encoding="utf-8") as f:
    json.dump(all_goods, f, ensure_ascii=False, indent=2)
print("done", len(all_goods))
