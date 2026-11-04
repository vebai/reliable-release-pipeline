"""Runtime observation: check HTTP endpoints and source revision, fail closed."""
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def get_json(base, path):
    with urlopen(base + path, timeout=2) as response:
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("application/json"):
            raise ValueError(f"{path}: expected JSON content type")
        return response.status, json.load(response)


def verify(base, revision, environment):
    last_error = None
    for _ in range(20):
        try:
            health_code, health = get_json(base, "/health")
            if health_code != 200 or health.get("status") != "healthy":
                raise ValueError("health check not healthy")
            version_code, version = get_json(base, "/version")
            if version_code != 200 or version.get("version") != revision:
                raise ValueError(f"version mismatch: expected {revision}, got {version!r}")
            if version.get("environment") != environment:
                raise ValueError(f"environment mismatch: expected {environment}, got {version!r}")
            products_code, products = get_json(base, "/products")
            if products_code != 200 or not isinstance(products.get("products"), list):
                raise ValueError("products contract failure")
            print(f"PASS: /health 200; /version {revision}; /products 200; environment {environment}")
            return
        except (URLError, HTTPError, ValueError, OSError, json.JSONDecodeError) as err:
            last_error = err
            time.sleep(0.5)
    raise RuntimeError(f"FAIL: deployment verification failed after retries: {last_error}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("Usage: verify_http.py BASE_URL EXPECTED_REVISION EXPECTED_ENVIRONMENT")
    try:
        verify(*sys.argv[1:])
    except Exception as ex:
        print(str(ex), file=sys.stderr)
        sys.exit(1)
