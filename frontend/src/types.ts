export type ModelSummary = {
  id: string;
  provider: string;
  name: string;
  version: string;
  avgScore: number;
  hallucinationRate: number;
  avgLatencyMs: number;
  avgCostUsd: number;
  passRate: number;
  tokenUsage: number;
};

export type FailureCategory =
  | 'Hallucination'
  | 'Unsafe Advice'
  | 'Prompt Injection'
  | 'Jailbreak'
  | 'Logical Error'
  | 'Reasoning Failure'
  | 'Formatting Failure'
  | 'Toxic Output'
  | 'Bias'
  | 'Refusal Failure';

export type FailureItem = {
  id: string;
  model: string;
  prompt: string;
  failureCategory: FailureCategory;
  severity: 'low' | 'medium' | 'high';
  score: number;
  explanation: string;
};

export type RunRecord = {
  id: string;
  provider: string;
  model: string;
  prompt: string;
  latencyMs: number;
  costUsd: number;
  score: number;
  failureCategory: FailureCategory | 'Pass';
};

export type DashboardFilterState = {
  provider: string;
  search: string;
};

export type DashboardMetrics = {
  model_count: number;
  run_count: number;
  average_score: number;
  average_latency_ms: number;
  average_cost_usd: number;
  hallucination_rate: number;
  pass_rate: number;
};
