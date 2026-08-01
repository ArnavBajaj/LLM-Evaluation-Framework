import type { RunRecord } from '../types';

type PromptSearchProps = {
  records: RunRecord[];
};

export function PromptSearch({ records }: PromptSearchProps) {
  return (
    <div className="search-panel">
      <div className="search-panel__header">
        <h3>Prompt search</h3>
        <span>{records.length} matching runs</span>
      </div>
      <div className="search-list">
        {records.map((record) => (
          <article key={record.id} className="search-list__item">
            <div>
              <strong>{record.prompt}</strong>
              <p>
                {record.provider} · {record.model} · {record.failureCategory}
              </p>
            </div>
            <span>{record.latencyMs} ms</span>
          </article>
        ))}
      </div>
    </div>
  );
}
