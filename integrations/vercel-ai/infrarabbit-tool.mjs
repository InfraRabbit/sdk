// Vercel AI SDK tool: cheapest current prices from InfraRabbit. Data: InfraRabbit, infrarabbit.com
import { tool } from "ai";
import { z } from "zod";
import { Client } from "infrarabbit";

export function infrarabbitCheapest(client = new Client()) {
  return tool({
    description: "Cheapest current list prices (VPS, GPU, LLM) from InfraRabbit, each with source and read date.",
    inputSchema: z.object({
      category: z.enum(["vps", "gpu", "llm"]).default("vps"),
      vcpu: z.number().optional(),
      ram_gb: z.number().optional(),
      region: z.string().optional().describe("e.g. eu, us"),
      gpu: z.string().optional().describe("e.g. H100"),
      limit: z.number().int().min(1).max(10).default(5),
    }),
    execute: async (args) => {
      const r = await client.cheapest(args);
      return {
        skus: r.skus.map(({ sku_id, name, provider, price, currency, unit, verified_at, source_url }) =>
          ({ sku_id, name, provider, price, currency, unit, verified_at, source_url })),
        attribution: "Data: InfraRabbit, infrarabbit.com",
      };
    },
  });
}

// Usage: generateText({ model, tools: { infrarabbitCheapest: infrarabbitCheapest() }, prompt: "Cheapest 4 GB VPS in the EU?" })
