import { useEffect, useState } from 'react'
import { listProjects, createProject, deleteProject } from '../api/projects'

const statusLabels = {
  planning: 'Planeación',
  active: 'Activo',
  on_hold: 'En pausa',
  completed: 'Completado',
}

function Projects() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState('planning')
  const [submitting, setSubmitting] = useState(false)

  async function loadProjects() {
    setLoading(true)
    const data = await listProjects()
    setProjects(data)
    setLoading(false)
  }

  useEffect(() => {
    loadProjects()
  }, [])

  async function handleCreate(e) {
    e.preventDefault()
    setSubmitting(true)
    await createProject({ name, description: description || null, status })
    setName('')
    setDescription('')
    setStatus('planning')
    setShowForm(false)
    setSubmitting(false)
    loadProjects()
  }

  async function handleDelete(id) {
    await deleteProject(id)
    loadProjects()
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Proyectos</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity"
        >
          {showForm ? 'Cancelar' : 'Nuevo proyecto'}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleCreate}
          className="bg-bg-surface border border-border rounded-lg p-4 mb-6 flex flex-col gap-3"
        >
          <input
            type="text"
            placeholder="Nombre del proyecto"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <textarea
            placeholder="Descripción (opcional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={2}
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent resize-none"
          />
          <select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          >
            <option value="planning">Planeación</option>
            <option value="active">Activo</option>
            <option value="on_hold">En pausa</option>
            <option value="completed">Completado</option>
          </select>
          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50 self-start"
          >
            {submitting ? 'Guardando...' : 'Guardar proyecto'}
          </button>
        </form>
      )}

      {loading ? (
        <p className="text-text-secondary text-sm">Cargando proyectos...</p>
      ) : projects.length === 0 ? (
        <div className="border border-dashed border-border rounded-lg p-8 text-center">
          <p className="text-text-secondary text-sm">Todavía no tienes proyectos registrados.</p>
        </div>
      ) : (
        <div className="border border-border rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-bg-surface text-text-secondary text-left">
                <th className="px-4 py-3 font-medium">Nombre</th>
                <th className="px-4 py-3 font-medium">Estado</th>
                <th className="px-4 py-3 font-medium">Descripción</th>
                <th className="px-4 py-3 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {projects.map((project) => (
                <tr key={project.id} className="border-t border-border">
                  <td className="px-4 py-3">{project.name}</td>
                  <td className="px-4 py-3 text-text-secondary">
                    {statusLabels[project.status] || project.status}
                  </td>
                  <td className="px-4 py-3 text-text-secondary">{project.description || '—'}</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDelete(project.id)}
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

export default Projects