import type { DashboardFilterState } from '../types';

type FilterBarProps = {
  filters: DashboardFilterState;
  providers: string[];
  onChange: (next: DashboardFilterState) => void;
};

export function FilterBar({ filters, providers, onChange }: FilterBarProps) {
  return (
    <div className="filter-bar">
      <label>
        <span>Provider</span>
        <select value={filters.provider} onChange={(event) => onChange({ ...filters, provider: event.target.value })}>
          <option value="All">All</option>
          {providers.map((provider) => (
            <option key={provider} value={provider}>
              {provider}
            </option>
          ))}
        </select>
      </label>
      <label>
        <span>Prompt search</span>
        <input
          value={filters.search}
          onChange={(event) => onChange({ ...filters, search: event.target.value })}
          placeholder="Search failure cases, prompts, or models"
        />
      </label>
    </div>
  );
}
