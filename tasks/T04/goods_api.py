import json, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from catalog import PAGES
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        page = int(q.get("page", ["1"])[0])
        size = int(q.get("size", ["20"])[0])
        i = page - 1
        if i < 0 or i >= len(PAGES):
            body = {"data": {"items": [], "has_more": False}}
        else:
            body = {"data": {"items": PAGES[i]["items"][:size], "has_more": PAGES[i]["has_more"]}}
        b = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)
    def log_message(self, *a):
        pass
HTTPServer(("127.0.0.1", 8931), H).serve_forever()
