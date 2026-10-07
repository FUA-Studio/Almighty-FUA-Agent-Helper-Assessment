PAGES = []
def _mk(lo, hi, invalid):
    items = []
    for i in range(lo, hi):
        items.append({"id": i, "name": "goods-%d" % i, "price": round(1.0 + (i * 7 % 97) / 3.0, 2), "status": 0 if i in invalid else 1})
    return items
PAGES.append({"items": _mk(101, 121, {107, 115}), "has_more": True})
PAGES.append({"items": _mk(121, 141, {123, 131, 138}), "has_more": True})
PAGES.append({"items": _mk(141, 149, {144}), "has_more": False})
def expected():
    out = []
    for p, pg in enumerate(PAGES, 1):
        for it in pg["items"]:
            if it["status"] == 1:
                out.append({"id": it["id"], "name": it["name"], "price": it["price"], "source_page": p})
    return out
