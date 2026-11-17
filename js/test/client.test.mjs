import { test } from "node:test";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { readFileSync } from "node:fs";
import { Client, InfraRabbitError } from "../dist/esm/index.js";

const require = createRequire(import.meta.url);
const cjs = require("../dist/cjs/index.js");
const fixture = readFileSync(new URL("../../python/tests/fixtures/cheapest.json", import.meta.url), "utf8");

function fake(status = 200, body = fixture) {
  const calls = [];
  const fetch = async (url, init) => { calls.push({ url, init }); return new Response(body, { status }); };
  return { calls, fetch };
}

test("cheapest builds query and UA", async () => {
  const { calls, fetch } = fake();
  const r = await new Client({ fetch }).cheapest({ ram_gb: 4, region: "eu", limit: 1 });
  assert.ok(r.skus[0].sku_id.startsWith("vps/"));
  assert.equal(calls[0].url, "https://infrarabbit.com/v1/cheapest?category=vps&ram_gb=4&region=eu&limit=1");
  assert.match(calls[0].init.headers["User-Agent"], /^infrarabbit-js\//);
});

test("history keeps slashes in sku id", async () => {
  const { calls, fetch } = fake();
  await new Client({ fetch }).history("gpu/datacrunch/x.y", { days: 30 });
  assert.equal(calls[0].url, "https://infrarabbit.com/v1/skus/gpu/datacrunch/x.y/history?days=30");
});

test("errors", async () => {
  const { fetch } = fake(404, "unknown sku");
  await assert.rejects(new Client({ fetch }).sku("nope"), (e) => e instanceof InfraRabbitError && e.status === 404);
});

test("CJS build works", () => { assert.equal(typeof cjs.Client, "function"); });

test("live", { skip: !process.env.INFRARABBIT_LIVE }, async () => {
  const r = await new Client().cheapest({ category: "vps", limit: 1 });
  assert.ok(r.skus[0].price > 0);
});
