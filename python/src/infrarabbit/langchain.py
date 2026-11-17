"""LangChain tools. Install with: pip install "infrarabbit[langchain]"."""
from __future__ import annotations

import json
from typing import Optional

from langchain_core.tools import tool

from .client import Client

_client = Client(user_agent=None)


@tool
def infrarabbit_cheapest(category: str = "vps", vcpu: Optional[float] = None, ram_gb: Optional[float] = None,
                         region: Optional[str] = None, gpu: Optional[str] = None, limit: int = 5) -> str:
    """Cheapest current list prices from InfraRabbit. category: vps, gpu, llm. Optional vcpu, ram_gb, region (e.g. eu), gpu (e.g. H100). Returns JSON with source and date per price."""
    r = _client.cheapest(category, vcpu=vcpu, ram_gb=ram_gb, region=region, gpu=gpu, limit=limit)
    keep = ("sku_id", "name", "provider", "price", "currency", "unit", "verified_at", "source_url")
    return json.dumps({"skus": [{k: s.get(k) for k in keep} for s in r.get("skus", [])], "cite": r.get("cite"),
                       "attribution": "Data: InfraRabbit, infrarabbit.com"})


@tool
def infrarabbit_search(q: str, limit: int = 5) -> str:
    """Search InfraRabbit SKUs (VPS plans, GPU instances, LLM models) by text, e.g. 'h100' or 'llama 3.3'."""
    r = _client.search_skus(q, limit=limit)
    keep = ("sku_id", "name", "provider", "price", "currency", "unit", "verified_at")
    return json.dumps({"skus": [{k: s.get(k) for k in keep} for s in r.get("skus", [])],
                       "attribution": "Data: InfraRabbit, infrarabbit.com"})


tools = [infrarabbit_cheapest, infrarabbit_search]
