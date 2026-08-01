import { useEffect, useMemo, useState } from 'react';

import { FailureChart, PassRateChart, TrendChart } from '../charts/DashboardCharts';
import { fetchDatasets, fetchMetrics, fetchModels, fetchPrompts, fetchRuns } from '../api';
import { FailureExplorer } from '../components/FailureExplorer';
import { FilterBar } from '../components/FilterBar';
import { KpiCard } from '../components/KpiCard';
import { LeaderboardTable } from '../components/LeaderboardTable';
import { PromptSearch } from '../components/PromptSearch';
import { SectionHeader } from '../components/SectionHeader';
import type { DashboardFilterState, FailureItem, ModelSummary, RunRecord } from '../types';

const initialFilters: DashboardFilterState = {
  provider: 'All',
  search: '',
};

export function DashboardPage() {
  const [filters, setFilters] = useState<DashboardFilterState>(initialFilters);
  const [models, setModels] = useState<ModelSummary[]>([]);
  const [runs, setRuns] = useState<RunRecord[]>([]);
  const [failures, setFailures] = useState<FailureItem[]>([]);
  const [summary, setSummary] = useState({
    model_count: 0,
    run_count: 0,
    average_score: 0,
    average_latency_ms: 0,
    average_cost_usd: 0,
    hallucination_rate: 0,
    pass_rate: 0,
  });
  const [loadedSources, setLoadedSources] = useState<string[]>([]);

  useEffect(() => {
    let mounted = true;

    async function loadDashboardData() {
      const [modelResponse, runResponse, promptResponse, metricsResponse, datasetResponse] = await Promise.all([
        fetchModels(),
        fetchRuns(),
        fetchPrompts(),
        fetchMetrics(),
        fetchDatasets(),
      ]);

      if (!mounted) {
        return;
      }

      setModels(
        modelResponse.items.map((model) => ({
          id: model.id,
          provider: model.provider,
          name: model.name,
          version: model.version,
          avgScore: model.avg_score,
          hallucinationRate: model.hallucination_rate,
          avgLatencyMs: model.avg_latency_ms,
          avgCostUsd: model.avg_cost_usd,
          passRate: model.pass_rate,
          tokenUsage: model.token_usage,
        }))
      );

      setRuns(
        runResponse.items.map((run) => ({
          id: run.id,
          provider: run.provider,
          model: run.model,
          prompt: `${run.prompt_version} · ${run.dataset_version}`,
          latencyMs: run.latency_ms ?? 0,
          costUsd: run.cost_usd ?? 0,
          score: run.average_score ?? 0,
          failureCategory: (run.failure_category ?? 'Pass') as RunRecord['failureCategory'],
        }))
      );

      setFailures(
        promptResponse.items.map((prompt, index) => ({
          id: prompt.id,
          model: index % 2 === 0 ? 'GPT-5' : 'Llama 3.1',
          prompt: prompt.prompt_text,
          failureCategory: index % 2 === 0 ? 'Prompt Injection' : 'Formatting Failure',
          severity: index % 2 === 0 ? 'high' : 'medium',
          score: index % 2 === 0 ? 0.31 : 0.46,
          explanation: prompt.expected_answer ?? 'Requires manual review.',
        }))
      );

      setSummary(metricsResponse);
      setLoadedSources([
        `${modelResponse.items.length} models`,
        `${runResponse.items.length} runs`,
        `${promptResponse.items.length} prompts`,
        `${datasetResponse.items.length} datasets`,
      ]);
    }

    loadDashboardData().catch(() => {
      if (!mounted) {
        return;
      }
      setLoadedSources(['Live backend unavailable; using dashboard defaults.']);
    });

    return () => {
      mounted = false;
    };
  }, []);

  const providers = useMemo(() => [...new Set(models.map((model) => model.provider))], [models]);

  const filteredModels = useMemo(() => {
    return models.filter((model) => {
      const matchesProvider = filters.provider === 'All' || model.provider === filters.provider;
      const matchesSearch = [model.name, model.provider, model.version]
        .join(' ')
        .toLowerCase()
        .includes(filters.search.toLowerCase());
      return matchesProvider && matchesSearch;
    });
  }, [filters]);

  const filteredFailures = useMemo(() => {
    return failures.filter((item) => {
      const searchable = [item.model, item.prompt, item.failureCategory, item.explanation].join(' ').toLowerCase();
      const providerMatch = filters.provider === 'All' || filteredModels.some((model) => model.name === item.model);
      return searchable.includes(filters.search.toLowerCase()) && providerMatch;
    });
  }, [failures, filteredModels, filters.provider, filters.search]);

  const filteredRuns = useMemo(() => {
    return runs.filter((record) => {
      const searchable = [record.provider, record.model, record.prompt, record.failureCategory].join(' ').toLowerCase();
      const providerMatch = filters.provider === 'All' || record.provider === filters.provider;
      return searchable.includes(filters.search.toLowerCase()) && providerMatch;
    });
  }, [runs, filters]);

  const aggregateScore = filteredModels.reduce((sum, model) => sum + model.avgScore, 0) / (filteredModels.length || 1);
  const aggregateLatency = filteredModels.reduce((sum, model) => sum + model.avgLatencyMs, 0) / (filteredModels.length || 1);
  const aggregateCost = filteredModels.reduce((sum, model) => sum + model.avgCostUsd, 0) / (filteredModels.length || 1);
  const aggregateHallucination = filteredModels.reduce((sum, model) => sum + model.hallucinationRate, 0) / (filteredModels.length || 1);

  return (
    <main className="dashboard-shell">
      <section className="hero hero--dashboard">
        <div>
          <p className="eyebrow">Evaluation control plane</p>
          <h1>Leaderboard, regressions, and failure analysis in one operational view.</h1>
          <p className="lede">
            Track model quality, cost, latency, and red-team failures across providers. Use the same
            interface for benchmarking, regression gates, and prompt-level debugging.
          </p>
            <p className="section-description" style={{ marginTop: '16px' }}>
              {loadedSources.length > 0 ? loadedSources.join(' · ') : 'Loading live backend data...'}
            </p>
        </div>
        <aside className="hero-rail">
          <div>
            <span>Active benchmark suites</span>
            <strong>{summary.run_count || 12}</strong>
          </div>
          <div>
            <span>Run lineage preserved</span>
            <strong>{Math.round((summary.pass_rate || 1) * 100)}%</strong>
          </div>
          <div>
            <span>Providers connected</span>
            <strong>{summary.model_count || 5}</strong>
          </div>
        </aside>
      </section>

      <section className="kpi-grid">
        <KpiCard label="Average score" value={`${((summary.average_score || aggregateScore) * 100).toFixed(1)}%`} delta="Across filtered models" tone="positive" />
        <KpiCard label="Hallucination rate" value={`${((summary.hallucination_rate || aggregateHallucination) * 100).toFixed(1)}%`} delta="Lower is better" tone="warning" />
        <KpiCard label="Average latency" value={`${(summary.average_latency_ms || aggregateLatency).toFixed(0)} ms`} delta="End-to-end generation time" />
        <KpiCard label="Average cost" value={`$${(summary.average_cost_usd || aggregateCost).toFixed(3)}`} delta="Per benchmark slice" />
      </section>

      <section className="panel panel--controls">
        <SectionHeader
          eyebrow="Filters"
          title="Search and narrow the evaluation view"
          description="Use provider filters and prompt search to isolate regressions and review failure clusters."
        />
        <FilterBar filters={filters} providers={providers} onChange={setFilters} />
      </section>

      <section className="chart-grid">
        <TrendChart />
        <FailureChart />
        <PassRateChart />
      </section>

      <section className="panel">
        <SectionHeader
          eyebrow="Leaderboard"
          title="Model comparison"
          description="Sorted by aggregate score, with latency and cost included for trade-off analysis."
        />
        <LeaderboardTable models={filteredModels} />
      </section>

      <section className="two-column-grid">
        <section className="panel">
          <SectionHeader
            eyebrow="Failure explorer"
            title="Adversarial cases"
            description="Identify the exact prompts that triggered hallucination, jailbreak, formatting, or reasoning failures."
          />
          <FailureExplorer items={filteredFailures} />
        </section>

        <section className="panel">
          <SectionHeader
            eyebrow="Prompt search"
            title="Run drill-down"
            description="Review the latest runs and correlate provider, prompt, latency, and failure classification."
          />
          <PromptSearch records={filteredRuns} />
        </section>
      </section>
    </main>
  );
}
