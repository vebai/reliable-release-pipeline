import json
import os
import threading
import unittest
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen
from shop_api import ShopHandler


class ShopAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), ShopHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=2)

    def fetch(self, path):
        try:
            with urlopen(self.base + path, timeout=3) as resp:
                return resp.status, json.load(resp)
        except HTTPError as err:
            return err.code, json.loads(err.read())

    def test_health_passes_by_default(self):
        with patch.dict(os.environ, {"SIMULATE_FAILURE": "0"}):
            status, data = self.fetch("/health")
        self.assertEqual((status, data["status"]), (200, "healthy"))

    def test_version_identifies_build(self):
        with patch.dict(os.environ, {"APP_VERSION": "abc1234", "ENVIRONMENT": "staging"}):
            status, data = self.fetch("/version")
        self.assertEqual(status, 200)
        self.assertEqual(data, {"version": "abc1234", "environment": "staging"})

    def test_products_contract(self):
        status, data = self.fetch("/products")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(data["products"]), 1)
        self.assertTrue(all("id" in p and "price_pence" in p for p in data["products"]))

    def test_missing_route(self):
        status, _ = self.fetch("/not-there")
        self.assertEqual(status, 404)

    def test_controlled_failure_is_detectable(self):
        with patch.dict(os.environ, {"SIMULATE_FAILURE": "1"}):
            status, data = self.fetch("/health")
        self.assertEqual((status, data["status"]), (500, "unhealthy"))


if __name__ == "__main__":
    unittest.main()
