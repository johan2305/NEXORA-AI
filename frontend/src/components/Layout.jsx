import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { clearTokens } from '../api/auth'
import { useTheme } from '../context/ThemeContext'
import NotificationBell from './NotificationBell'

const navItems = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/customers', label: 'Clientes' },
  { to: '/projects', label: 'Proyectos' },
  { to: '/tasks', label: 'Tareas' },
  { to: '/automations', label: 'Automatizaciones' },
]

function Layout() {
  const navigate = useNavigate()
  const { theme, toggleTheme } = useTheme()

  function handleLogout() {
    clearTokens()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-bg-base text-text-primary font-sans flex">
      <aside className="w-56 border-r border-border p-4 flex flex-col">
        <h1 className="text-lg font-semibold mb-8 px-2">NEXORA AI</h1>
        <nav className="flex flex-col gap-1 flex-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `px-3 py-2 rounded text-sm transition-colors ${
                  isActive
                    ? 'bg-bg-surface text-accent'
                    : 'text-text-secondary hover:text-text-primary'
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="flex flex-col gap-2 pt-4 border-t border-border">
          <NotificationBell />
          <button
            onClick={toggleTheme}
            className="px-3 py-2 rounded text-sm text-text-secondary hover:text-text-primary text-left"
          >
            Tema: {theme}
          </button>
          <button
            onClick={handleLogout}
            className="px-3 py-2 rounded text-sm text-error text-left hover:opacity-80"
          >
            Cerrar sesión
          </button>
        </div>
      </aside>
      <main className="flex-1 p-8 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout