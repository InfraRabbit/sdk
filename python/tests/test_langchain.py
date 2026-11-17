import json

import pytest

pytest.importorskip("langchain_core")
from infrarabbit import langchain as lc  # noqa: E402


class Fake:
    def cheapest(self, *a, **k):
        return {"skus": [{"sku_id": "vps/x/y", "name": "Y", "price": 1.0, "extra": 1}], "cite": {"text": "c"}}


def test_tool(monkeypatch):
    monkeypatch.setattr(lc, "_client", Fake())
    out = json.loads(lc.infrarabbit_cheapest.invoke({"category": "vps", "limit": 1}))
    assert out["skus"][0]["sku_id"] == "vps/x/y" and "extra" not in out["skus"][0]
    assert "InfraRabbit" in out["attribution"]
