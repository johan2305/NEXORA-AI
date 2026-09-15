import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register, saveTokens } from '../api/auth'

function Register() {
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [organizationName, setOrganizationName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const tokens = await register({ email, password, fullName, organizationName })
      saveTokens(tokens)
      navigate('/dashboard')
    } catch (err) {
      const detail = err.response?.data?.detail
      setError(Array.isArray(detail) ? detail[0]?.msg : detail || 'No se pudo registrar')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-bg-base text-text-primary flex items-center justify-center font-sans">
      <div className="w-full max-w-sm bg-bg-surface border border-border rounded-lg p-8">
        <h1 className="text-2xl font-semibold mb-1">NEXORA AI</h1>
        <p className="text-text-secondary text-sm mb-6">Crea tu cuenta y tu organización</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <input
            type="text"
            placeholder="Nombre completo"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-text-primary placeholder:text-text-secondary focus:outline-none focus:border-accent"
          />
          <input
            type="text"
            placeholder="Nombre de tu empresa"
            value={organizationName}
            onChange={(e) => setOrganizationName(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-text-primary placeholder:text-text-secondary focus:outline-none focus:border-accent"
          />
          <input
            type="email"
            placeholder="Correo electrónico"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-text-primary placeholder:text-text-secondary focus:outline-none focus:border-accent"
          />
          <input
            type="password"
            placeholder="Contraseña (mín. 8, con mayúscula y minúscula)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="bg-bg-base border border-border rounded px-3 py-2 text-text-primary placeholder:text-text-secondary focus:outline-none focus:border-accent"
          />

          {error && <p className="text-error text-sm">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className="bg-accent text-white rounded px-3 py-2 font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {loading ? 'Creando cuenta...' : 'Crear cuenta'}
          </button>
        </form>

        <p className="text-text-secondary text-sm mt-6">
          ¿Ya tienes cuenta? <Link to="/login" className="text-accent">Inicia sesión</Link>
        </p>
      </div>
    </div>
  )
}

export default Register