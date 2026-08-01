import { ArcElement, CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Tooltip } from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';

import { failureDistribution, telemetrySeries } from '../data/mockDashboard';

ChartJS.register(ArcElement, CategoryScale, Legend, LinearScale, LineElement, PointElement, Tooltip);

const lineData = {
  labels: telemetrySeries.map((entry) => entry.label),
  datasets: [
    {
      label: 'Average score',
      data: telemetrySeries.map((entry) => entry.score * 100),
      borderColor: '#61dafb',
      backgroundColor: 'rgba(97, 218, 251, 0.2)',
      tension: 0.35,
      fill: true,
    },
    {
      label: 'Latency ms',
      data: telemetrySeries.map((entry) => entry.latency),
      borderColor: '#7c8dff',
      backgroundColor: 'rgba(124, 141, 255, 0.18)',
      tension: 0.35,
    },
  ],
};

const pieData = {
  labels: failureDistribution.map((entry) => entry.label),
  datasets: [
    {
      label: 'Failure count',
      data: failureDistribution.map((entry) => entry.value),
      backgroundColor: ['#61dafb', '#7c8dff', '#ff8b7a', '#ffbf69', '#a3d977', '#d88cff'],
      borderWidth: 0,
    },
  ],
};

const barData = {
  labels: ['GPT-5', 'Claude', 'Gemini', 'Mistral', 'Llama'],
  datasets: [
    {
      label: 'Pass rate',
      data: [91, 89, 84, 81, 74],
      backgroundColor: ['#61dafb', '#7c8dff', '#a3d977', '#ffbf69', '#ff8b7a'],
    },
  ],
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: '#eff4ff' } },
  },
  scales: {
    x: {
      ticks: { color: '#9fb0d0' },
      grid: { color: 'rgba(159, 176, 208, 0.12)' },
    },
    y: {
      ticks: { color: '#9fb0d0' },
      grid: { color: 'rgba(159, 176, 208, 0.12)' },
    },
  },
};

export function TrendChart() {
  return (
    <section className="chart-card">
      <header>
        <h3>Quality and latency trend</h3>
        <p>Seven-day aggregated view across the latest regression suite.</p>
      </header>
      <div className="chart-stage chart-stage--tall">
        <Line data={lineData} options={chartOptions} />
      </div>
    </section>
  );
}

export function FailureChart() {
  return (
    <section className="chart-card">
      <header>
        <h3>Failure distribution</h3>
        <p>Normalized category counts from the latest adversarial suite.</p>
      </header>
      <div className="chart-stage">
        <Pie data={pieData} options={{ responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: '#eff4ff' } } } }} />
      </div>
    </section>
  );
}

export function PassRateChart() {
  return (
    <section className="chart-card">
      <header>
        <h3>Model comparison</h3>
        <p>Pass rate across providers for the same benchmark slice.</p>
      </header>
      <div className="chart-stage">
        <Bar data={barData} options={chartOptions} />
      </div>
    </section>
  );
}
