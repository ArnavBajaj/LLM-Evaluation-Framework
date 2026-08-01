type KpiCardProps = {
  label: string;
  value: string;
  delta?: string;
  tone?: 'positive' | 'neutral' | 'warning';
};

export function KpiCard({ label, value, delta, tone = 'neutral' }: KpiCardProps) {
  return (
    <article className={`kpi-card kpi-card--${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      {delta ? <small>{delta}</small> : null}
    </article>
  );
}
