import type { FailureItem } from '../types';

type FailureExplorerProps = {
  items: FailureItem[];
};

export function FailureExplorer({ items }: FailureExplorerProps) {
  return (
    <div className="failure-explorer">
      {items.map((item) => (
        <article className="failure-card" key={item.id}>
          <div className="failure-card__topline">
            <strong>{item.failureCategory}</strong>
            <span className={`severity severity--${item.severity}`}>{item.severity}</span>
          </div>
          <h3>{item.model}</h3>
          <p className="failure-prompt">{item.prompt}</p>
          <p>{item.explanation}</p>
          <footer>
            <span>Score {item.score.toFixed(2)}</span>
          </footer>
        </article>
      ))}
    </div>
  );
}
