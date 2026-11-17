import { test } from "node:test";
import assert from "node:assert/strict";
import { infrarabbitCheapest } from "./infrarabbit-tool.mjs";

test("tool executes against the client", async () => {
  const fake = { cheapest: async (a) => ({ skus: [{ sku_id: "vps/x/y", name: "Y", price: 1, extra: 1, a }] }) };
  const t = infrarabbitCheapest(fake);
  const out = await t.execute({ category: "vps", limit: 1 }, { toolCallId: "1", messages: [] });
  assert.equal(out.skus[0].sku_id, "vps/x/y");
  assert.ok(!("extra" in out.skus[0]));
  assert.ok(t.inputSchema);
});
