# infrarabbit (JavaScript / TypeScript)

Client for the public InfraRabbit price API: cheapest VPS, GPU and LLM prices, each with source and read date. No key, zero dependencies (uses `fetch`, Node 18+).

```js
// npm install infrarabbit
import { Client } from "infrarabbit";
const c = new Client();
const top = (await c.cheapest({ category: "vps", ram_gb: 4, region: "eu", limit: 1 })).skus[0];
console.log(top.name, top.price, top.currency, top.verified_at);
// also: searchSkus({q}), sku(id), history(id), changes(), since(date), vpsPlans(), index()
```

ESM and CJS (`require("infrarabbit")`) with types. User-Agent is `infrarabbit-js/<version>` (set by Node, ignored by browsers).
Vercel AI SDK tool: see `integrations/vercel-ai` in the repo. MCP server: https://infrarabbit.com/mcp.

Data: InfraRabbit, infrarabbit.com. Data terms: https://infrarabbit.com/data (the MIT licence covers this code only).
