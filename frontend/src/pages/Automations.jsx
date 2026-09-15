import { useEffect, useState } from 'react'
import {
  listAutomations,
  createAutomation,
  deleteAutomation,
  runAutomation,
  listExecutions,
} from '../api/automations'

function Automations() {
  const [automations, setAutomations] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [daysInactive, setDaysInactive] = useState(7)
  const [submitting, setSubmitting] = useState(false)

  const [expandedId, setExpandedId] = useState(null)
  const [executions, setExecutions] = useState([])
  const [runningId, setRunningId] = useState(null)

  async function loadAutomations() {
    setLoading(true)
    const data = await listAutomations()
    setAutomations(data)
    setLoading(false)
  }

  useEffect(() => {
    loadAutomations()
  }, [])

  async function handleCreate(e) {
    e.preventDefault()
    setSubmitting(true)
    await createAutomation({
      name,
      trigger_type: 'customer_inactive',
      trigger_config: { days_inactive: Number(daysInactive) },
      action_type: 'create_task',
      action_config: { title_template: 'Seguimiento con {customer_name}' },
    })
    setName('')
    setDaysInactive(7)
    setShowForm(false)
    setSubmitting(false)
    loadAutomations()
  }

  async function handleDelete(id) {
    await deleteAutomation(id)
    if (expandedId === id) setExpandedId(null)
    loadAutomations()
  }

  async function handleRun(id) {
    setRunningId(id)
    await runAutomation(id)
    setRunningId(null)
    if (expandedId === id) handleToggleExecutions(id)
  }

  async function handleToggleExecutions(id) {
    if (expandedId === id) {
      setExpandedId(null)
      return
    }
    const data = await listExecutions(id)
    setExecutions(data)
    setExpandedId(id)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Automatizaciones</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity"
        >
          {showForm ? 'Cancelar' : 'Nueva automatización'}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleCreate}
          className="bg-bg-surface border border-border rounded-lg p-4 mb-6 flex flex-col gap-3"
        >
          <p className="text-xs font-mono text-text-secondary">
            TRIGGER: cliente sin actividad → ACCIÓN: crear tarea de seguimiento
          </p>
          <input
            type="text"
            placeholder="Nombre de la automatización"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <label className="text-sm text-text-secondary flex items-center gap-2">
            Días de inactividad:
            <input
              type="number"
              min="0"
              value={daysInactive}
              onChange={(e) => setDaysInactive(e.target.value)}
              className="bg-bg-base border border-border rounded px-3 py-2 text-sm w-24 focus:outline-none focus:border-accent"
            />
          </label>
          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50 self-start"
          >
            {submitting ? 'Guardando...' : 'Guardar automatización'}
          </button>
        </form>
      )}

      {loading ? (
        <p className="text-text-secondary text-sm">Cargando automatizaciones...</p>
      ) : automations.length === 0 ? (
        <div className="border border-dashed border-border rounded-lg p-8 text-center">
          <p className="text-text-secondary text-sm">Todavía no tienes automatizaciones.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {automations.map((automation) => (
            <div key={automation.id} className="border border-border rounded-lg overflow-hidden">
              <div className="flex justify-between items-center p-4 bg-bg-surface">
                <div>
                  <p className="font-medium">{automation.name}</p>
                  <p className="text-xs font-mono text-text-secondary mt-1">
                    {automation.trigger_type} ({automation.trigger_config.days_inactive}d) →{' '}
                    {automation.action_type}
                  </p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleRun(automation.id)}
                    disabled={runningId === automation.id}
                    className="px-3 py-1.5 rounded border border-accent text-accent text-xs font-medium hover:bg-accent hover:text-white transition-colors disabled:opacity-50"
                  >
                    {runningId === automation.id ? 'Ejecutando...' : 'Run'}
                  </button>
                  <button
                    onClick={() => handleToggleExecutions(automation.id)}
                    className="px-3 py-1.5 rounded border border-border text-text-secondary text-xs hover:text-text-primary transition-colors"
                  >
                    {expandedId === automation.id ? 'Ocultar' : 'Historial'}
                  </button>
                  <button
                    onClick={() => handleDelete(automation.id)}
                    className="px-3 py-1.5 rounded border border-border text-error text-xs hover:opacity-80"
                  >
                    Eliminar
                  </button>
                </div>
              </div>

              {expandedId === automation.id && (
                <div className="p-4 border-t border-border">
                  {executions.length === 0 ? (
                    <p className="text-xs text-text-secondary">Sin ejecuciones todavía.</p>
                  ) : (
                    <div className="flex flex-col gap-2">
                      {executions.map((exec) => (
                        <div key={exec.id} className="flex items-center gap-3 text-xs font-mono">
                          <span
                            className={
                              exec.status === 'success' ? 'text-success' : 'text-error'
                            }
                          >
                            {exec.status}
                          </span>
                          <span className="text-text-secondary">
                            {new Date(exec.started_at).toLocaleString()}
                          </span>
                          <span className="text-text-primary">
                            {exec.trigger_context.customer_name || ''}
                          </span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Automations