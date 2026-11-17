"""Stdlib-only client (urllib). AsyncClient runs the same calls in a worker thread."""
from __future__ import annotations

import asyncio
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

__version__ = "0.1.0"
BASE_URL = "https://infrarabbit.com"

JSON = Dict[str, Any]


class InfraRabbitError(Exception):
    def __init__(self, status: int, message: str, url: str = ""):
        super().__init__(f"HTTP {status} for {url}: {message}")
        self.status = status
        self.url = url


def _clean(params: Dict[str, Any]) -> Dict[str, str]:
    out = {}
    for k, v in params.items():
        if v is None:
            continue
        out[k.rstrip("_")] = ("true" if v else "false") if isinstance(v, bool) else str(v)
    return out


class Client:
    """Sync client. Methods return the API's JSON as dicts."""

    def __init__(self, base_url: str = BASE_URL, timeout: float = 30.0, user_agent: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = user_agent or f"infrarabbit-python/{__version__}"

    def _get(self, path: str, **params: Any) -> JSON:
        q = urllib.parse.urlencode(_clean(params))
        url = f"{self.base_url}{path}" + (f"?{q}" if q else "")
        req = urllib.request.Request(url, headers={"User-Agent": self.user_agent, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise InfraRabbitError(e.code, e.read().decode("utf-8", "replace")[:300], url) from None

    def cheapest(self, category: str = "vps", *, vcpu: Optional[float] = None, ram_gb: Optional[float] = None,
                 disk_gb: Optional[float] = None, gpu: Optional[str] = None, gpu_count: Optional[int] = None,
                 region: Optional[str] = None, provider: Optional[str] = None, currency: str = "USD",
                 limit: int = 10, exact: bool = False) -> JSON:
        """Cheapest current plans. Result: {"skus": [...], "cite": {...}, ...}."""
        return self._get("/v1/cheapest", category=category, vcpu=vcpu, ram_gb=ram_gb, disk_gb=disk_gb, gpu=gpu,
                         gpu_count=gpu_count, region=region, provider=provider, currency=currency, limit=limit,
                         exact=exact or None)

    def search_skus(self, q: Optional[str] = None, *, category: Optional[str] = None, provider: Optional[str] = None,
                    limit: int = 100, offset: int = 0) -> JSON:
        return self._get("/v1/skus", q=q, category=category, provider=provider, limit=limit, offset=offset)

    def sku(self, sku_id: str) -> JSON:
        return self._get(f"/v1/skus/{urllib.parse.quote(sku_id, safe='/')}")

    def history(self, sku_id: str, *, days: Optional[int] = None, from_: Optional[str] = None,
                to: Optional[str] = None) -> JSON:
        return self._get(f"/v1/skus/{urllib.parse.quote(sku_id, safe='/')}/history", days=days, from_=from_, to=to)

    def changes(self, *, since: Optional[str] = None, category: Optional[str] = None, provider: Optional[str] = None,
                kind: Optional[str] = None, sku_id: Optional[str] = None, limit: int = 200) -> JSON:
        return self._get("/v1/changes", since=since, category=category, provider=provider, kind=kind,
                         sku_id=sku_id, limit=limit)

    def since(self, date: str, *, kind: Optional[str] = None, provider: Optional[str] = None,
              limit: Optional[int] = None) -> JSON:
        """Grouped answer to 'what changed since <date>' (YYYY-MM-DD)."""
        return self._get("/v1/since", date=date, kind=kind, provider=provider, limit=limit)

    def vps_plans(self, *, ram: Optional[float] = None, vcpu: Optional[float] = None, region: Optional[str] = None,
                  limit: Optional[int] = None) -> JSON:
        return self._get("/v1/vps/plans", ram=ram, vcpu=vcpu, region=region, limit=limit)

    def index(self, series: Optional[str] = None, *, days: Optional[int] = None) -> JSON:
        return self._get(f"/v1/index/{series}" if series else "/v1/index", days=days)

    def providers(self, category: Optional[str] = None) -> JSON:
        return self._get("/v1/providers", category=category)

    def status(self) -> JSON:
        return self._get("/v1/status")


class AsyncClient:
    """Async twin of Client (same methods, awaitable)."""

    def __init__(self, *args: Any, **kwargs: Any):
        self._c = Client(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        fn = getattr(self._c, name)
        if name.startswith("_") or not callable(fn):
            return fn

        async def call(*a: Any, **kw: Any) -> JSON:
            return await asyncio.to_thread(fn, *a, **kw)

        return call
