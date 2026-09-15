import { useEffect, useState } from 'react'
import { listCustomers, createCustomer, deleteCustomer } from '../api/customers'

function Customers() {
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [company, setCompany] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function loadCustomers() {
    setLoading(true)
    const data = await listCustomers()
    setCustomers(data)
    setLoading(false)
  }

  useEffect(() => {
    loadCustomers()
  }, [])

  async function handleCreate(e) {
    e.preventDefault()
    setSubmitting(true)
    await createCustomer({ name, email: email || null, company: company || null })
    setName('')
    setEmail('')
    setCompany('')
    setShowForm(false)
    setSubmitting(false)
    loadCustomers()
  }

  async function handleDelete(id) {
    await deleteCustomer(id)
    loadCustomers()
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Clientes</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity"
        >
          {showForm ? 'Cancelar' : 'Nuevo cliente'}
        </button>
      </div>

      {showForm && (
        <form
          onSubmit={handleCreate}
          className="bg-bg-surface border border-border rounded-lg p-4 mb-6 flex flex-col gap-3"
        >
          <input
            type="text"
            placeholder="Nombre"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <input
            type="email"
            placeholder="Correo (opcional)"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <input
            type="text"
            placeholder="Empresa (opcional)"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="bg-bg-base border border-border rounded px-3 py-2 text-sm focus:outline-none focus:border-accent"
          />
          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 rounded bg-accent text-white text-sm font-medium hover:opacity-90 transition-opacity disabled:opacity-50 self-start"
          >
            {submitting ? 'Guardando...' : 'Guardar cliente'}
          </button>
        </form>
      )}

      {loading ? (
        <p className="text-text-secondary text-sm">Cargando clientes...</p>
      ) : customers.length === 0 ? (
        <div className="border border-dashed border-border rounded-lg p-8 text-center">
          <p className="text-text-secondary text-sm">Todavía no tienes clientes registrados.</p>
        </div>
      ) : (
        <div className="border border-border rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-bg-surface text-text-secondary text-left">
                <th className="px-4 py-3 font-medium">Nombre</th>
                <th className="px-4 py-3 font-medium">Correo</th>
                <th className="px-4 py-3 font-medium">Empresa</th>
                <th className="px-4 py-3 font-medium"></th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id} className="border-t border-border">
                  <td className="px-4 py-3">{customer.name}</td>
                  <td className="px-4 py-3 text-text-secondary">{customer.email || '—'}</td>
                  <td className="px-4 py-3 text-text-secondary">{customer.company || '—'}</td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => handleDelete(customer.id)}
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

export default Customers