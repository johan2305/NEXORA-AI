import { useEffect, useState } from 'react'
import { listTasks, createTask, deleteTask } from '../api/tasks'
import { createSmartTask } from '../api/ai'

const priorityColors = {
  low: 'text-text-secondary',
  medium: 'text-accent',
  high: 'text-warning',
  urgent: 'text-error',
}

const priorityLabels = {
  low: 'Baja',
  medium: 'Media',
  high: 'Alta',
  urgent: 'Urgente',
}

function Tasks() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [title, setTitle] = useState('')
  const [priority, setPriority] = useState('medium')
  const [submitting, setSubmitting] = useState(false)

  const [aiText, setAiText] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiError, setAiError] = useState('')

  async function loadTasks() {
    setLoading(true)
    const data = await listTasks()
    setTasks(data)
    setLoading(false)
  }

  useEffect(() => {
    loadTasks()
  }, [])

  async function handleCreate(e) {
    e.preventDefault()
    setSubmitting(true)
    await createTask({ title, priority })
    setTitle('')
    setPriority('medium')
    setShowForm(false)
    setSubmitting(false)
    loadTasks()
  }

  async function handleDelete(id) {
    await deleteTask(id)
    loadTasks()
  }

  async function handleAiSubmit(e) {
    e.preventDefault()
    setAiError('')
    setAiLoading(true)
    try {
      await createSmartTask(aiText)
      setAiText('')
      loadTasks()
    } catch (err) {
      setAiError('No se pudo procesar la solicitud con IA. Intenta de nuevo.')
    } finally {
      setAiLoading(false)
    }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Tareas</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity"
        >
          {showForm ? 'Cancelar' : 'Nueva tarea'}
        </button>
      </div>

      <form
        onSubmit={handleAiSubmit}
        className="bg-bg-surface border border-accent/40 rounded-lg p-4 mb-6"
      >
        <p className="text-xs font-mono text-accent mb-2">COPILOTO NEXORA</p>
        <div className="flex gap-2">
          <input
            type="text"
            placeholder="Describe lo que necesitas, ej: 'llamar a Juan mañana, es urgente'"
            value={aiText}
            onChange={(e) => setAiText(e.target.value)}
            required
            className="flex-1 bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <button
            type="submit"
            disabled={aiLoading}
            className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50 whitespace-nowrap"
          >
            {aiLoading ? 'Analizando...' : 'Crear con IA'}
          </button>
        </div>
        {aiError && <p className="text-error text-xs mt-2">{aiError}</p>}
      </form>

      {showForm && (
        <form
          onSubmit={handleCreate}
          className="bg-bg-surface border border-border rounded-lg p-4 mb-6 flex flex-col gap-3"
        >
          <input
            type="text"
            placeholder="Título de la tarea"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <select
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          >
            <option value="low">Baja</option>
            <option value="medium">Media</option>
            <option value="high">Alta</option>
            <option value="urgent">Urgente</option>
          </select>
          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50 self-start"
          >
            {submitting ? 'Guardando...' : 'Guardar tarea'}
          </button>
        </form>
      )}

      {loading ? (
        <p className="text-text-secondary text-sm">Cargando tareas...</p>
      ) : tasks.length === 0 ? (
        <div className="border border-dashed border-border rounded-lg p-8 text-center">
          <p className="text-text-secondary text-sm">Todavía no tienes tareas registradas.</p>
        </div>
      ) : (
        <div className="border border-border rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-bg-surface text-text-secondary text-left">
                <th className="px-4 py-3 font-medium">Título</th>
                <th className="px-4 py-3 font-medium">Prioridad</th>
                <th className="px-4 py-3 font-medium">Estado</th>
                <th className="px-4 py-3 font-medium">Creada por</th>
                <th className="px-4 py-3 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr key={task.id} className="border-t border-border">
                  <td className="px-4 py-3">{task.title}</td>
                  <td className={`px-4 py-3 font-medium ${priorityColors[task.priority]}`}>
                    {priorityLabels[task.priority] || task.priority}
                  </td>
                  <td className="px-4 py-3 text-text-secondary">{task.status}</td>
                  <td className="px-4 py-3 text-text-secondary font-mono text-xs">{task.created_by}</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDelete(task.id)}
                      className="text-error text-xs hover:opacity-80"
                    >
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

export default Tasks