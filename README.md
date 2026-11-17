# InfraRabbit SDK

[![CI](https://github.com/InfraRabbit/sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/InfraRabbit/sdk/actions/workflows/ci.yml)

Client packages for the public, read-only InfraRabbit price API (https://infrarabbit.com, no key needed). InfraRabbit archives published compute prices (GPU hours, VPS plans, LLM tokens) daily, with history and price indices.

- [`python/`](python): `infrarabbit` for Python (stdlib only, sync + async)
- [`js/`](js): `infrarabbit` for JavaScript/TypeScript (zero deps, ESM + CJS, types)
- [`integrations/`](integrations): LangChain tool (Python extra `infrarabbit[langchain]`) and a Vercel AI SDK tool example

<!-- REMOVE-WHEN-PUBLISHED -->
> Not yet on PyPI/npm: install from source until published.
> `pip install "git+https://github.com/InfraRabbit/sdk.git#subdirectory=python"`
> JS: clone the repo, then `cd js && npm install && npm run build`.
<!-- /REMOVE-WHEN-PUBLISHED -->

Links: [API docs](https://infrarabbit.com/api) · [MCP server](https://infrarabbit.com/mcp) · [llms.txt](https://infrarabbit.com/llms.txt) · [Dataset](https://huggingface.co/datasets/InfraRabbit/compute-prices)

Data: InfraRabbit, infrarabbit.com. Data terms: https://infrarabbit.com/licensing. The MIT licence here covers the code only.
