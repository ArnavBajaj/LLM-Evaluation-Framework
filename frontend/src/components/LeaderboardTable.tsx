import type { ModelSummary } from '../types';

type LeaderboardTableProps = {
  models: ModelSummary[];
};

export function LeaderboardTable({ models }: LeaderboardTableProps) {
  return (
    <div className="table-shell">
      <table className="leaderboard-table">
        <thead>
          <tr>
            <th>Model</th>
            <th>Avg score</th>
            <th>Hallucination</th>
            <th>Latency</th>
            <th>Cost</th>
            <th>Pass rate</th>
          </tr>
        </thead>
        <tbody>
          {models.map((model) => (
            <tr key={model.id}>
              <td>
                <div className="table-model">
                  <strong>{model.name}</strong>
                  <span>{model.provider} · {model.version}</span>
                </div>
              </td>
              <td>{(model.avgScore * 100).toFixed(1)}%</td>
              <td>{(model.hallucinationRate * 100).toFixed(1)}%</td>
              <td>{model.avgLatencyMs} ms</td>
              <td>${model.avgCostUsd.toFixed(3)}</td>
              <td>{(model.passRate * 100).toFixed(1)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
