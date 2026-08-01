export type ApiModel = {
  id: string;
  provider: string;
  name: string;
  version: string;
  avg_score: number;
  hallucination_rate: number;
  avg_latency_ms: number;
  avg_cost_usd: number;
  pass_rate: number;
  token_usage: number;
};

export type ApiPrompt = {
  id: string;
  title: string;
  category: string;
  difficulty: string;
  tags: string[];
  prompt_text: string;
  expected_answer?: string | null;
  dataset_source?: string | null;
  version: string;
};

export type ApiRun = {
  id: string;
  model: string;
  provider: string;
  prompt_version: string;
  dataset_version: string;
  temperature: number;
  seed?: number | null;
  status: string;
  average_score?: number | null;
  cost_usd?: number | null;
  latency_ms?: number | null;
  failure_category?: string | null;
  created_at: string;
};

export type ApiDataset = {
  id: string;
  name: string;
  version: string;
  source?: string | null;
  description?: string | null;
  prompt_count: number;
  tags: string[];
};

export type ApiMetricSummary = {
  model_count: number;
  run_count: number;
  average_score: number;
  average_latency_ms: number;
  average_cost_usd: number;
  hallucination_rate: number;
  pass_rate: number;
  failure_distribution: Record<string, number>;
};

type ApiListResponse<T> = {
  items: T[];
};

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1';

async function requestJson<T>(path: string): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchModels() {
  return requestJson<ApiListResponse<ApiModel>>('/models/');
}

export async function fetchPrompts() {
  return requestJson<ApiListResponse<ApiPrompt>>('/prompts/');
}

export async function fetchRuns() {
  return requestJson<ApiListResponse<ApiRun>>('/runs/');
}

export async function fetchDatasets() {
  return requestJson<ApiListResponse<ApiDataset>>('/datasets/');
}

export async function fetchMetrics() {
  return requestJson<ApiMetricSummary>('/metrics/');
}
