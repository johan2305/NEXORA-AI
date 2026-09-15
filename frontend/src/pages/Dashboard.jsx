import { useEffect, useState } from 'react'
import { getAnalyticsSummary } from '../api/analytics'

function MetricCard({ label, value, sublabel }) {
  return (
    <div className="bg-bg-surface border border-border rounded-lg p-4">
      <p className="text-xs text-text-secondary uppercase tracking-wide">{label}</p>
      <p className="text-3xl font-semibold font-mono mt-2">{value}</p>
      {sublabel && <p className="text-xs text-text-secondary mt-1">{sublabel}</p>}
    </div>
  )
}

function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const data = await getAnalyticsSummary()
      setSummary(data)
      setLoading(false)
    }
    load()
  }, [])

  if (loading) {
    return <p className="text-text-secondary text-sm">Cargando métricas...</p>
  }

  const automatedTasks =
    (summary.tasks_by_created_by.automation || 0) + (summary.tasks_by_created_by.ai || 0)
  const humanTasks = summary.tasks_by_created_by.user || 0

  return (
    <div>
      <h1 className="text-2xl font-semibold mb-6">Dashboard</h1>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <MetricCard label="Tareas totales" value={summary.total_tasks} />
        <MetricCard label="Clientes" value={summary.total_customers} />
        <MetricCard label="Automatizaciones" value={summary.total_automations} />
        <MetricCard
          label="Horas ahorradas (est.)"
          value={summary.estimated_hours_saved}
          sublabel="por IA y automatizaciones"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div className="bg-bg-surface border border-border rounded-lg p-4">
          <p className="text-sm font-medium mb-3">Origen de las tareas</p>
          <div className="flex flex-col gap-2 text-sm">
            <div className="flex justify-between">
              <span className="text-text-secondary">Creadas por usuarios</span>
              <span className="font-mono">{humanTasks}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-secondary">Creadas por IA / Automatización</span>
              <span className="font-mono text-accent">{automatedTasks}</span>
            </div>
          </div>
        </div>

        <div className="bg-bg-surface border border-border rounded-lg p-4">
          <p className="text-sm font-medium mb-3">Ejecuciones de automatizaciones</p>
          <div className="flex flex-col gap-2 text-sm">
            <div className="flex justify-between">
              <span className="text-text-secondary">Exitosas</span>
              <span className="font-mono text-success">
                {summary.automation_executions_success}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-secondary">Fallidas</span>
              <span className="font-mono text-error">
                {summary.automation_executions_failed}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-bg-surface border border-border rounded-lg p-4">
        <p className="text-sm font-medium mb-3">Uso de IA</p>
        <div className="flex gap-8 text-sm">
          <div>
            <p className="text-text-secondary text-xs">Solicitudes totales</p>
            <p className="font-mono text-lg">{summary.ai_requests_total}</p>
          </div>
          <div>
            <p className="text-text-secondary text-xs">Latencia promedio</p>
            <p className="font-mono text-lg">
              {summary.ai_avg_latency_ms ? `${summary.ai_avg_latency_ms}ms` : '—'}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard