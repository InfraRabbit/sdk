/** Client for the InfraRabbit price API. Data: InfraRabbit, infrarabbit.com. */
export const VERSION = "0.1.0";
export const BASE_URL = "https://infrarabbit.com";

export interface Sku {
  sku_id: string;
  category: string;
  provider: string;
  name: string;
  price: number | null;
  currency: string;
  unit: string;
  price_usd?: number | null;
  price_eur?: number | null;
  verified_at?: string;
  source_url?: string;
  cite?: { text: string; url: string };
  [key: string]: unknown;
}
export interface SkuList { skus: Sku[]; count?: number; cite?: { text: string; url?: string }; [key: string]: unknown }
export type Json = Record<string, unknown>;

export interface CheapestParams {
  category?: string; vcpu?: number; ram_gb?: number; disk_gb?: number; gpu?: string; gpu_count?: number;
  region?: string; provider?: string; currency?: string; limit?: number; exact?: boolean;
}

export class InfraRabbitError extends Error {
  constructor(public status: number, message: string, public url: string) {
    super(`HTTP ${status} for ${url}: ${message}`);
  }
}

export interface ClientOptions { baseUrl?: string; userAgent?: string; fetch?: typeof fetch }

export class Client {
  private baseUrl: string;
  private ua: string;
  private f: typeof fetch;
  constructor(opts: ClientOptions = {}) {
    this.baseUrl = (opts.baseUrl ?? BASE_URL).replace(/\/+$/, "");
    this.ua = opts.userAgent ?? `infrarabbit-js/${VERSION}`;
    this.f = opts.fetch ?? ((...a) => fetch(...a));
  }

  private async get<T>(path: string, params: Record<string, unknown> = {}): Promise<T> {
    const q = new URLSearchParams();
    for (const [k, v] of Object.entries(params)) if (v !== undefined && v !== null && v !== false) q.set(k, String(v));
    const url = this.baseUrl + path + (q.size ? `?${q}` : "");
    // User-Agent is ignored by browsers (forbidden header) and honoured by Node/Deno/Bun.
    const r = await this.f(url, { headers: { Accept: "application/json", "User-Agent": this.ua } });
    if (!r.ok) throw new InfraRabbitError(r.status, (await r.text()).slice(0, 300), url);
    return (await r.json()) as T;
  }

  cheapest(p: CheapestParams = {}): Promise<SkuList> { return this.get("/v1/cheapest", { category: "vps", ...p }); }
  searchSkus(p: { q?: string; category?: string; provider?: string; limit?: number; offset?: number } = {}): Promise<SkuList> {
    return this.get("/v1/skus", p);
  }
  sku(id: string): Promise<Sku> { return this.get(`/v1/skus/${id.split("/").map(encodeURIComponent).join("/")}`); }
  history(id: string, p: { days?: number; from?: string; to?: string } = {}): Promise<Json> {
    return this.get(`/v1/skus/${id.split("/").map(encodeURIComponent).join("/")}/history`, p);
  }
  changes(p: { since?: string; category?: string; provider?: string; kind?: string; sku_id?: string; limit?: number } = {}): Promise<Json> {
    return this.get("/v1/changes", p);
  }
  since(date: string, p: { kind?: string; provider?: string; limit?: number } = {}): Promise<Json> {
    return this.get("/v1/since", { date, ...p });
  }
  vpsPlans(p: { ram?: number; vcpu?: number; region?: string; limit?: number } = {}): Promise<Json> { return this.get("/v1/vps/plans", p); }
  index(series?: string, p: { days?: number } = {}): Promise<Json> { return this.get(series ? `/v1/index/${series}` : "/v1/index", p); }
  providers(category?: string): Promise<Json> { return this.get("/v1/providers", { category }); }
  status(): Promise<Json> { return this.get("/v1/status"); }
}
