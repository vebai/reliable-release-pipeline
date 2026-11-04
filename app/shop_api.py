"""Tiny Shop API for the book's release evidence exercise. Standard library only."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PRODUCTS = [{"id": "sku-001", "name": "Notebook", "price_pence": 499},
            {"id": "sku-002", "name": "Pen", "price_pence": 150}]


class ShopHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = self.path.split("?", 1)[0]
        if route == "/health":
            broken = os.environ.get("SIMULATE_FAILURE") == "1"
            self.respond(500 if broken else 200,
                         {"status": "unhealthy" if broken else "healthy"})
        elif route == "/version":
            self.respond(200, {"version": os.environ.get("APP_VERSION", "unversioned"),
                               "environment": os.environ.get("ENVIRONMENT", "local")})
        elif route == "/products":
            self.respond(200, {"products": PRODUCTS})
        else:
            self.respond(404, {"error": "not_found"})

    def respond(self, code, payload):
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}", flush=True)


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), ShopHandler)
    print(f"Shop API listening on port {port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
