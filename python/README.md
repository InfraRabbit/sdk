# infrarabbit (Python)

Client for the public InfraRabbit price API: cheapest VPS, GPU and LLM prices, each with source and read date. No key.

```python
# pip install infrarabbit
from infrarabbit import Client
c = Client()
top = c.cheapest("vps", ram_gb=4, region="eu", limit=1)["skus"][0]
print(top["name"], top["price"], top["currency"], top["verified_at"])
print(c.search_skus("h100", limit=3)["count"], "H100 SKUs")  # also: sku(), history(), changes(), since(), vps_plans(), index()
```

Async: `from infrarabbit import AsyncClient`, then `await AsyncClient().cheapest("gpu", gpu="H100")`.
LangChain: `pip install "infrarabbit[langchain]"`, then `from infrarabbit.langchain import tools`.
User-Agent is `infrarabbit-python/<version>`. MCP server: https://infrarabbit.com/mcp.

Data: InfraRabbit, infrarabbit.com. Data terms: https://infrarabbit.com/data (the MIT licence covers this code only).
