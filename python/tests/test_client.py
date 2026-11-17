import asyncio
import json
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest

from infrarabbit import AsyncClient, Client, InfraRabbitError

FIX = Path(__file__).parent / "fixtures"
SEEN = []


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        SEEN.append((self.path, self.headers["User-Agent"]))
        if self.path.startswith("/v1/skus/nope"):
            self.send_response(404); self.end_headers(); self.wfile.write(b'{"detail":"unknown sku"}'); return
        name = "cheapest.json" if self.path.startswith("/v1/cheapest") else "skus.json"
        body = (FIX / name).read_bytes()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)

    def log_message(self, *a):
        pass


@pytest.fixture(scope="module")
def base():
    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_port}"
    srv.shutdown()


def test_cheapest_params_and_ua(base):
    r = Client(base).cheapest("vps", ram_gb=4, region="eu", limit=1)
    assert r["skus"][0]["sku_id"].startswith("vps/")
    path, ua = SEEN[-1]
    assert "category=vps" in path and "ram_gb=4" in path and "region=eu" in path and "vcpu" not in path
    assert ua.startswith("infrarabbit-python/")


def test_search_and_sku_path(base):
    assert Client(base).search_skus("h100", limit=1)["count"] == 1
    Client(base).history("gpu/datacrunch/x.y", days=30)
    assert SEEN[-1][0] == "/v1/skus/gpu/datacrunch/x.y/history?days=30"


def test_error(base):
    with pytest.raises(InfraRabbitError) as e:
        Client(base).sku("nope")
    assert e.value.status == 404


def test_async(base):
    r = asyncio.run(AsyncClient(base).cheapest("vps", limit=1))
    assert r["skus"]


@pytest.mark.live
@pytest.mark.skipif(not os.environ.get("INFRARABBIT_LIVE"), reason="set INFRARABBIT_LIVE=1")
def test_live():
    r = Client().cheapest("vps", limit=1)
    assert r["skus"][0]["price"] > 0
